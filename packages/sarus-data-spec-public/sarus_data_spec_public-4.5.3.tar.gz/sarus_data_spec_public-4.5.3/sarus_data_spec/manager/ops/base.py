from __future__ import annotations

import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec.manager.async_utils import decoupled_async_iter
import sarus_data_spec.dataspec_validator.typing as sdvt
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.sarus_query_builder.core.core import (
        OptimizableQueryBuilder,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus" not in str(e_pandas_dp):
        raise


class DataspecStaticChecker:
    def __init__(self, dataspec: st.DataSpec):
        self.dataspec = dataspec

    def is_dp_writable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PUP arguments are PUP and aligned
            (i.e. same PUP token)
            - other dataspecs arguments are public
        """
        return False

    def is_dp(self) -> bool:
        """Checks if the transform is DP and compatible with the arguments."""
        return False

    def is_dp_able(self) -> bool:
        """Checks if the dataspec has a transform that either has a DP
        equivalent, allowing the rewritten dataspec to be considered DP
        if the input rewritten PUP token is not None."""
        return False

    def is_pup_able(self) -> bool:
        """Checks if the dataspec has a transform that either has a PUP
        equivalent or does not require one, allowing the rewritten dataspec to
        be considered 'PUP' if the input rewritten PUP token is not None."""
        raise NotImplementedError(
            f"Dataspec {self.dataspec.uuid()} was asked if it is_pup_able"
        )

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        return None

    def pup_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's PUP equivalent transform if existing."""
        return None

    def dp_equivalent(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        raise NotImplementedError

    async def private_queries(self) -> t.List[st.PrivateQuery]:
        """Return the PrivateQueries summarizing DP characteristics."""
        if self.is_dp():
            raise NotImplementedError
        else:
            return []

    async def query_builder(self) -> OptimizableQueryBuilder:
        raise NotImplementedError


class DatasetStaticChecker(DataspecStaticChecker):
    def __init__(self, dataset: st.Dataset):
        super().__init__(dataset)
        self.dataset = dataset

    async def schema(self) -> st.Schema:
        """Computes the schema of the dataspec"""
        raise NotImplementedError

    def pup_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """Return a token if the output is PUP."""
        raise NotImplementedError

    def rewritten_pup_token(
        self, public_context: t.Collection[str]
    ) -> t.Optional[str]:
        raise NotImplementedError

    def pup_kind(self) -> sdvt.PUPKind:
        raise NotImplementedError


class DatasetImplementation:
    def __init__(self, dataset: st.Dataset):
        self.dataset = dataset

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    async def size(self) -> st.Size:
        raise NotImplementedError

    async def multiplicity(self) -> st.Multiplicity:
        raise NotImplementedError

    async def bounds(self) -> st.Bounds:
        raise NotImplementedError

    async def marginals(self) -> st.Marginals:
        raise NotImplementedError

    async def sql(
        self,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """It composes the query and it sends it to the parent."""
        raise NotImplementedError

    @staticmethod
    async def decoupled_async_iter(
        source: t.AsyncIterator[pa.RecordBatch], buffer_size: int = 100
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return decoupled_async_iter(source=source, buffer_size=buffer_size)


class ScalarImplementation:
    def __init__(self, scalar: st.Scalar):
        self.scalar = scalar

    async def value(self) -> t.Any:
        raise NotImplementedError

    @staticmethod
    async def decoupled_async_iter(
        source: t.AsyncIterator[pa.RecordBatch], buffer_size: int = 100
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return decoupled_async_iter(source=source, buffer_size=buffer_size)


def concat_record_batches(batches: t.List[pa.RecordBatch]) -> pa.RecordBatch:
    struct_arrays = [batch.to_struct_array() for batch in batches]
    concatenated_struct_array = pa.concat_arrays(struct_arrays)
    return pa.RecordBatch.from_struct_array(concatenated_struct_array)


async def _ensure_batch_correct(
    async_iterator: t.Union[
        t.AsyncIterator[pa.RecordBatch], t.AsyncIterator[pa.Array]
    ],
    func_to_apply: t.Callable,
    batch_size: int,
) -> t.AsyncIterator[pa.RecordBatch]:
    """Method that executes func_to_apply on each batch
    of the async_iterator but rather than directly returning
    the result, it accumulates them and returns them progressively
    so that each new batch has batch_size."""

    global_array = None
    async for batch in async_iterator:
        new_array = await func_to_apply(batch)
        if len(new_array) == batch_size and global_array is None:
            selected_array = new_array.take(
                np.linspace(0, batch_size - 1, batch_size, dtype=int)
            )

            if isinstance(selected_array, pa.RecordBatch):
                yield selected_array
            else:
                yield pa.RecordBatch.from_struct_array(selected_array)
        elif global_array is not None:
            if isinstance(global_array, pa.RecordBatch) and isinstance(
                new_array, pa.RecordBatch
            ):
                global_array = concat_record_batches([global_array, new_array])
            else:
                global_array = pa.concat_arrays([global_array, new_array])

            if len(global_array) < batch_size:
                continue
            else:
                # here cannot use array.slice because there
                # is a bug in the columns being copied
                # when we switch to record batch
                selected_array = global_array.take(
                    np.linspace(0, batch_size - 1, batch_size, dtype=int)
                )

                if isinstance(selected_array, pa.RecordBatch):
                    yield selected_array
                else:
                    yield pa.RecordBatch.from_struct_array(selected_array)

                global_array = global_array.take(
                    np.linspace(
                        batch_size,
                        len(global_array) - 1,
                        len(global_array) - batch_size,
                        dtype=int,
                    )
                )

        else:
            # initialize global_array
            global_array = new_array
            continue
    # handle remaining array: split it in

    if global_array is not None and len(global_array) > 0:
        while len(global_array) > 0:
            min_val = min(batch_size, len(global_array))
            indices = np.linspace(
                0, len(global_array) - 1, len(global_array), dtype=int
            )
            selected_array = global_array.take(indices[:min_val])

            if isinstance(selected_array, pa.RecordBatch):
                yield selected_array
            else:
                yield pa.RecordBatch.from_struct_array(selected_array)
            global_array = global_array.take(indices[min_val:])
