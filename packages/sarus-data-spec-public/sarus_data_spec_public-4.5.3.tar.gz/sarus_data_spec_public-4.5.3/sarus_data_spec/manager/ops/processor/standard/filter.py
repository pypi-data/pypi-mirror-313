import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import (
    DATA,
    OPTIONAL_VALUE,
    PRIMARY_KEYS,
)
from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.visitor_selector import (  # noqa: E501
    filter_primary_keys,
    select_rows,
    update_fks,
)
from sarus_data_spec.marginals import marginals as marg_builder
from sarus_data_spec.multiplicity import multiplicity as multiplicity_builder
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.statistics as sds
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st


class FilterStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        new_type = sdt.Type(
            self.dataset.transform().protobuf().spec.filter.filter
        )
        new_type = update_fks(
            curr_type=new_type,
            original_type=new_type,  # type:ignore
        )
        old_properties = parent_schema.properties()

        if PRIMARY_KEYS in old_properties.keys():
            new_pks = filter_primary_keys(
                old_properties[PRIMARY_KEYS],
                new_type,
            )
            old_properties[PRIMARY_KEYS] = new_pks  # type:ignore

        # VERY UGLY SHOULD BE REMOVED WHEN WE HAVE PROTECTED TYPE
        previous_fields = parent_schema.type().children()
        if DATA in previous_fields.keys():
            previous_fields[DATA] = new_type.data_type()
            new_type = sdt.Struct(fields=previous_fields)
        return schema(
            self.dataset,
            schema_type=new_type,
            privacy_unit_tracking_paths=None,
            properties=old_properties,
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


class Filter(StandardDatasetImplementation):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a user_settings transform
    """

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        schema = await self.dataset.manager().async_schema(
            dataset=self.dataset
        )
        parent_schema = await self.parent_schema()

        async def filter_func(batch: pa.RecordBatch) -> pa.Array:
            array = convert_record_batch(
                record_batch=batch, _type=parent_schema.type()
            )
            # VERY UGLY SHOULD BE REMOVED WHEN WE HAVE PROTECTED TYPE
            if DATA in parent_schema.type().children():
                pa_fields = list(array.type)
                old_arrays = array.flatten()
                idx_data = array.type.get_field_index(DATA)
                array = old_arrays[idx_data]
                updated_array, filter_indices = select_rows(
                    schema.data_type(),
                    array,
                )
                pa_fields[idx_data] = pa_fields[idx_data].with_type(
                    updated_array.type
                )
                old_arrays[idx_data] = updated_array
                new_struct = pa.StructArray.from_arrays(
                    old_arrays,
                    fields=pa_fields,
                )
                return new_struct.filter(filter_indices)
            else:
                updated_array, filter_indices = select_rows(
                    schema.data_type(),
                    array,
                )
                return updated_array.filter(filter_indices)

        return await self.ensure_batch_correct(
            await self.parent_to_arrow(batch_size),
            func_to_apply=filter_func,
            batch_size=batch_size,
        )

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        return None

    async def size(self) -> st.Size:
        schema = await self.dataset.manager().async_schema(self.dataset)
        sizes = await self.parent_size()
        new_stats = update_statistics(
            stats=sizes.statistics(), new_type=schema.data_type()
        )
        return size_builder(dataset=self.dataset, statistics=new_stats)

    async def multiplicity(self) -> st.Multiplicity:
        schema = await self.dataset.manager().async_schema(self.dataset)
        multiplicities = await self.parent_multiplicity()
        new_stats = update_statistics(
            stats=multiplicities.statistics(), new_type=schema.data_type()
        )
        return multiplicity_builder(dataset=self.dataset, statistics=new_stats)

    async def bounds(self) -> st.Bounds:
        schema = await self.dataset.manager().async_schema(self.dataset)
        bounds = await self.parent_bounds()
        new_stats = update_statistics(
            stats=bounds.statistics(), new_type=schema.data_type()
        )
        return bounds_builder(dataset=self.dataset, statistics=new_stats)

    async def marginals(self) -> st.Marginals:
        schema = await self.dataset.manager().async_schema(self.dataset)
        marginals = await self.parent_marginals()
        new_stats = update_statistics(
            stats=marginals.statistics(), new_type=schema.data_type()
        )
        return marg_builder(dataset=self.dataset, statistics=new_stats)


def update_statistics(
    stats: st.Statistics, new_type: st.Type
) -> st.Statistics:
    """Visitor to update recursively the stats object via the new_type.
    Sub_statistics whose corresponding type is absent in new_type are removed.
    """

    class Updater(st.StatisticsVisitor):
        result = stats

        def Struct(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # filter does not affect structs
            children_type = new_type.children()
            new_struct = sds.Struct(
                fields={
                    fieldname: update_statistics(
                        fieldstat, children_type[fieldname]
                    )
                    for fieldname, fieldstat in self.result.children().items()
                },
                size=size,
                multiplicity=multiplicity,
                name=name,
                properties=self.result.properties(),
            )
            self.result = new_struct

        def Union(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            children_type = new_type.children()
            children_stat = self.result.children()
            new_fields = {
                fieldname: update_statistics(
                    children_stat[fieldname], fieldtype
                )
                for fieldname, fieldtype in children_type.items()
            }
            self.result = sds.Union(
                fields=new_fields,
                size=size,
                multiplicity=multiplicity,
                name=name if name is not None else "Union",
                properties=self.result.properties(),
            )

        def Optional(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            self.result = sds.Optional(
                statistics=update_statistics(
                    self.result.children()[OPTIONAL_VALUE],
                    new_type.children()[OPTIONAL_VALUE],
                ),
                size=size,
                multiplicity=multiplicity,
                properties=self.result.properties(),
            )

        def Null(self, size: int, multiplicity: float) -> None:
            pass

        def Unit(self, size: int, multiplicity: float) -> None:
            pass

        def Boolean(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[bool]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Id(self, size: int, multiplicity: float) -> None:
            pass

        def Integer(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[str]] = None,
            values: t.Optional[t.List[float]] = None,
            name: str = "Enum",
        ) -> None:
            pass

        def Float(
            self,
            size: int,
            multiplicity: float,
            min_value: float,
            max_value: float,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[float]] = None,
        ) -> None:
            pass

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
            pass

        def Bytes(self, size: int, multiplicity: float) -> None:
            pass

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
            pass

        def Date(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Time(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Constrained(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            raise NotImplementedError

    visitor = Updater()
    stats.accept(visitor)
    return visitor.result
