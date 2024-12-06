import logging
import typing as t
import warnings

import numpy as np
import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.constants import DATA
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.processor.standard.sample import fast_gather
from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)
from sarus_data_spec.path import straight_path
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema
import sarus_data_spec.typing as st

try:
    import sqlalchemy as sa
except ModuleNotFoundError:
    warnings.warn("sqlalchemy not installed. No sampling on bigdata")

try:
    from sarus_data_spec.manager.ops.sql_utils.bigdata import (
        path_to_quoted_string,
        sqlalchemy_query_to_string,
    )
    from sarus_data_spec.manager.ops.sql_utils.queries import nest_queries
    from sarus_data_spec.manager.ops.sql_utils.schema_translations import (
        async_sa_metadata_from_dataset,
    )
except ModuleNotFoundError:
    warnings.warn("sql utils not installed.")

logger = logging.getLogger(__name__)


class ToSmallDataStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            privacy_unit_tracking_paths=parent_schema.protobuf().privacy_unit,
            properties=parent_schema.properties(),
            name=parent_schema.name(),
        )

    def is_pup_able(self) -> bool:
        """Checks if the dataspec has a transform that either has a PUP
        equivalent or does not require one, allowing the rewritten dataspec to
        be considered 'PUP' if the input rewritten PUP token is not None.
        This op can be applied after a non-PUP dataset.
        """
        return True

    def pup_transform(self) -> t.Optional[st.Transform]:
        """Needed during the rewriting. The PUP transform is the
        transform itself. The PUP equivalent to the transform is
        transform itself.
        """
        return self.dataspec.transform()


class ToSmallData(StandardDatasetImplementation):
    async def size(self) -> st.Size:
        raise NotImplementedError

    async def multiplicity(self) -> st.Multiplicity:
        raise NotImplementedError

    async def marginals(self) -> st.Marginals:
        raise NotImplementedError

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = t.cast(Dataset, self.parent())
        if parent.manager().is_big_data(parent):
            queries = await self.sql_implementation()
            assert queries is not None
            nested_queries = nest_queries(queries)
            schema = await self.dataset.async_schema()
            return await self.dataset.manager().async_sql(
                parent,
                query=nested_queries,
                batch_size=batch_size,
                result_type=schema.type(),
            )
        return await self._arrow_to_arrow(batch_size)

    async def _arrow_to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        previous_schema = await self.parent_schema()
        parent_batches = [
            convert_record_batch(batch, previous_schema.type())
            async for batch in await self.parent_to_arrow(
                batch_size=batch_size
            )
        ]
        struct_arr = pa.concat_arrays(parent_batches)
        # maybe to add
        # if len(previous_schema.tables()) == 1:
        #    # to change here
        #    return await limit_arrow_to_arrow(self, batch_size)

        size_dict = await to_small_data_sizes(self.dataset)
        to_small_data_proto = (
            self.dataset.transform().protobuf().spec.to_small_data
        )
        random_sampling = to_small_data_proto.random_sampling
        seed = Scalar(to_small_data_proto.seed).value()
        generator = np.random.default_rng(seed)

        if struct_arr.type.get_field_index(DATA) == -1:
            array_to_take = struct_arr
        else:
            array_to_take = struct_arr.flatten()[
                struct_arr.type.get_field_index(DATA)
            ]

        indices_to_take = limit_indices_from_array(
            array=array_to_take,
            _type=previous_schema.data_type(),
            selected_indices=pa.array(
                np.linspace(0, len(struct_arr) - 1, len(struct_arr), dtype=int)
            ),
            new_size_dict=size_dict,
            curr_path=[DATA],
            random_sampling=random_sampling,
            random_gen=generator,
        )
        return fast_gather(
            indices=indices_to_take.to_numpy(),
            batches=pa.Table.from_arrays(
                struct_arr.flatten(),
                names=[one_child.name for one_child in list(struct_arr.type)],
            ).to_batches(max_chunksize=1000),
            batch_size=batch_size,
        )

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        schema = await self.parent_schema()
        to_small_data_proto = (
            self.dataset.transform().protobuf().spec.to_small_data
        )
        random_sampling = to_small_data_proto.random_sampling
        size_dict = await to_small_data_sizes(self.dataset)
        sqlalchemy_metadata = await async_sa_metadata_from_dataset(
            self.dataset
        )
        queries = {}
        schema_name = schema.name()
        for table_path in schema.tables():
            size_table = size_dict[table_path]
            curr_path = table_path.to_strings_list()[0]
            full_tablename = (
                curr_path[1:] if (curr_path[0] == DATA) else curr_path
            )
            is_there_table_name = len(full_tablename) > 0
            if not is_there_table_name:
                full_tablename = [schema_name]
            sa_table_name = path_to_quoted_string(
                straight_path(full_tablename)
            )
            sa_table = sqlalchemy_metadata.tables[sa_table_name]
            if random_sampling:
                sample_query = (
                    sa.select(sa_table)
                    .order_by(sa.func.random())
                    .limit(size_table)
                )
            else:
                sample_query = sa.select(sa_table).limit(size_table)
            if not is_there_table_name:
                full_tablename = [""]
            queries[tuple(full_tablename)] = sqlalchemy_query_to_string(
                sample_query
            )
        return queries


async def to_small_data_sizes(
    dataset: st.Dataset,
) -> t.Dict[st.Path, int]:
    """Get the sampling rates for each table"""
    parent_ds = t.cast(Dataset, dataset.parents()[0][0])
    to_small_data_proto = dataset.transform().protobuf().spec.to_small_data
    sampled_size = to_small_data_proto.size
    schema = await parent_ds.manager().async_schema(parent_ds)
    table_paths = schema.tables()
    size_per_table = int(int(sampled_size) / len(table_paths))

    # test if min_table_size is not too high
    return {table_path: size_per_table for table_path in table_paths}


def limit_indices_from_array(
    array: pa.Array,
    _type: st.Type,
    selected_indices: pa.Array,
    new_size_dict: t.Dict[st.Path, int],
    curr_path: t.List[str],
    random_gen: np.random.Generator,
    random_sampling: bool,
) -> pa.Array:
    class IndicesLimit(st.TypeVisitor):
        indices: pa.Array = selected_indices
        batch_array: pa.Array = array

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            new_indices = []
            for item_name, item_type in fields.items():
                index_element = self.batch_array.type.get_field_index(
                    item_name
                )
                filter_idex = pa.array(
                    np.equal(
                        self.batch_array.field("field_selected"),
                        np.array(item_name),
                    )
                )
                updated_indices = limit_indices_from_array(
                    self.batch_array.filter(filter_idex).flatten()[
                        index_element
                    ],
                    item_type,
                    self.indices.filter(filter_idex),
                    new_size_dict,
                    [*(el for el in curr_path), item_name],
                    random_gen,
                    random_sampling,
                )
                new_indices.append(updated_indices)
            self.indices = pa.concat_arrays(new_indices)

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            new_size = new_size_dict[straight_path(curr_path.copy())]
            # taking the first new_size indices
            if random_sampling:
                self.indices = pa.array(
                    random_gen.choice(
                        self.indices,
                        replace=False,
                        size=min(new_size, len(self.indices), len(array)),
                    )
                )
            else:
                self.indices = self.indices.slice(0, new_size)

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = IndicesLimit()
    _type.accept(visitor)
    return visitor.indices
