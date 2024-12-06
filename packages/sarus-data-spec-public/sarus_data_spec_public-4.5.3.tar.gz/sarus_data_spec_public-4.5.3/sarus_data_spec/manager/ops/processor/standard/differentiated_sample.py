import typing as t
import warnings

import numpy as np
import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATA
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.processor.standard.sample import (
    fast_gather,
    new_sampling_ratio,
    sample_arrow_to_arrow,
)
from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)
from sarus_data_spec.marginals import marginals as marginals_builder
from sarus_data_spec.multiplicity import multiplicity as multiplicity_builder
from sarus_data_spec.path import straight_path
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.typing as st

try:
    import sqlalchemy as sa
except ModuleNotFoundError:
    warnings.warn("sqlalchemy not installed. No sampling on bigdata")

try:
    from sarus_data_spec.manager.ops.processor.standard.sampling.differentiated_sampling_sizes import (  # noqa: E501
        differentiated_sampling_sizes,
    )
    from sarus_data_spec.manager.ops.processor.standard.sampling.size_utils import (  # noqa: E501
        differentiated_sampled_size,
        sampled_size,
    )
except ModuleNotFoundError as exception:
    # for the public repo
    if (
        exception.name
        == "sarus_data_spec.manager.ops.processor.standard.sampling"  # noqa: E501
    ):
        pass
    else:
        raise exception

try:
    from sarus_data_spec.manager.ops.sql_utils.bigdata import (
        find_optimal_multiplier_fraction,
        path_to_quoted_string,
        sqlalchemy_query_to_string,
    )
    from sarus_data_spec.manager.ops.sql_utils.queries import nest_queries
    from sarus_data_spec.manager.ops.sql_utils.schema_translations import (
        async_sa_metadata_from_dataset,
    )
except ModuleNotFoundError:
    warnings.warn("sql utils not installed.")


class DifferentiatedSampleStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            privacy_unit_tracking_paths=parent_schema.protobuf().privacy_unit,
            properties=parent_schema.properties(),
            name=parent_schema.name(),
        )


