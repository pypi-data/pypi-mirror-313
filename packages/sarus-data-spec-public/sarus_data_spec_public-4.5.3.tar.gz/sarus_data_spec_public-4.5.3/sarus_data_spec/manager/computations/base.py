from __future__ import annotations

import asyncio
import logging
import traceback
import typing as t

from sarus_data_spec.constants import PROCESSING_INFO
from sarus_data_spec.manager.base import Base
from sarus_data_spec.manager.typing import Computation
from sarus_data_spec.status import status_error_policy
import sarus_data_spec.status as stt
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)
T = t.TypeVar("T")


class BaseComputation(Computation[T]):
    """General class that implements some
    methods of the protocol shared by all task
    computations"""

    task_name = ""

    def __init__(self, computing_manager: Base):
        self._computing_manager = computing_manager

    def computing_manager(self) -> Base:
        return self._computing_manager

    def status(self, dataspec: st.DataSpec) -> t.Optional[st.Status]:
        return self.computing_manager().status(dataspec, self.task_name)

    def launch_task(self, dataspec: st.DataSpec) -> t.Optional[t.Awaitable]:
        """Launch the task computation.

        Returns an optional awaitable that can be used in async functions to
        wait for the task to complete. This can be useful if some managers have
        a more efficient way than statuses to await for the result.
        """
        raise NotImplementedError

    async def task_result(self, dataspec: st.DataSpec, **kwargs: t.Any) -> T:
        """Return the task result.

        This is the main entry point from outide the computation. The call to
        `complete_task` will launch the task if it does not exist and wait for
        it to be ready.

        Here, we assert that the task is ready and then get the result in a
        try/catch block.
        """
        status = await self.complete_task(dataspec=dataspec)
        stage = status.task(self.task_name)
        assert stage
        assert stage.ready()
        try:
            return await self.result_from_stage_properties(
                dataspec, stage.properties(), **kwargs
            )
        except stt.DataSpecErrorStatus as exception:
            stt.error(
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
            stt.error(
                dataspec=dataspec,
                manager=self.computing_manager(),
                task=self.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(False),
                },
            )
            raise stt.DataSpecErrorStatus((False, traceback.format_exc()))

    async def result_from_stage_properties(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> T:
        """Return the task result by reading cache or computing the value."""
        raise NotImplementedError

    async def complete_task(self, dataspec: st.DataSpec) -> st.Status:
        """Poll the last status for the given task and if no status
        is available either performs the computation or delegates it
        to another manager. Then keeps polling until either the task
        is completed or an error occurs."""

        manager_status = self.status(dataspec)

        if manager_status is None:
            task = self.launch_task(dataspec=dataspec)
            if task is not None:
                # NB: an exception raised in an asyncio task will be reraised
                # in the awaiting code
                await task
            # In the other cases, the complete_task will be reentered with
            # the pending status, resulting in a polling process
            return await self.complete_task(dataspec)

        else:
            last_task = t.cast(st.Stage, manager_status.task(self.task_name))
            if last_task.ready():
                return manager_status
            elif last_task.pending():
                return await self.pending(dataspec)
            elif last_task.processing():
                return await self.processing(dataspec)
            elif last_task.error():
                return await self.error(dataspec)
            else:
                raise ValueError(f"Inconsistent status {manager_status}")

    async def pending(self, dataspec: st.DataSpec) -> st.Status:
        """The behaviour depends on the manager"""
        raise NotImplementedError

    async def processing(self, dataspec: st.DataSpec) -> st.Status:
        """The behaviour depends on the manager"""
        raise NotImplementedError

    async def error(
        self,
        dataspec: st.DataSpec,
    ) -> st.Status:
        """The DataSpec already has an Error status.
        In this case, we clear the statuses so that the
        task can be relaunched in the future.
        """
        status = self.status(dataspec)
        if status is not None:
            stage = status.task(self.task_name)
            assert stage
            should_clear = status_error_policy(stage=stage)
            if should_clear:
                status.clear_task(self.task_name)
                return await self.complete_task(dataspec=dataspec)
            raise stt.DataSpecErrorStatus(
                (
                    stage.properties()["relaunch"] == str(True),
                    stage.properties()["message"],
                )
            )
        return await self.complete_task(dataspec=dataspec)

    async def wait_for_computation(
        self,
        dataspec: st.DataSpec,
        current_stage: str,
        timeout: int = 300,
        max_delay: int = 10,
    ) -> st.Stage:
        """Utility to wait for the availability of a computation, by polling
        its status for at most `timeout` seconds, with a period of at most
        `max_delay` seconds between each attempt. Delay grows exponentially
        at first."""
        delay = min(1, timeout, max_delay)
        total_wait = 0
        while total_wait < timeout:
            status = self.status(dataspec=dataspec)
            assert status
            stage = status.task(self.task_name)
            assert stage
            if stage.processing() and PROCESSING_INFO in stage.properties():
                max_info_length = 100
                print(max_info_length * " ", end="\r")  # clear line
                print(stage[PROCESSING_INFO][:max_info_length], end="\r")
            if stage.stage() == current_stage:
                logger.info(f"POLLING {self.task_name} {dataspec.uuid()}")
                await asyncio.sleep(delay)
                total_wait += delay
                delay = min(2 * delay, max_delay, timeout - total_wait)
            else:
                break
        assert stage
        return stage

    def force_launch(self, dataspec: st.DataSpec) -> None:
        """Method to force launch when an existing
        status with relaunch=true exists. it creates
        a new status without the task in question
        and calls launch task"""
        status = self.status(dataspec=dataspec)
        if status is not None:
            stage = status.task(self.task_name)
            assert stage
            if stage.error() and status_error_policy(stage=stage):
                status.clear_task(self.task_name)
        self.launch_task(dataspec=dataspec)


class ErrorCatchingAsyncIterator:
    """Wrap an AsyncIterator and catches potential errors.

    When an error occurs, this sets the Dataspec status to error
    accordingly.
    """

    def __init__(
        self,
        ait: t.AsyncIterator,
        dataspec: st.DataSpec,
        computation: BaseComputation,
    ):
        self.ait: t.AsyncIterator = ait
        self.computation = computation
        self.dataspec = dataspec
        self.agen: t.Optional[t.AsyncIterator] = None

    def __aiter__(self) -> t.AsyncIterator:
        return self.ait

    async def __anext__(self) -> t.Any:
        try:
            batch = await self.ait.__anext__()
        except StopAsyncIteration:
            raise
        except stt.DataSpecErrorStatus as exception:
            stt.error(
                dataspec=self.dataspec,
                manager=self.computation.computing_manager(),
                task=self.computation.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(exception.relaunch),
                },
            )
            raise
        except Exception:
            stt.error(
                dataspec=self.dataspec,
                manager=self.computation.computing_manager(),
                task=self.computation.task_name,
                properties={
                    "message": traceback.format_exc(),
                    "relaunch": str(False),
                },
            )
            raise stt.DataSpecErrorStatus((False, traceback.format_exc()))

        else:
            return batch
