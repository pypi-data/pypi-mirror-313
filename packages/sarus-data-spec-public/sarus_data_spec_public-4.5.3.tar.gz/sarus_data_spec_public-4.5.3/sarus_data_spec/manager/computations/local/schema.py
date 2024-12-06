import logging
import time
import traceback
import typing as t

from sarus_data_spec import typing as st
from sarus_data_spec.constants import SCHEMA_TASK
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.cache_utils import lru_caching
from sarus_data_spec.manager.computations.local.base import LocalComputation
from sarus_data_spec.schema import Schema
from sarus_data_spec.status import DataSpecErrorStatus, error, ready

logger = logging.getLogger(__name__)


class SchemaComputation(LocalComputation[st.Schema]):
    """Class responsible to compute schemas"""

    task_name = SCHEMA_TASK

    async def prepare(self, dataspec: st.DataSpec) -> None:
        try:
            logger.info(f"STARTED SCHEMA {dataspec.uuid()}")
            start = time.perf_counter()
            schema = await self.computing_manager().async_schema_op(
                dataset=t.cast(Dataset, dataspec)
            )

        except DataSpecErrorStatus as exception:
            error(
                dataspec=dataspec,
                manager=self.computing_manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(exception.relaunch),
                },
            )
            raise
        except Exception:
            error(
                dataspec=dataspec,
                manager=self.computing_manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(False),
                },
            )
            raise DataSpecErrorStatus((False, traceback.format_exc()))
        else:
            end = time.perf_counter()
            logger.info(
                f"FINISHED SCHEMA {dataspec.uuid()} ({end-start:.2f}s)"
            )
            ready(
                dataspec=dataspec,
                manager=self.computing_manager(),
                task=self.task_name,
                properties={"uuid": schema.uuid()},
            )

    async def result_from_stage_properties(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> st.Schema:
        return t.cast(
            Schema,
            dataspec.storage().referrable(properties["uuid"]),
        )

    @lru_caching("computation", use_first_arg=True)
    async def task_result(
        self, dataspec: st.DataSpec, **kwargs: t.Any
    ) -> st.Schema:
        return await super().task_result(dataspec, **kwargs)
