from typing import AsyncIterator, List, Union
import typing as t
import warnings

import numpy as np
import pyarrow as pa
import gc

from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATA
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.async_utils import async_iter
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
    from sarus_data_spec.sarus_statistics.tasks.size.sample_visitor import (
        sampled_size,
    )
except ModuleNotFoundError as exception:
    # for the public repo
    if "sarus_data_spec.sarus_statistics" in str(exception.name):
        pass
    else:
        raise exception

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


class SampleStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            privacy_unit_tracking_paths=parent_schema.protobuf().privacy_unit,
            properties=parent_schema.properties(),
            name=parent_schema.name(),
        )


class Sample(StandardDatasetImplementation):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a sample transform
    """

    async def size(self) -> st.Size:
        parent_size = await self.parent_size()
        size_ratio = new_sampling_ratio(self.dataset, parent_size.statistics())
        if size_ratio >= 1:
            return parent_size
        return size_builder(
            self.dataset, sampled_size(parent_size.statistics(), size_ratio)
        )

    async def multiplicity(self) -> st.Multiplicity:
        parent_multiplicity = await self.parent_multiplicity()
        return multiplicity_builder(
            self.dataset, parent_multiplicity.statistics()
        )

    async def bounds(self) -> st.Bounds:
        parent_bounds = await self.parent_bounds()
        size_ratio = new_sampling_ratio(
            self.dataset, parent_bounds.statistics()
        )
        if size_ratio >= 1:
            return parent_bounds
        return bounds_builder(
            self.dataset, sampled_size(parent_bounds.statistics(), size_ratio)
        )

    async def marginals(self) -> st.Marginals:
        parent_marginals = await self.parent_marginals()
        size_ratio = new_sampling_ratio(
            self.dataset, parent_marginals.statistics()
        )
        if size_ratio >= 1:
            return parent_marginals
        return marginals_builder(
            self.dataset,
            sampled_size(parent_marginals.statistics(), size_ratio),
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
        return await sample_arrow_to_arrow(self, batch_size)

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        schema = await self.dataset.async_schema()
        parent_ds = t.cast(Dataset, self.parent())
        sample_spec = getattr(
            self.dataset.transform().protobuf().spec,
            self.dataset.transform().protobuf().spec.WhichOneof("spec"),  # type: ignore[arg-type]
        )

        previous_size = await parent_ds.manager().async_size(parent_ds)
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
            if sample_spec.HasField("fraction"):
                fraction = sample_spec.fraction
                sample_query = sa.select(sa_table).where(
                    sa.func.random() < fraction
                )
            else:
                sample_query = (
                    sa.select(sa_table)
                    .order_by(sa.func.random())
                    .limit(
                        int(
                            sample_spec.size
                            * previous_stats.nodes_statistics(table_path)[
                                0
                            ].size()
                            / previous_stats.size()
                        )
                    )
                )

            queries[tuple(full_tablename)] = sqlalchemy_query_to_string(
                sample_query
            )
        return queries


def fast_gather(
    indices: Union[List[int], np.ndarray],
    batches: List[pa.RecordBatch],
    batch_size: int,
) -> AsyncIterator[pa.RecordBatch]:
    """
    A simple approach based on PyArrow's Table.take().
    """
    assert len(indices), "Indices must be non-empty"
    table = pa.Table.from_batches(batches, schema=batches[0].schema)
    return async_iter(table.take(indices).to_batches(max_chunksize=batch_size))


def new_sampling_ratio(
    dataset: st.Dataset, statistics: st.Statistics
) -> float:
    """From a transformed dataset which last transform is sample or
    differentiated_sample, get sampling ratio"""
    spec = dataset.transform().protobuf().spec
    transform_type = spec.WhichOneof("spec")
    assert transform_type
    sampling_spec = getattr(spec, transform_type)
    if sampling_spec.HasField("fraction"):
        return t.cast(float, sampling_spec.fraction)
    return t.cast(float, sampling_spec.size / statistics.size())


async def sample_arrow_to_arrow(
    op: StandardDatasetImplementation, batch_size: int
) -> t.AsyncIterator[pa.RecordBatch]:
    spec = op.dataset.transform().protobuf().spec
    transform_type = spec.WhichOneof("spec")
    assert transform_type
    sampling_spec = getattr(spec, transform_type)
    seed = Scalar(sampling_spec.seed).value()
    generator = np.random.default_rng(seed)
    parent_batches = [batch async for batch in await op.parent_to_arrow()]
    parent_table = pa.Table.from_batches(parent_batches)

    if sampling_spec.HasField("fraction"):
        new_size = int(sampling_spec.fraction * parent_table.num_rows)
    else:
        new_size = sampling_spec.size

    parent_size = await op.parent_size()
    if new_size >= parent_size.statistics().size():
        del parent_batches, parent_table
        gc.collect()
        return await op.parent_to_arrow(batch_size)

    # TODO: we take the min of new_size, parent_table.num_rows
    # to avoid errors when the DP size is bigger than the actual
    # one but this is not DP actual
    indices = generator.choice(
        parent_table.num_rows,
        replace=False,
        size=min(new_size, parent_table.num_rows),
    )
    return fast_gather(
        indices=indices,
        batches=parent_table.to_batches(max_chunksize=1000),
        batch_size=batch_size,
    )
