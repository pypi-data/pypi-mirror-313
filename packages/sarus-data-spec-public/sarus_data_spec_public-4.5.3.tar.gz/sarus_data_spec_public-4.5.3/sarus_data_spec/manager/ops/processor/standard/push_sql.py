import typing as t

import pyarrow as pa

from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)
from sarus_data_spec.schema import schema
import sarus_data_spec.typing as st


class PushSQLStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            privacy_unit_tracking_paths=None,
            properties=parent_schema.properties(),
            name=parent_schema.name(),
        )


class PushSQL(StandardDatasetImplementation):
    """Computes schema and arrow
    batches for a dataspec transformed by
    an push sql transform. It is used to push the data of the parents in a
    sql database.
    """

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return await self.parent_to_arrow(batch_size=batch_size)

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        """pass query to parents"""
        return None
