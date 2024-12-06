from __future__ import annotations

import shutil
import typing as t
import warnings
import logging
import pyarrow as pa
from sarus_data_spec.arrow.type import to_arrow
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import (
    SYNTHETIC_MODEL,
    SYNTHETIC_TASK,
    DATA,
)
from pydantic import RootModel

import sarus_data_spec.type as sdt
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.marginals import marginals as marginals_builder
from sarus_data_spec.multiplicity import multiplicity as multiplicity_builder
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.typing as st

try:
    from sarus_synthetic_data.generator import SyntheticDatasetGenerator
    from sarus_synthetic_data.configs.global_config import (
        SyntheticConfig,
        TrigramsColumn,
    )
except ModuleNotFoundError:
    warnings.warn("Synthetic Data not available")

from .config_updates import update_config

try:
    from sarus_data_spec.manager.ops.source.query_builder import (
        synthetic_parameters,
    )
except ModuleNotFoundError:
    warnings.warn(
        "synthetic_parameters not found, "
        "synthetic data operations not available "
    )
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema
from sarus_data_spec.path import straight_path
from sarus_data_spec.manager.ops.processor.standard.standard_op import (
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
    StandardScalarImplementation,
    StandardScalarStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.select_table import (
    select_table,
)
from sarus_data_spec.arrow.array import convert_record_batch
import os
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)


def convert_array_to_table(
    schema_type: st.Type, arrow_data: pa.array
) -> pa.Array:
    """Given a PyArrow array, returns a correctly-defined Table."""

    class ArrayToTable(sdt.TypeVisitor):
        """Handles both configuration: a dataset as a Struct or as an Union."""

        result = None

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            names = list(fields.keys())
            self.result = pa.Table.from_arrays(
                arrays=arrow_data.flatten(), names=names
            )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            names = list(fields.keys())
            arrs = arrow_data.flatten()
            schema = pa.schema(
                [
                    pa.field(name, type=arr.type)
                    for arr, name in zip(arrs[:-1], names)
                ]
            )
            schema = schema.append(
                pa.field(
                    "field_selected", type=pa.large_string(), nullable=False
                )
            )
            self.result = pa.Table.from_arrays(
                arrays=arrow_data.flatten(), schema=schema
            )

    visitor = ArrayToTable()
    schema_type.accept(visitor)
    return visitor.result


async def async_iter_arrow(
    iterator: t.Iterator[pa.RecordBatch],
) -> t.AsyncIterator[pa.RecordBatch]:
    """Async generator from the synthetic data iterator."""
    for batch in iterator:
        yield batch
    return


class SyntheticStaticChecker(StandardDatasetStaticChecker):
    def pup_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        # TODO add pup token when the synthetic data is actually protected
        return None

    def rewritten_pup_token(
        self, public_context: t.Collection[str]
    ) -> t.Optional[str]:
        # TODO add pup token when the synthetic data is actually protected
        return None

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.data_type(),
            properties=parent_schema.properties(),
            name=parent_schema.name(),
        )


class Synthetic(StandardDatasetImplementation):
    """Create a Synthetic op class for is_pup."""

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        dataset = self.dataset
        parents, parents_dict = dataset.parents()

        # Forcing the marginals to be computed first
        parent = t.cast(Dataset, parents[0])
        marginals = await parent.manager().async_marginals(parent)
        schema = await parent.manager().async_schema(parent)
        parent_stats = marginals.statistics()

        # Budget
        budget_param = parents_dict["sd_budget"]
        budget = t.cast(
            t.Tuple[float, float],
            await dataset.manager().async_value(t.cast(Scalar, budget_param)),
        )

        # Model
        model_properties = t.cast(Scalar, parents_dict["synthetic_model"])
        synthetic_config = t.cast(
            SyntheticConfig,
            await dataset.manager().async_value(model_properties),
        )

        # Update SyntheticConfig with Calibrated Noise
        config_with_noise = await synthetic_parameters(
            dataset,
            sd_budget=budget,
            task=SYNTHETIC_TASK,
            synthetic_config=synthetic_config,
        )
        # Links computation
        links = await self.dataset.manager().async_links(self.dataset)
        # Update SyntheticConfig with saving_dir, Distributions,Sampling size,links
        synthetic_data_dir = os.path.join(
            self.dataset.manager().parquet_dir(),
            self.dataset.uuid(),
            "synthetic_data",
        )
        os.makedirs(synthetic_data_dir, exist_ok=True)
        final_config = update_config(
            config_with_noise,
            synthetic_data_dir,
            parent_stats,
            links.links_statistics(),
        )

        temp_preprocess_uri = os.path.join(synthetic_data_dir, "preprocessing")
        os.makedirs(temp_preprocess_uri, exist_ok=True)
        await self.save_data_for_synthetic_training(
            final_config, temp_preprocess_uri, parent, schema
        )
        generator = SyntheticDatasetGenerator(final_config)
        dataset_schema = await dataset.manager().async_schema(dataset)
        datatype = dataset_schema.type()
        generator.train()
        sample_dict = generator.sample()
        shutil.rmtree(temp_preprocess_uri)
        sample = consolidate_samples(sample_dict, datatype, (), parent_stats)
        table = convert_array_to_table(datatype, sample)
        return async_iter_arrow(table.to_batches(max_chunksize=batch_size))

    async def save_data_for_synthetic_training(
        self,
        final_config: SyntheticConfig,
        temp_preprocess_uri: str,
        parent: st.Dataset,
        schema: st.Schema,
    ) -> None:
        # save data per table for tables that require either correlation training
        # or trigrams training or are public
        tables_with_correlation_or_trigrams_or_public: t.Dict[
            t.Tuple[str, ...], t.List[pa.RecordBatch]
        ] = {
            table_name: []
            for table_name, table_config in final_config.tables.items()
            if table_config.correlation_generation is not None
            or table_config.is_public
            or (
                table_config.independent_generation is not None
                and any(
                    isinstance(config, TrigramsColumn)
                    for config in table_config.independent_generation.columns.values()
                )
            )
        }
        if len(tables_with_correlation_or_trigrams_or_public) > 0:
            async for batch in await parent.async_to_arrow():
                array = convert_record_batch(
                    record_batch=batch, _type=schema.type()
                )
                old_arrays = array.flatten()
                idx_data = array.type.get_field_index(DATA)
                array = old_arrays[idx_data]
                for (
                    table_name
                ) in tables_with_correlation_or_trigrams_or_public.keys():
                    table_path = straight_path([DATA, *table_name])
                    updated_array, filter_indices = select_table(
                        _type=schema.data_type(),
                        array=array,
                        path=table_path,
                    )
                    old_arrays[idx_data] = updated_array
                    new_struct = pa.StructArray.from_arrays(
                        old_arrays,
                        names=list(schema.type().children().keys()),
                    )
                    tables_with_correlation_or_trigrams_or_public[
                        table_name
                    ].append(
                        pa.record_batch(new_struct.filter(filter_indices))
                    )
            for (
                table_name,
                table_list,
            ) in tables_with_correlation_or_trigrams_or_public.items():
                table = pa.Table.from_batches(table_list)
                table = table.flatten()
                table = table.rename_columns(
                    [el.removeprefix(DATA + ".") for el in table.column_names]
                )
                data_uri = os.path.join(
                    temp_preprocess_uri, str(table_name) + ".parquet"
                )
                final_config.tables[table_name].data_uri = data_uri
                pq.write_table(table, version="2.6", where=data_uri)

    async def size(self) -> st.Size:
        parent_size = await self.parent_size()
        return size_builder(self.dataset, parent_size.statistics())

    async def multiplicity(self) -> st.Multiplicity:
        parent_multiplicity = await self.parent_multiplicity()
        return multiplicity_builder(
            self.dataset, parent_multiplicity.statistics()
        )

    async def bounds(self) -> st.Bounds:
        parent_bounds = await self.parent_bounds()
        return bounds_builder(self.dataset, parent_bounds.statistics())

    async def marginals(self) -> st.Marginals:
        parent_marginals = await self.parent_marginals()
        return marginals_builder(self.dataset, parent_marginals.statistics())


