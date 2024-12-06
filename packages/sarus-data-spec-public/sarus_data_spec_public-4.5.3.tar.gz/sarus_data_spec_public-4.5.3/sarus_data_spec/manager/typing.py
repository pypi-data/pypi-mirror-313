from __future__ import annotations

from typing import (
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Protocol,
    Tuple,
    runtime_checkable,
)
import typing as t

import pandas as pd
import pyarrow as pa

try:
    import tensorflow as tf
except ModuleNotFoundError:
    pass  # Warning is displayed by typing.py

import warnings

from sarus_data_spec.storage.typing import HasStorage
import sarus_data_spec.dataspec_rewriter.typing as sdrt
import sarus_data_spec.dataspec_validator.typing as sdvt
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

try:
    import sqlalchemy as sa

    sa_engine = sa.engine.Engine
except ModuleNotFoundError:
    warnings.warn("Sqlalchemy not installed, cannot send sql queries")
    sa_engine = t.Any  # type: ignore


@runtime_checkable
class Manager(st.Referrable[sp.Manager], HasStorage, Protocol):
    """Provide the dataset functionalities"""

    def to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.Iterator[pa.RecordBatch]:
        """Synchronous method based on async_to_arrow
        that returns an iterator of arrow batches
        for the input dataset"""
        ...

    async def async_to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> AsyncIterator[pa.RecordBatch]:
        """Asynchronous method. It orchestrates how
        the iterator is obtained: it can either be delegated
        via arrow_task and the result polled, or computed directly
        it via the op"""
        ...

    def schema(self, dataset: st.Dataset) -> st.Schema:
        """Synchronous method that returns the schema of a
        dataspec. Based on the asynchronous version"""
        ...

    async def async_schema(self, dataset: st.Dataset) -> st.Schema:
        """Asynchronous method that returns the schema of a
        dataspec. The computation can be either delegated to
        another manager via schema_task and the result polled
        or executed directly via async_schema_ops"""
        ...

    def value(self, scalar: st.Scalar) -> st.DataSpecValue:
        """Synchronous method that returns the value of a
        scalar. Based on the asynchronous version"""
        ...

    async def async_value(self, scalar: st.Scalar) -> st.DataSpecValue:
        """Asynchronous method that returns the value of a
        scalar. The computation can be either delegated to
        another manager via value_task and the result polled
        or executed directly via async_value_ops"""
        ...

    def prepare(self, dataspec: st.DataSpec) -> None:
        """Make sure a Dataspec is ready."""
        ...

    async def async_prepare(self, dataspec: st.DataSpec) -> None:
        """Make sure a Dataspec is ready asynchronously."""
        ...

    async def async_prepare_parents(self, dataspec: st.DataSpec) -> None:
        """Prepare all the parents of a Dataspec."""
        ...

    def sql_prepare(self, dataset: st.Dataset) -> None:
        """Make sure a dataset is sql ready"""
        ...

    async def async_sql_prepare(self, dataset: st.Dataset) -> None:
        """Make sure a dataset is sql ready asynchronously."""
        ...

    async def async_sql_prepare_parents(self, dataset: st.Dataset) -> None:
        """SQL prepare all the parents of a dataset. It should sql_prepare
        dataset parents and prepare Scalars parents.
        """
        ...

    def cache_scalar(self, scalar: st.Scalar) -> None:
        """Synchronous scalar caching"""
        ...

    async def async_cache_scalar(self, scalar: st.Scalar) -> None:
        """Asynchronous scalar caching"""
        ...

    def to_parquet(self, dataset: st.Dataset) -> None:
        """Synchronous parquet caching"""
        ...

    async def async_to_parquet(self, dataset: st.Dataset) -> None:
        """Asynchronous parquet caching"""
        ...

    def parquet_dir(self) -> str: ...

    def marginals(self, dataset: st.Dataset) -> st.Marginals: ...

    async def async_marginals(self, dataset: st.Dataset) -> st.Marginals: ...

    def bounds(self, dataset: st.Dataset) -> st.Bounds: ...

    async def async_bounds(self, dataset: st.Dataset) -> st.Bounds: ...

    def size(self, dataset: st.Dataset) -> st.Size: ...

    async def async_size(self, dataset: st.Dataset) -> st.Size: ...

    def multiplicity(self, dataset: st.Dataset) -> st.Multiplicity: ...

    async def async_multiplicity(
        self, dataset: st.Dataset
    ) -> st.Multiplicity: ...

    def to_pandas(self, dataset: st.Dataset) -> pd.DataFrame: ...

    async def async_to_pandas(self, dataset: st.Dataset) -> pd.DataFrame: ...

    async def async_to(
        self,
        dataset: st.Dataset,
        kind: t.Type,
        drop_admin: bool = True,
        batch_size: t.Optional[int] = None,
    ) -> st.DatasetCastable:
        """Casts a Dataset to a Python type passed as argument."""
        ...

    def to(
        self, dataset: st.Dataset, kind: t.Type, drop_admin: bool = True
    ) -> st.DatasetCastable: ...

    def to_tensorflow(self, dataset: st.Dataset) -> tf.data.Dataset: ...

    async def async_to_tensorflow(
        self, dataset: st.Dataset
    ) -> tf.data.Dataset: ...

    def to_sql(self, dataset: st.Dataset) -> None: ...

    def push_sql(self, dataset: st.Dataset) -> None: ...

    async def async_to_sql(self, dataset: st.Dataset) -> None: ...

    async def async_push_sql(self, dataset: st.Dataset) -> None: ...

    def status(
        self, dataspec: st.DataSpec, task_name: t.Optional[str] = None
    ) -> t.Optional[st.Status]: ...

    def dataspec_rewriter(self) -> sdrt.DataspecRewriter: ...

    def dataspec_validator(self) -> sdvt.DataspecValidator: ...

    def is_remote(self, dataspec: st.DataSpec) -> bool:
        """Is the dataspec a remotely defined dataset."""
        ...

    def infer_dataset_or_scalar(
        self,
        transform: st.Transform,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> Tuple[str, Callable[[st.DataSpec], None]]: ...

    def foreign_keys(self, dataset: st.Dataset) -> Dict[st.Path, st.Path]: ...

    async def async_foreign_keys(
        self, dataset: st.Dataset
    ) -> Dict[st.Path, st.Path]: ...

    async def async_primary_keys(
        self, dataset: st.Dataset
    ) -> List[st.Path]: ...

    def primary_keys(self, dataset: st.Dataset) -> List[st.Path]: ...

    def sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> Iterator[pa.RecordBatch]: ...

    async def async_sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, st.NestedQueryDict],
        dialect: Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> AsyncIterator[pa.RecordBatch]: ...

    async def execute_sql_query(
        self,
        dataset: st.Dataset,
        caching_properties: t.Mapping[str, str],
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]: ...

    async def async_sql_op(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]: ...

    def is_big_data(self, dataset: st.DataSpec) -> bool: ...

    def caches(self) -> t.Any: ...

    def is_cached(self, dataspec: st.DataSpec) -> bool:
        """Returns whether a dataspec should be cached
        or not"""
        ...

    def is_cached_to_sql(self, dataspec: st.DataSpec) -> bool:
        """Returns whether a dataspec should be pushed to sql
        or not"""
        ...

    def attribute(
        self, name: str, dataspec: st.DataSpec
    ) -> t.Optional[st.Attribute]: ...

    def attributes(
        self, name: str, dataspec: st.DataSpec
    ) -> t.List[st.Attribute]: ...

    def links(self, dataset: st.Dataset) -> st.Links: ...

    async def async_links(self, dataset: st.Dataset) -> st.Links: ...

    def sql_pushing_schema_prefix(self, dataset: st.Dataset) -> str: ...

    def engine(self, uri: str) -> sa_engine: ...

    def mock_value(
        self,
        transform: st.Transform,
        *arguments: st.DataSpec,
        **named_arguments: st.DataSpec,
    ) -> t.Any:
        """Compute the mock value of an external transform applied on
        Dataspecs.
        """

    def composed_callable(
        self, transform: st.Transform
    ) -> t.Callable[..., t.Any]:
        """Return a Python callable of a composed transform."""

    def launch_job(
        self, command: t.List[str], env: t.Dict[str, str]
    ) -> None: ...

    def python_type(self, dataspec: st.DataSpec) -> str: ...


