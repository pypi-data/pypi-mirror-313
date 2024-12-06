from __future__ import annotations

from uuid import UUID
import asyncio
import hashlib
import logging
import os
import time
import typing as t
import warnings

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.admin_utils import async_to_arrow_extract_data_only
from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.arrow.conversion import async_cast_arrow_batches
from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.constants import (
    BIG_DATA_TASK,
    BIG_DATA_THRESHOLD,
    DATASET_N_BYTES,
    DATASET_N_LINES,
    IS_BIG_DATA,
    IS_REMOTE,
    THRESHOLD_TYPE,
    SAMPLE_SIZE_N_LINES,
)
from sarus_data_spec.dataspec_rewriter.recursive_rewriter import (
    RecursiveDataspecRewriter,
)
from sarus_data_spec.dataspec_validator.recursive_validator import (
    RecursiveDataspecValidator,
)
from sarus_data_spec.manager.async_utils import sync, sync_iterator
from sarus_data_spec.manager.ops.processor.external.external_op import (  # noqa: E501
    async_compute_external_value,
)
from sarus_data_spec.manager.ops.processor.routing import get_implementation
from sarus_data_spec.manager.typing import Computation
from sarus_data_spec.protobuf.utilities import copy
from sarus_data_spec.protobuf.utilities import json as utilities_json
from sarus_data_spec.schema import Schema
from sarus_data_spec.status import error_aggregation
from sarus_data_spec.transform import transform_id
import sarus_data_spec.dataspec_rewriter.typing as sdrt
import sarus_data_spec.dataspec_validator.typing as sdvt
import sarus_data_spec.manager.typing as manager_typing
import sarus_data_spec.protobuf as sp
import sarus_data_spec.status as stt
import sarus_data_spec.storage.typing as storage_typing
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.bounds import Bounds
    from sarus_data_spec.links import Links
    from sarus_data_spec.marginals import Marginals
    from sarus_data_spec.multiplicity import Multiplicity
    from sarus_data_spec.size import Size

except ModuleNotFoundError:
    pass
try:
    import tensorflow as tf

    from sarus_data_spec.manager.ops.tensorflow.features import (
        deserialize,
        flatten,
        nest,
        serialize,
        to_internal_signature,
    )
    from sarus_data_spec.manager.ops.tensorflow.tensorflow_visitor import (  # noqa: E501
        convert_tensorflow,
    )
except ModuleNotFoundError:
    pass  # error message printed from typing.py
try:
    import sqlalchemy as sa

    sa_engine = sa.engine.Engine
except ModuleNotFoundError:
    warnings.warn("Sqlalchemy not installed, cannot send sql queries")
    sa_engine = t.Any  # type: ignore
from sarus_data_spec.manager.ops.processor.external.external_op import (
    external_implementation,
)

logger = logging.getLogger(__name__)

BATCH_SIZE = 10000


