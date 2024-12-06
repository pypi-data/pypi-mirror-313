import typing as t
import pyarrow as pa
import numpy as np
import pyarrow.compute as pc
import warnings

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.constants import (
    DATA,
    MULTIPLICITY,
)
from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)

from sarus_data_spec.dataset import Dataset
from sarus_data_spec.path import Path, straight_path
from sarus_data_spec.marginals import marginals as marg_builder
from sarus_data_spec.multiplicity import multiplicity as multiplicity_builder
from sarus_data_spec.size import size as size_builder
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.schema import schema
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


class SelectTableStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        path = Path(self.dataset.transform().protobuf().spec.select_table.path)
        sub_types = parent_schema.data_type().sub_types(path)
        assert len(sub_types) == 1
        new_type = sub_types[0]
        # TODO: update foreign_keys/primary_keys in the type
        previous_fields = parent_schema.type().children()

        try:
            parent_stats = (await self.parent_marginals()).statistics()
            path = Path(
                self.dataset.transform().protobuf().spec.select_table.path
            )
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


class SelectTable(StandardDatasetImplementation):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a select_table transform
    """

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        previous_ds = t.cast(Dataset, self.parent())
        path = Path(self.dataset.transform().protobuf().spec.select_table.path)
        parent_schema = await self.parent_schema()

        async def select_table_func(
            batch: pa.RecordBatch,
        ) -> pa.Array:
            array = convert_record_batch(
                record_batch=batch, _type=parent_schema.type()
            )

            if DATA in parent_schema.type().children():
                old_arrays = array.flatten()
                idx_data = array.type.get_field_index(DATA)
                array = old_arrays[idx_data]
                updated_array, filter_indices = select_table(
                    _type=parent_schema.data_type(),
                    array=array,
                    path=path,
                )
                old_arrays[idx_data] = updated_array

                new_struct = pa.StructArray.from_arrays(
                    old_arrays,
                    names=list(parent_schema.type().children().keys()),
                )
                return new_struct.filter(filter_indices)

            updated_array, filter_indices = select_table(
                array=array, path=path, _type=parent_schema.data_type()
            )
            if isinstance(updated_array, pa.StructArray):
                return updated_array.filter(filter_indices)
            else:
                old_arrays[idx_data] = updated_array

                new_struct = pa.StructArray.from_arrays(
                    old_arrays,
                    names=[path.to_strings_list()[0][-1]],
                )
                return new_struct.filter(filter_indices)

        return await self.ensure_batch_correct(
            async_iterator=await previous_ds.async_to_arrow(
                batch_size=batch_size
            ),
            batch_size=batch_size,
            func_to_apply=select_table_func,
        )

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        sqlalchemy_metadata = await async_sa_metadata_from_dataset(
            t.cast(Dataset, self.parent())
        )
        queries: t.Dict[t.Tuple[str, ...], str] = {}
        table_path = Path(
            self.dataset.transform().protobuf().spec.select_table.path
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
        path = Path(self.dataset.transform().protobuf().spec.select_table.path)
        new_stats = sizes.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return size_builder(dataset=self.dataset, statistics=new_stats[0])

    async def multiplicity(self) -> st.Multiplicity:
        multiplicities = await self.parent_multiplicity()
        path = Path(self.dataset.transform().protobuf().spec.select_table.path)
        new_stats = multiplicities.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return multiplicity_builder(
            dataset=self.dataset, statistics=new_stats[0]
        )

    async def bounds(self) -> st.Bounds:
        bounds = await self.parent_bounds()
        path = Path(self.dataset.transform().protobuf().spec.select_table.path)
        new_stats = bounds.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return bounds_builder(dataset=self.dataset, statistics=new_stats[0])

    async def marginals(self) -> st.Marginals:
        marginals = await self.parent_marginals()
        path = Path(self.dataset.transform().protobuf().spec.select_table.path)
        new_stats = marginals.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return marg_builder(dataset=self.dataset, statistics=new_stats[0])


def select_table(
    array: pa.Array, path: st.Path, _type: st.Type, is_optional: bool = False
) -> t.Tuple[pa.Array, pa.Array]:
    """Visitor selecting columns based on the type."""

    class TableSelector(sdt.TypeVisitor_):
        batch_array: pa.Array = array
        filter_indices: pa.Array

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if len(path.sub_paths()) == 0:
                self.batch_array = array
                self.filter_indices = np.full_like(array, True)
            else:
                sub_path = path.sub_paths()[0]
                idx = array.type.get_field_index(sub_path.label())

                initial_field_selected = self.batch_array.field(
                    "field_selected"
                ).to_numpy(zero_copy_only=False)

                self.batch_array, filter_idx = select_table(
                    array=array.flatten()[idx],
                    path=sub_path,
                    _type=fields[sub_path.label()],
                )

                field_selected = pa.array(
                    initial_field_selected == sub_path.label(), type=pa.bool_()
                )
                result = pc.and_(field_selected, filter_idx)
                self.filter_indices = result

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.filter_indices = pa.array(
                [True] * len(self.batch_array), type=pa.bool_()
            )

    visitor = TableSelector()
    _type.accept(visitor)
    return visitor.batch_array, visitor.filter_indices