@runtime_checkable
class HasManager(Protocol):
    """Has a manager."""

    def manager(self) -> Manager:
        """Return a manager (usually a singleton)."""
        ...


T = t.TypeVar("T", covariant=True)


@runtime_checkable
class Computation(t.Protocol[T]):
    """Protocol for classes that perform tasks computations.
    It sets how computations are scheduled and launched
    depending on statuses. A computation is mainly defined by two methods:
     - launch : a method that does not return a value but
     that only has side effects, changing either the storage or the cache
    and that updates statuses during the process
    - result: a method that allows to get the value of the computation
    either by reading the cache/storage or via the ops.

    Furthermore, a computation has a method to monitor task completion.
    """

    task_name: str = ""

    def launch_task(self, dataspec: st.DataSpec) -> t.Optional[t.Awaitable]:
        """This methods launches a task in the background
        but returns immediately without waiting for the
        result. It updates the statuses during its process."""
        ...

    async def task_result(self, dataspec: st.DataSpec, **kwargs: t.Any) -> T:
        """Returns the value for the given computed task. It either
        retrieves it from the cache or computes it via the ops."""
        ...

    async def complete_task(self, dataspec: st.DataSpec) -> st.Status:
        """Monitors a task: it launches it if there is no status
        and then polls until it is ready/error"""
        ...