class Base(manager_typing.Manager):
    """Provide the dataset functionalities."""

    def __init__(
        self, storage: storage_typing.Storage, protobuf: sp.Manager
    ) -> None:
        self._protobuf: sp.Manager = copy(protobuf)
        self._freeze()
        self._storage = storage
        self.storage().store(self)
        self._parquet_dir = os.path.expanduser("/tmp/sarus_dataset/")
        os.makedirs(self.parquet_dir(), exist_ok=True)
        self._dataspec_rewriter = RecursiveDataspecRewriter(storage=storage)
        self._dataspec_validator = RecursiveDataspecValidator(storage=storage)

        # To define in subclasses
        self.to_arrow_computation: Computation[t.AsyncIterator[pa.RecordBatch]]
        self.to_parquet_computation: Computation[str]
        self.cache_scalar_computation: Computation[t.Tuple[str, str]]
        self.value_computation: Computation[t.Any]
        self.schema_computation: Computation[st.Schema]

    # --------PROTOBUF METHODS---------
    def protobuf(self) -> sp.Manager:
        return copy(self._protobuf)

    def prototype(self) -> t.Type[sp.Manager]:
        return sp.Manager

    def type_name(self) -> str:
        return sp.type_name(self._protobuf)

    def __repr__(self) -> str:
        return utilities_json(self._protobuf)

    def __getitem__(self, key: str) -> str:
        return t.cast(str, self._protobuf.properties[key])

    def properties(self) -> t.Mapping[str, str]:
        return self.protobuf().properties

    def _checksum(self) -> bytes:
        """Compute an md5 checksum"""
        md5 = hashlib.md5(usedforsecurity=False)
        md5.update(sp.serialize(self._protobuf))
        return md5.digest()

    def _freeze(self) -> None:
        self._protobuf.uuid = ""
        self._frozen_checksum = self._checksum()
        self._protobuf.uuid = UUID(bytes=self._frozen_checksum).hex

    def _frozen(self) -> bool:
        uuid = self._protobuf.uuid
        self._protobuf.uuid = ""
        result = (self._checksum() == self._frozen_checksum) and (
            uuid == UUID(bytes=self._frozen_checksum).hex
        )
        self._protobuf.uuid = uuid
        return result

    def uuid(self) -> str:
        return self._protobuf.uuid

    def referring(
        self, type_name: t.Optional[str] = None
    ) -> t.Collection[st.Referring]:
        return self.storage().referring(self, type_name=type_name)

    def storage(self) -> storage_typing.Storage:
        return self._storage

    def caches(self) -> t.Any:
        raise NotImplementedError

    # -------DATASPEC RELATED------

    def attribute(
        self, name: str, dataspec: st.DataSpec
    ) -> t.Optional[st.Attribute]:
        attributes = t.cast(
            t.Set[st.Attribute],
            self.storage().referring(
                dataspec, type_name=sp.type_name(sp.Attribute)
            ),
        )
        filtered_attributes = [
            element for element in attributes if element.name() == name
        ]

        if len(filtered_attributes) == 0:
            return None

        if len(filtered_attributes) == 1:
            return t.cast(st.Attribute, filtered_attributes[0])

        raise ValueError("There are two attributes with the same name")

    def attributes(
        self, name: str, dataspec: st.DataSpec
    ) -> t.List[st.Attribute]:
        attributes = t.cast(
            t.Set[st.Attribute],
            self.storage().referring(
                dataspec, type_name=sp.type_name(sp.Attribute)
            ),
        )
        return [element for element in attributes if element.name() == name]

    def infer_dataset_or_scalar(
        self,
        transform: st.Transform,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> t.Tuple[str, t.Callable[[st.DataSpec], None]]:
        """Infer the transform output type : minimal type inference.
        The inference is performed by getting the python type first
        then checking if that type is in a Dataset or Scalar"""

        python_type, _ = self.infer_python_type_new_dataspec(
            transform, *arguments, **named_arguments
        )

        # Infer output types
        dataspec_type = (
            sp.type_name(sp.Dataset)
            if python_type
            in [str(el) for el in t.get_args(st.DatasetCastable)]
            else sp.type_name(sp.Scalar)
        )

        def attach_nothing(ds: st.DataSpec) -> None:
            return

        # Return the output type
        return dataspec_type, attach_nothing

    def infer_python_type_new_dataspec(
        self,
        transform: st.Transform,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> t.Tuple[str, bool]:
        """Infers the python type of the output of a transform and
        its arguments/named arguments via the mechanism of the output hint
        if implemented otherwise by executing on the mock and returns the
        type and if it is a hint"""

        hint = None
        try:
            implementation = external_implementation(transform)
            hint = implementation.py_output_hint(
                transform, *arguments, **named_arguments
            )
        except Exception:
            pass
        if hint is not None:
            type_str = hint
            is_hint = True
        else:
            mock_value = self.mock_value(
                transform, *arguments, **named_arguments
            )
            type_str = str(type(mock_value))
            is_hint = False
        return type_str, is_hint

    def is_big_data(self, dataspec: st.DataSpec) -> bool:
        if not dataspec.prototype() == sp.Dataset:
            # scalar could be bigdata in the futur
            return False
        dataset = t.cast(st.Dataset, dataspec)
        # TODO: this should take dataspec as input not only dataset
        status = self.status(dataset, task_name=BIG_DATA_TASK)

        if status is not None:
            # check if big_data_present
            big_data_task = status.task(BIG_DATA_TASK)
            # if yes:return answer
            if (big_data_task is not None) and (
                big_data_task.stage() == "ready"
            ):
                return big_data_task.properties()[IS_BIG_DATA] == str(True)

        if dataset.is_source():
            raise NotImplementedError(
                "Found source dataset without any big data status"
            )
        else:
            if dataset.transform().is_external():
                return False
            parents, named_parents = dataset.parents()
            parents_list = [
                parent for parent in parents if isinstance(parent, st.DataSpec)
            ]
            parents_dict = {
                name: parent
                for name, parent in named_parents.items()
                if isinstance(parent, st.DataSpec)
            }
            ds_args = [
                element
                for element in parents_list
                if element.type_name() == sp.type_name(sp.Dataset)
            ]
            for element in parents_dict.values():
                if element.type_name() == sp.type_name(sp.Dataset):
                    ds_args.append(element)
            if len(ds_args) > 1:
                raise NotImplementedError(
                    "transforms with many dataspecs not supported yet"
                )
            if len(ds_args) == 0:
                return False
            is_parent_big_data = self.is_big_data(ds_args[0])

            if not is_parent_big_data:
                # write status it is not big data
                stt.ready(
                    dataset,
                    task=BIG_DATA_TASK,
                    properties={
                        IS_BIG_DATA: str(False)
                    },  # we do not need to add more info because a
                    # non big_data dataset cannot become big_data
                )
                return False
            else:
                assert len(ds_args) > 0
                # check that the transform does not change
                # the big data status
                (
                    is_big_data,
                    number_lines,
                    number_bytes,
                    threshold_kind,
                ) = check_transform_big_data(
                    dataset.transform(),
                    ds_args[0],  # type:ignore
                    parents_dict,
                )
                status = self.status(ds_args[0], task_name=BIG_DATA_TASK)
                # TODO: there is an error where a status
                # is put with the wrong manager
                if status is None:
                    status = stt.last_status(
                        dataspec=ds_args[0], task=BIG_DATA_TASK
                    )
                assert status
                big_data_threshold = int(
                    status.task(BIG_DATA_TASK).properties()[BIG_DATA_THRESHOLD]  # type:ignore
                )
                sample_size_n_lines = status.task(BIG_DATA_TASK).properties()[  # type:ignore
                    SAMPLE_SIZE_N_LINES
                ]
                # write status
                stt.ready(
                    dataset,
                    task=BIG_DATA_TASK,
                    properties={
                        IS_BIG_DATA: str(is_big_data),
                        BIG_DATA_THRESHOLD: str(big_data_threshold),
                        SAMPLE_SIZE_N_LINES: str(sample_size_n_lines),
                        DATASET_N_LINES: str(number_lines),
                        DATASET_N_BYTES: str(number_bytes),
                        THRESHOLD_TYPE: threshold_kind,
                    },
                )
                return is_big_data

    def status(
        self, dataspec: st.DataSpec, task_name: t.Optional[str] = None
    ) -> t.Optional[st.Status]:
        return stt.last_status(
            dataspec=dataspec,
            manager=self,
            task=task_name,
        )

    def foreign_keys(self, dataset: st.Dataset) -> t.Dict[st.Path, st.Path]:
        return t.cast(
            t.Dict[st.Path, st.Path], sync(self.async_foreign_keys(dataset))
        )

    def primary_keys(self, dataset: st.Dataset) -> t.List[st.Path]:
        return t.cast(t.List[st.Path], sync(self.async_primary_keys(dataset)))

    async def async_primary_keys(self, dataset: st.Dataset) -> t.List[st.Path]:
        raise NotImplementedError

    async def async_foreign_keys(
        self, dataset: st.Dataset
    ) -> t.Dict[st.Path, st.Path]:
        raise NotImplementedError

    # -------CACHING POLICY/UTILS ----

    def is_cached(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def is_cached_to_sql(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def parquet_dir(self) -> str:
        return self._parquet_dir

    def sql_pushing_schema_prefix(self, dataset: st.Dataset) -> str:
        raise NotImplementedError

    def computation_timeout(self, dataspec: st.DataSpec) -> int:
        raise NotImplementedError

    def computation_max_delay(self, dataspec: st.DataSpec) -> int:
        raise NotImplementedError

    # ------SYNC COMPUTATIONS METHODS--------------

    def to(
        self, dataset: st.Dataset, kind: t.Type, drop_admin: bool = True
    ) -> st.DatasetCastable:
        return sync(self.async_to(dataset, kind, drop_admin))

    def bounds(self, dataset: st.Dataset) -> st.Bounds:
        return t.cast(Bounds, sync(self.async_bounds(dataset)))

    def cache_scalar(self, scalar: st.Scalar) -> None:
        sync(self.async_cache_scalar(scalar=scalar))

    def links(self, dataset: st.Dataset) -> st.Links:
        return t.cast(Links, sync(self.async_links(dataset)))

    def marginals(self, dataset: st.Dataset) -> st.Marginals:
        return t.cast(Marginals, sync(self.async_marginals(dataset)))

    def prepare(self, dataspec: st.DataSpec) -> None:
        """Make sure a Dataspec is ready."""
        sync(self.async_prepare(dataspec))

    def schema(self, dataset: st.Dataset) -> Schema:
        return t.cast(Schema, sync(self.async_schema(dataset=dataset)))

    def size(self, dataset: st.Dataset) -> st.Size:
        return t.cast(Size, sync(self.async_size(dataset)))

    def multiplicity(self, dataset: st.Dataset) -> st.Multiplicity:
        return t.cast(Multiplicity, sync(self.async_multiplicity(dataset)))

    def sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> t.Iterator[pa.RecordBatch]:
        return sync_iterator(
            self.async_sql(dataset, query, dialect, batch_size)
        )

    def sql_prepare(self, dataset: st.Dataset) -> None:
        """SQL prepare dataset."""
        sync(self.async_sql_prepare(dataset))

    def to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.Iterator[pa.RecordBatch]:
        return sync_iterator(
            self.async_to_arrow(dataset=dataset, batch_size=batch_size)
        )

    def to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        return sync(self.async_to_pandas(dataset=dataset))

    def to_parquet(self, dataset: st.Dataset) -> None:
        sync(self.async_to_parquet(dataset=dataset))

    def to_sql(self, dataset: st.Dataset) -> None:
        sync(self.async_to_sql(dataset=dataset))

    def push_sql(self, dataset: st.Dataset) -> None:
        sync(self.async_push_sql(dataset=dataset))

    def to_tensorflow(self, dataset: st.Dataset) -> tf.data.Dataset:
        return sync(self.async_to_tensorflow(dataset=dataset))

    def value(self, scalar: st.Scalar) -> st.DataSpecValue:
        return sync(self.async_value(scalar=scalar))

    def composed_callable(
        self, transform: st.Transform
    ) -> t.Callable[..., t.Any]:
        implementation = get_implementation(transform.transform_to_apply())
        return implementation.callable(transform)

    # ------ASYNC COMPUTATIONS--------
    async def async_to(
        self,
        dataset: st.Dataset,
        kind: t.Type,
        drop_admin: bool = True,
        batch_size: t.Optional[int] = None,
    ) -> st.DatasetCastable:
        """Convert a Dataset's to a Python type."""
        if batch_size is None:
            batch_size = BATCH_SIZE
        if drop_admin:
            batches_async_it = await async_to_arrow_extract_data_only(
                dataset=dataset, batch_size=batch_size
            )
        else:
            if kind not in [
                pd.DataFrame,
                t.Iterator[pa.RecordBatch],
                t.AsyncIterator[pa.RecordBatch],
                pd.core.groupby.DataFrameGroupBy,
                pd.core.groupby.SeriesGroupBy,
            ]:
                raise TypeError(
                    f"The target type {kind} is not compatible"
                    " with the protection."
                )
            batches_async_it = await dataset.async_to_arrow(
                batch_size=batch_size
            )

        return await async_cast_arrow_batches(batches_async_it, kind)

    async def async_bounds(self, dataset: st.Dataset) -> st.Bounds:
        raise NotImplementedError

    async def async_cache_scalar(self, scalar: st.Scalar) -> None:
        await self.cache_scalar_computation.complete_task(dataspec=scalar)

    async def async_prepare(self, dataspec: st.DataSpec) -> None:
        """Make sure a Dataspec is ready asynchronously."""
        computation = self.dataspec_computation(dataspec)
        await computation.complete_task(dataspec)

    async def async_prepare_parents(self, dataspec: st.DataSpec) -> None:
        """Prepare all the parents of a Dataspec."""
        args, kwargs = dataspec.parents()
        parents = list(args) + list(kwargs.values())
        coros = [
            self.async_prepare(parent)
            for parent in parents
            if isinstance(parent, st.DataSpec)
        ]
        # here, if many parents potentially fail, we want to be sure
        # that all of them do it, and not only the first one (to
        # modify all statuses accordingly).
        # After, we only raise the first exception for the child.

        results = await asyncio.gather(*coros, return_exceptions=True)
        exceptions = [
            element for element in results if isinstance(element, Exception)
        ]
        if len(exceptions) == 0:
            return
        raise error_aggregation(exceptions)

    async def async_links(self, dataset: st.Dataset) -> t.Any:
        raise NotImplementedError

    async def async_marginals(self, dataset: st.Dataset) -> st.Marginals:
        raise NotImplementedError

    async def async_schema(self, dataset: st.Dataset) -> st.Schema:
        return await self.schema_computation.task_result(dataspec=dataset)

    async def async_size(self, dataset: st.Dataset) -> st.Size:
        raise NotImplementedError

    async def async_multiplicity(self, dataset: st.Dataset) -> st.Multiplicity:
        raise NotImplementedError

    async def async_to_arrow(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Reads asynchronous iterator of datast batches"""
        computation = t.cast(
            Computation[t.AsyncIterator[pa.RecordBatch]],
            self.dataspec_computation(dataset),
        )
        return await computation.task_result(
            dataspec=dataset, batch_size=batch_size
        )

    async def async_to_parquet(self, dataset: st.Dataset) -> None:
        await self.to_parquet_computation.complete_task(dataspec=dataset)

    async def async_sql(
        self,
        dataset: st.Dataset,
        query: t.Union[str, st.NestedQueryDict],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        computation = t.cast(
            Computation[t.AsyncIterator[pa.RecordBatch]],
            self.sql_computation(),
        )
        return await computation.task_result(
            dataset,
            query=query,
            dialect=dialect,
            batch_size=batch_size,
            result_type=result_type,
        )

    async def async_sql_prepare(self, dataset: st.Dataset) -> None:
        """SQL prepare the dataset synchronously"""
        computation = t.cast(
            Computation[t.AsyncIterator[pa.RecordBatch]],
            self.sql_computation(),
        )
        await computation.complete_task(dataset)

    async def async_sql_prepare_parents(self, dataset: st.Dataset) -> None:
        """SQL prepare all the parents of a dataset: calling async_sql_prepare
        for dataset parents and async_prepare for scalar parents.
        """
        args, kwargs = dataset.parents()
        parents = list(args) + list(kwargs.values())
        coros = [
            self.async_sql_prepare(t.cast(st.Dataset, parent))
            if dataset.prototype() == sp.Dataset
            else self.async_prepare(parent)
            for parent in parents
            if isinstance(parent, st.DataSpec)
        ]
        # here, if many parents potentially fail, we want to be sure
        # that all of them do it, and not only the first one (to
        # modify all statuses accordingly).
        # After, we only raise the first exception for the child.

        results = await asyncio.gather(*coros, return_exceptions=True)
        exceptions = [
            element for element in results if isinstance(element, Exception)
        ]
        if len(exceptions) == 0:
            return
        raise error_aggregation(exceptions)

    async def async_to_pandas(self, dataset: st.Dataset) -> pd.DataFrame:
        return await self.async_to(
            dataset=dataset, kind=pd.DataFrame, drop_admin=False
        )

    async def async_value(self, scalar: st.Scalar) -> t.Any:
        """Reads asynchronously value of a scalar."""
        computation = self.dataspec_computation(scalar)
        return await computation.task_result(dataspec=scalar)

    # -------- REWRITING ---------

    def dataspec_rewriter(self) -> sdrt.DataspecRewriter:
        return self._dataspec_rewriter

    def dataspec_validator(self) -> sdvt.DataspecValidator:
        return self._dataspec_validator

    def set_remote(self, dataspec: st.DataSpec) -> None:
        """Add an Attribute to tag the DataSpec as remotely fetched."""
        attach_properties(
            dataspec,
            properties={
                # TODO deprecated in SDS >=2.0.0 -> remove property
                "is_remote": str(True)
            },
            name=IS_REMOTE,
        )

    def is_remote(self, dataspec: st.DataSpec) -> bool:
        """Is the dataspec a remotely defined dataset."""
        is_remote_att = self.attribute(IS_REMOTE, dataspec)
        return is_remote_att is not None

    def dataspec_computation(
        self, dataspec: st.DataSpec
    ) -> Computation[t.AsyncIterator[pa.RecordBatch]]:
        """Return the Computation for getting the dataspec's value"""
        raise NotImplementedError

    def sql_computation(self) -> Computation[t.AsyncIterator[pa.RecordBatch]]:
        """Returns the SQL Computation of the manager. The aim of the method is
        is to reduce code duplication between API and Worker manager
        """
        raise NotImplementedError

    async def async_to_tensorflow(
        self, dataset: st.Dataset
    ) -> tf.data.Dataset:
        root_dir = os.path.join(
            self.parquet_dir(), "tfrecords", dataset.uuid()
        )
        schema_type = (await self.async_schema(dataset)).type()
        signature = to_internal_signature(schema_type)

        if not os.path.exists(root_dir):
            # the dataset is cached first
            os.makedirs(root_dir)

            flattener = flatten(signature)
            serializer = serialize(signature)
            i = 0
            batches_async_it = await self.async_to_arrow(
                dataset=dataset, batch_size=BATCH_SIZE
            )
            async for batch in batches_async_it:
                filename = os.path.join(root_dir, f"batch_{i}.tfrecord")
                i += 1
                await write_tf_batch(
                    filename, batch, schema_type, flattener, serializer
                )

        # reading from cache
        glob = os.path.join(root_dir, "*.tfrecord")
        filenames = tf.data.Dataset.list_files(glob, shuffle=False)
        deserializer = deserialize(signature)
        nester = nest(signature)
        return tf.data.TFRecordDataset(filenames).map(deserializer).map(nester)

    def mock_value(
        self,
        transform: st.Transform,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> t.Any:
        """Compute the mock value of an external transform applied on
        Dataspecs.
        """
        start = time.perf_counter()
        assert transform.is_external()
        mock_args = [
            arg.variant(st.ConstraintKind.MOCK)
            if isinstance(arg, st.DataSpec)
            else arg  # `arg` can be a composed Transform
            for arg in arguments
        ]
        named_mock_args = {
            name: arg.variant(st.ConstraintKind.MOCK)
            if isinstance(arg, st.DataSpec)
            else arg  # `arg` can be a composed Transform
            for name, arg in named_arguments.items()
        }

        if any([ds is None for ds in mock_args]) or any(
            [ds is None for ds in named_mock_args.values()]
        ):
            raise ValueError(
                "Cannot infer the output type of the external "
                "transform because one of the parents has a None MOCK."
            )

        typed_mock_args = [t.cast(st.DataSpec, ds) for ds in mock_args]
        typed_named_mock_args = {
            name: t.cast(st.DataSpec, ds)
            for name, ds in named_mock_args.items()
        }

        try:
            mock_value = sync(
                async_compute_external_value(
                    transform, *typed_mock_args, **typed_named_mock_args
                )
            )
        except Exception as e:
            raise e

        end = time.perf_counter()
        logger.info(f"MOCK VALUE {transform_id(transform)} ({end-start:.2f}s)")

        return mock_value

    async def async_value_op(self, scalar: st.Scalar) -> t.Any:
        raise NotImplementedError

    async def async_to_arrow_op(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    async def async_schema_op(self, dataset: st.Dataset) -> st.Schema:
        raise NotImplementedError

    async def async_to_sql(self, dataset: st.Dataset) -> None:
        raise NotImplementedError

    async def async_push_sql(self, dataset: st.Dataset) -> None:
        raise NotImplementedError

    async def async_sql_op(
        self,
        dataset: st.Dataset,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    def engine(self, uri: str) -> sa_engine:
        raise NotImplementedError

    async def execute_sql_query(
        self,
        dataset: st.Dataset,
        caching_properties: t.Mapping[str, str],
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    def manager(self) -> manager_typing.Manager:
        return self

    def launch_job(self, command: t.List[str], env: t.Dict[str, str]) -> None:
        raise NotImplementedError

    def python_type(self, dataspec: st.DataSpec) -> str:
        raise NotImplementedError


def check_transform_big_data(
    transform: st.Transform,
    parent_dataset: st.Dataset,
    parents_dict: t.Mapping[str, st.DataSpec],
) -> t.Tuple[bool, int, int, str]:
    """This methods return true if the dataset transformed
    is big_data and False otherwise. This method is called when the parent
    is big_data so if the transform does not
    affect the size, it should return True
    """
    status = parent_dataset.manager().status(
        parent_dataset, task_name=BIG_DATA_TASK
    )
    if status is None:
        status = stt.last_status(parent_dataset, task=BIG_DATA_TASK)
    assert status
    big_data_threshold = int(
        status.task(BIG_DATA_TASK).properties()[BIG_DATA_THRESHOLD]  # type:ignore
    )
    threshold_kind = status.task(BIG_DATA_TASK).properties()[THRESHOLD_TYPE]  # type:ignore

    parent_n_lines_str = status.task(BIG_DATA_TASK).properties()[  # type:ignore
        DATASET_N_LINES
    ]
    if parent_n_lines_str == "":
        parent_n_lines = 0
    else:
        parent_n_lines = int(parent_n_lines_str)

    parent_bytes_str = status.task(BIG_DATA_TASK).properties()[DATASET_N_BYTES]  # type:ignore
    if parent_bytes_str == "":
        parent_bytes = 0
    else:
        parent_bytes = int(parent_bytes_str)

    transform_name = transform.name()
    if transform_name in ("Sample", "DifferentiatedSample"):
        transform_type = transform.protobuf().spec.WhichOneof("spec")
        assert transform_type
        if getattr(transform.protobuf().spec, transform_type).HasField(
            "fraction"
        ):
            fraction = getattr(
                transform.protobuf().spec, transform_type
            ).fraction
            new_bytes = int(fraction * parent_bytes)
            n_lines = int(fraction * parent_n_lines)

            if threshold_kind == DATASET_N_BYTES:
                return (
                    new_bytes > big_data_threshold,
                    n_lines,
                    new_bytes,
                    threshold_kind,
                )
        else:
            n_lines = getattr(transform.protobuf().spec, transform_type).size
            new_bytes = int(n_lines * parent_bytes / parent_n_lines)

            if threshold_kind == DATASET_N_BYTES:
                big_data_threshold = int(1e5)

        threshold_kind = DATASET_N_LINES

        return n_lines > big_data_threshold, n_lines, new_bytes, threshold_kind

    elif transform_name == "filter":
        # TODO: we need to save the real sizes of a dataspec in the statuses
        # so that we can check what happens here
        return True, parent_n_lines, parent_bytes, threshold_kind

    elif transform_name == "Synthetic data":
        # here we should leverage the sampling ratio just to get the size,
        # in any case, synthetic data is never big data

        threshold_kind = DATASET_N_LINES
        synthetic_size = parent_dataset.size()
        assert synthetic_size is not None

        return (
            False,
            synthetic_size.statistics().size(),
            int(
                synthetic_size.statistics().size()
                * parent_bytes
                / parent_n_lines
            ),
            threshold_kind,
        )
    elif transform_name == "select_sql":
        # TODO https://gitlab.com/sarus-tech/sarus-data-spec/-/issues/207
        return True, parent_n_lines, parent_bytes, threshold_kind
    # just for test
    elif transform_name == "ToSmallData":
        return (False, -1, -1, threshold_kind)
    else:
        # other transforms do not affect size
        if transform_name == "user_settings":
            warnings.warn(
                "user_settings transform considered to" "not affect size"
            )
        return True, parent_n_lines, parent_bytes, threshold_kind


async def write_tf_batch(
    filename: str,
    batch: pa.RecordBatch,
    schema_type: st.Type,
    flattener: t.Callable,
    serializer: t.Callable,
) -> None:
    with tf.io.TFRecordWriter(filename) as writer:
        batch = convert_tensorflow(
            convert_record_batch(record_batch=batch, _type=schema_type),
            schema_type,
        )
        batch = tf.data.Dataset.from_tensor_slices(batch).map(flattener)
        for row in batch:
            as_bytes = serializer(row)
            writer.write(as_bytes)