class SyntheticModelStaticChecker(StandardScalarStaticChecker): ...


class SyntheticModel(StandardScalarImplementation):
    """Computes the synthetic model to use"""

    async def value(self) -> t.Any:
        attribute = self.scalar.attribute(name=SYNTHETIC_MODEL)
        assert attribute is not None, "No attribute value for synthetic model"
        return (
            RootModel[SyntheticConfig]
            .model_validate_json(attribute.properties()["config"])
            .root
        )


def consolidate_samples(
    batch_data: t.Dict[t.Tuple[str, ...], pa.Table],
    data_type: st.Type,
    curr_path: t.Tuple[str, ...],
    statistics: st.Statistics,
) -> pa.Array:
    """Visitor to put back together the sampled tables
    in the general schema (union or directly struct)"""

    class ConsolidatorVisitor(sdt.TypeVisitor):
        result = None

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            arrays = []
            child_stats = statistics.children()
            for field_name, field_type in fields.items():
                arrays.append(
                    consolidate_samples(
                        batch_data,
                        data_type=field_type,
                        curr_path=(*curr_path, field_name),
                        statistics=child_stats[field_name],
                    )
                )
            names = list(fields.keys())
            sizes = [
                getattr(
                    stat.protobuf(),
                    t.cast(str, stat.protobuf().WhichOneof("statistics")),
                ).size
                for stat in child_stats.values()
            ]
            pa_fields = [
                pa.field(name=field_name, type=array.type, nullable=True)
                for field_name, array in zip(names, arrays)
            ]
            pa_fields.append(
                pa.field(
                    name="field_selected",
                    type=pa.large_string(),
                    nullable=False,
                )
            )
            structs = []
            for i, array in enumerate(arrays):
                structs.append(
                    pa.concat_arrays(
                        [
                            pa.array([None] * sum(sizes[:i]), type=array.type),
                            array.combine_chunks()
                            if isinstance(array, pa.ChunkedArray)
                            else array,
                            pa.array(
                                sum(sizes[i + 1 :]) * [None], type=array.type
                            ),
                        ]
                    )
                )
            field_selected = pa.array(
                [
                    names[i]
                    for i, length in enumerate(sizes)
                    for _ in range(length)
                ],
                pa.large_string(),
            )
            if isinstance(field_selected, pa.ChunkedArray):
                field_selected = field_selected.combine_chunks()
            structs.append(field_selected)

            self.result = pa.StructArray.from_arrays(structs, fields=pa_fields)

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # check that types are correct with sarus
            new_fields = [
                pa.field(
                    name=field_name,
                    type=to_arrow(fields[field_name]),
                    nullable=fields[field_name].protobuf().HasField("optional")
                    or fields[field_name].protobuf().HasField("unit"),
                )
                for field_name in fields.keys()
            ]

            self.result = pa.StructArray.from_arrays(
                [
                    el.combine_chunks()
                    for el in batch_data[tuple(curr_path)]
                    .select(list(fields.keys()))
                    .columns
                ],
                fields=new_fields,
            )

    visitor = ConsolidatorVisitor()
    data_type.accept(visitor)
    return visitor.result
