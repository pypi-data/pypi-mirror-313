import asyncio
import logging
import typing as t

from sarus_data_spec.manager.computations.base import BaseComputation, T
import sarus_data_spec.status as stt
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class LocalComputation(BaseComputation[T]):
    """Base class for computations that execute
    code locally."""

    async def result_from_stage_properties(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> T:
        raise NotImplementedError

    async def pending(self, dataspec: st.DataSpec) -> st.Status:
        """If a task is pending, it should be computed"""

        task = self.launch_task(dataspec=dataspec)
        if task is not None:
            # NB: an exception raised in an asyncio task will be reraised
            # in the awaiting code
            await task
        # In the other cases, the complete_task will be reentered with
        # the pending status, resulting in a polling process
        return await self.complete_task(dataspec)

    async def processing(self, dataspec: st.DataSpec) -> st.Status:
        """If processing, wait for the task to be ready.
        Such a case can happen if another manager has taken the computation
        of the task. After a given timeout, an error is raised.
        """

        stage = await self.wait_for_computation(
            dataspec=dataspec,
            current_stage="processing",
            timeout=self.computing_manager().computation_timeout(dataspec),
            max_delay=self.computing_manager().computation_max_delay(dataspec),
        )
        if stage.processing():
            stt.error(
                dataspec=dataspec,
                manager=dataspec.manager(),
                task=self.task_name,
                properties={
                    "message": "TimeOutError:Processing time out for task"
                    f" {self.task_name} on dataspec {dataspec}",
                    "relaunch": str(True),
                },
            )
            raise stt.DataSpecErrorStatus(
                (
                    True,
                    "TimeOutError:Processing time out for task"
                    f" {self.task_name} on dataspec {dataspec}",
                )
            )
        # if the stage is an error, it is complete_task
        # that decides what to do via the error_policy
        return await self.complete_task(dataspec)

    def launch_task(self, dataspec: st.DataSpec) -> t.Optional[t.Awaitable]:
        status = self.status(dataspec)
        if status is None:
            _, is_updated = stt.processing(
                dataspec=dataspec,
                manager=self.computing_manager(),
                task=self.task_name,
            )
            if is_updated:
                return asyncio.create_task(
                    self.prepare(dataspec),
                    name=self.task_name + dataspec.uuid(),
                )
        else:
            stage = status.task(self.task_name)
            assert stage
            if stage.pending():
                _, is_updated = stt.processing(
                    dataspec=dataspec,
                    manager=self.computing_manager(),
                    task=self.task_name,
                )
                if is_updated:
                    return asyncio.create_task(
                        self.prepare(dataspec),
                        name=self.task_name + dataspec.uuid(),
                    )
        return None

    async def prepare(self, dataspec: st.DataSpec) -> None:
        """Prepare the computation and set the status accordingly.

        It is up to the computation to define what preparing means. It can be
        computing and caching the data as well as simply checking that the
        parents are themselves ready.
        """
        raise NotImplementedError
