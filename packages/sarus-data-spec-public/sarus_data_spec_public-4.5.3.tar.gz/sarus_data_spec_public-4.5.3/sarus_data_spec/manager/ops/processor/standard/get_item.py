import typing as t
import warnings

import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATA, MULTIPLICITY
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.visitor_selector import (  # noqa : E501
    select_rows,
)
from sarus_data_spec.marginals import marginals as marg_builder
from sarus_data_spec.multiplicity import multiplicity as multiplicity_builder
from sarus_data_spec.path import Path, straight_path
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.type as sdt
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
    from sarus_data_spec.manager.ops.sql_utils.schema_translations import (
        async_sa_metadata_from_dataset,
    )
except ModuleNotFoundError:
    warnings.warn("sql utils not installed.")


class GetItemStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        sub_types = parent_schema.data_type().sub_types(path)
        assert len(sub_types) == 1
        new_type = sub_types[0]
        # TODO: update foreign_keys/primary_keys in the type
        previous_fields = parent_schema.type().children()

        try:
            parent_stats = (await self.parent_marginals()).statistics()
            path = Path(self.dataset.transform().protobuf().spec.get_item.path)
            tab_multiplicity = parent_stats.nodes_statistics(path)[
                0
            ].multiplicity()
            properties = {MULTIPLICITY: str(tab_multiplicity)}
        except Exception:
            properties = {}
        if DATA in previous_fields.keys():
            previous_fields[DATA] = new_type
            new_type = sdt.Struct(fields=previous_fields)
        return schema(
            self.dataset,
            schema_type=new_type,
            privacy_unit_tracking_paths=None,
            name=parent_schema.name(),
            properties=properties,
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


class GetItem(StandardDatasetImplementation):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a get_item transform
    """

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        previous_ds = t.cast(Dataset, self.parent())
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        parent_schema = await self.parent_schema()

        async def get_item_func(batch: pa.RecordBatch) -> pa.Array:
            array = convert_record_batch(
                record_batch=batch, _type=parent_schema.type()
            )
            # VERY UGLY SHOULD BE REMOVED WHEN WE HAVE PROTECTED TYPE
            if DATA in parent_schema.type().children():
                old_arrays = array.flatten()
                idx_data = array.type.get_field_index(DATA)
                list_col_names = list(parent_schema.type().children().keys())
                list_idx = [
                    array.type.get_field_index(col) for col in list_col_names
                ]
                reordered_list_col_names = [
                    list_col_names[i]
                    for i in sorted(
                        range(len(list_idx)), key=lambda k: list_idx[k]
                    )
                ]
                array = old_arrays[idx_data]
                updated_array = get_items(
                    _type=parent_schema.data_type(),
                    array=array,
                    path=path,
                )
                old_arrays[idx_data] = updated_array
                return pa.StructArray.from_arrays(
                    old_arrays,
                    names=reordered_list_col_names,
                )

            updated_array = get_items(
                _type=parent_schema.data_type(),
                array=array,
                path=path,
            )
            if isinstance(updated_array, pa.StructArray):
                return updated_array
            return pa.StructArray.from_arrays(
                [updated_array],
                names=[path.to_strings_list()[0][-1]],
            )

        return await self.ensure_batch_correct(
            async_iterator=await previous_ds.async_to_arrow(
                batch_size=batch_size
            ),
            batch_size=batch_size,
            func_to_apply=get_item_func,
        )

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        sqlalchemy_metadata = await async_sa_metadata_from_dataset(
            t.cast(Dataset, self.parent())
        )
        queries: t.Dict[t.Tuple[str, ...], str] = {}
        table_path = Path(
            self.dataset.transform().protobuf().spec.get_item.path
        )
        curr_path = table_path.to_strings_list()[0]
        full_tablename = curr_path[1:] if curr_path[0] == DATA else curr_path
        sa_table_name = path_to_quoted_string(straight_path(full_tablename))
        sa_table = sqlalchemy_metadata.tables[sa_table_name]
        table_query = sa.select(sa_table)

        queries[()] = sqlalchemy_query_to_string(table_query)
        return queries

    async def size(self) -> st.Size:
        sizes = await self.parent_size()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = sizes.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return size_builder(dataset=self.dataset, statistics=new_stats[0])

    async def multiplicity(self) -> st.Multiplicity:
        multiplicities = await self.parent_multiplicity()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = multiplicities.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return multiplicity_builder(
            dataset=self.dataset, statistics=new_stats[0]
        )

    async def bounds(self) -> st.Bounds:
        bounds = await self.parent_bounds()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = bounds.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return bounds_builder(dataset=self.dataset, statistics=new_stats[0])

    async def marginals(self) -> st.Marginals:
        marginals = await self.parent_marginals()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = marginals.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return marg_builder(dataset=self.dataset, statistics=new_stats[0])


def get_items(array: pa.Array, path: st.Path, _type: st.Type) -> pa.Array:
    """Visitor selecting columns based on the type.
    The idea is that at each level,
    the filter for the array is computed, and for the union,
    we remove the fields that we want to filter among
    the columns
    """

    class ItemSelector(st.TypeVisitor):
        batch_array: pa.Array = array

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if len(path.sub_paths()) > 0:
                sub_path = path.sub_paths()[0]
                idx = array.type.get_field_index(sub_path.label())
                self.batch_array = get_items(
                    array=array.flatten()[idx],
                    path=sub_path,
                    _type=fields[sub_path.label()],
                )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            idx = self.batch_array.type.get_field_index(path.label())
            array = self.batch_array.flatten()(idx)
            if len(path.sub_paths()) == 0:
                self.batch_array = array
            else:
                self.batch_array = get_items(
                    array=array, path=path.sub_paths()[0], _type=type
                )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if len(path.sub_paths()) == 0:
                self.batch_array = array
            else:
                sub_path = path.sub_paths()[0]
                idx = array.type.get_field_index(sub_path.label())
                self.batch_array = get_items(
                    array=array.flatten()[idx],
                    path=sub_path,
                    _type=fields[sub_path.label()],
                )

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
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

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

    visitor = ItemSelector()
    _type.accept(visitor)
    return visitor.batch_array