class DifferentiatedSample(StandardDatasetImplementation):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a differentiated transform
    """

    async def size(self) -> st.Size:
        parent_size = await self.parent_size()

        previous_schema = await self.parent_schema()
        if len(previous_schema.tables()) == 1:
            size_ratio = new_sampling_ratio(
                self.dataset, parent_size.statistics()
            )
            if size_ratio >= 1:
                return size_builder(self.dataset, parent_size.statistics())
            return size_builder(
                self.dataset,
                sampled_size(parent_size.statistics(), size_ratio),
            )
        size_dict = await differentiated_sampling_sizes(self.dataset)
        return size_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_size.statistics(), size_dict, curr_path=[DATA]
            ),
        )

    async def multiplicity(self) -> st.Multiplicity:
        parent_multiplicity = await self.parent_multiplicity()
        return multiplicity_builder(
            self.dataset, parent_multiplicity.statistics()
        )

    async def bounds(self) -> st.Bounds:
        parent_bounds = await self.parent_bounds()
        previous_schema = await self.parent_schema()
        if len(previous_schema.tables()) == 1:
            size_ratio = new_sampling_ratio(
                self.dataset, parent_bounds.statistics()
            )

            if size_ratio >= 1:
                return bounds_builder(self.dataset, parent_bounds.statistics())

            return bounds_builder(
                self.dataset,
                sampled_size(parent_bounds.statistics(), size_ratio),
            )

        size_dict = await differentiated_sampling_sizes(self.dataset)
        return bounds_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_bounds.statistics(), size_dict, curr_path=[DATA]
            ),
        )

    async def marginals(self) -> st.Marginals:
        parent_marginals = await self.parent_marginals()
        previous_schema = await self.parent_schema()
        if len(previous_schema.tables()) == 1:
            size_ratio = new_sampling_ratio(
                self.dataset, parent_marginals.statistics()
            )

            if size_ratio >= 1:
                return marginals_builder(
                    self.dataset, parent_marginals.statistics()
                )

            return marginals_builder(
                self.dataset,
                sampled_size(parent_marginals.statistics(), size_ratio),
            )

        size_dict = await differentiated_sampling_sizes(self.dataset)
        return marginals_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_marginals.statistics(), size_dict, curr_path=[DATA]
            ),
        )

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = t.cast(Dataset, self.parent())
        if parent.manager().is_big_data(parent):
            queries = await self.sql_implementation()
            assert queries is not None
            # rewrite queries as nested dict rather than dict[tuple,str]
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
        seed = Scalar(
            self.dataset.transform().protobuf().spec.differentiated_sample.seed
        ).value()
        generator = np.random.default_rng(seed)

        previous_ds = t.cast(Dataset, self.parent())
        previous_schema = await self.parent_schema()

        if len(previous_schema.tables()) == 1:
            return await sample_arrow_to_arrow(self, batch_size)

        parent_batches = [
            convert_record_batch(batch, previous_schema.type())
            async for batch in await self.parent_to_arrow()
        ]
        struct_arr = pa.concat_arrays(parent_batches)
        previous_size = await previous_ds.manager().async_size(previous_ds)
        assert previous_size

        size_dict = await differentiated_sampling_sizes(self.dataset)

        indices_to_take = sample_indices_from_array(
            array=struct_arr.flatten()[struct_arr.type.get_field_index(DATA)],
            stat=previous_size.statistics(),
            selected_indices=pa.array(
                np.linspace(0, len(struct_arr) - 1, len(struct_arr), dtype=int)
            ),
            new_size_dict=size_dict,
            curr_path=[DATA],
            random_gen=generator,
        )
        return fast_gather(
            indices=indices_to_take.to_numpy(),
            batches=pa.Table.from_arrays(
                struct_arr.flatten(),
                names=list(previous_schema.type().children().keys()),
            ).to_batches(max_chunksize=1000),
            batch_size=batch_size,
        )

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        schema = await self.parent_schema()
        previous_size = await self.parent_size()
        size_dict = await differentiated_sampling_sizes(self.dataset)
        assert previous_size
        previous_stats = previous_size.statistics()
        sqlalchemy_metadata = await async_sa_metadata_from_dataset(
            self.dataset
        )

        queries = {}
        for table_path in schema.tables():
            curr_path = table_path.to_strings_list()[0]
            full_tablename = (
                curr_path[1:] if curr_path[0] == DATA else curr_path
            )
            sa_table_name = path_to_quoted_string(
                straight_path(full_tablename)
            )
            sa_table = sqlalchemy_metadata.tables[sa_table_name]
            sample_size = size_dict[table_path]
            if (
                self.dataset.transform()
                .protobuf()
                .spec.differentiated_sample.HasField("fraction")
            ):
                fraction = (
                    self.dataset.transform()
                    .protobuf()
                    .spec.differentiated_sample.fraction
                )
                sample_query = sa.select(sa_table).where(
                    sa.func.random() < fraction
                )
            else:
                fraction = (
                    sample_size
                    / previous_stats.nodes_statistics(table_path)[0].size()
                )
                mult_fraction = find_optimal_multiplier_fraction(
                    previous_stats.nodes_statistics(table_path)[0].size(),
                    sample_size,
                )
                optimal_fraction = round(fraction * mult_fraction, 4)
                sample_query = (
                    sa.select(sa_table)
                    .where(
                        sa.func.random()
                        < sa.literal(optimal_fraction, sa.FLOAT)
                    )
                    .order_by(sa.func.random())
                    .limit(sample_size)
                )

            queries[tuple(full_tablename)] = sqlalchemy_query_to_string(
                sample_query
            )

        return queries


def sample_indices_from_array(
    array: pa.Array,
    stat: st.Statistics,
    selected_indices: pa.Array,
    new_size_dict: t.Dict[st.Path, int],
    random_gen: np.random.Generator,
    curr_path: t.List[str],
) -> pa.Array:
    class IndicesSampler(st.StatisticsVisitor):
        indices: pa.Array = selected_indices
        batch_array: pa.Array = array

        def Union(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            new_indices = []
            for field, field_stat in fields.items():
                index_element = self.batch_array.type.get_field_index(field)
                filter_idex = pa.array(
                    np.equal(
                        self.batch_array.field("field_selected"),
                        np.array(field),
                    )
                )
                updated_indices = sample_indices_from_array(
                    self.batch_array.filter(filter_idex).flatten()[
                        index_element
                    ],
                    field_stat,
                    self.indices.filter(filter_idex),
                    new_size_dict,
                    random_gen,
                    [*(el for el in curr_path), field],
                )
                new_indices.append(updated_indices)
            self.indices = pa.concat_arrays(new_indices)

        def Struct(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # sample indices to size and sample ratio
            new_size = new_size_dict[straight_path(curr_path.copy())]
            self.indices = pa.array(
                random_gen.choice(
                    self.indices,
                    replace=False,
                    size=min(new_size, size, len(array)),
                )
            )  # need to put array otherwise because of dp
            # we can have size and new size larger and an error will be raised

        def Null(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Unit(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Boolean(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[bool]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Id(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Integer(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[str]] = None,
            values: t.Optional[t.List[float]] = None,
            name: str = "Enum",
        ) -> None:
            raise NotImplementedError

        def Float(
            self,
            size: int,
            multiplicity: float,
            min_value: float,
            max_value: float,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[float]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            example: str = "",
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Bytes(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Optional(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            statistics: st.Statistics,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            name: str = "List",
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            statistics: st.Statistics,
            size: int,
            multiplicity: float,
            min_values: t.Optional[t.List[float]] = None,
            max_values: t.Optional[t.List[float]] = None,
            name: str = "Array",
            probabilities: t.Optional[t.List[t.List[float]]] = None,
            values: t.Optional[t.List[t.List[float]]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = IndicesSampler()
    stat.accept(visitor)
    return visitor.indices
