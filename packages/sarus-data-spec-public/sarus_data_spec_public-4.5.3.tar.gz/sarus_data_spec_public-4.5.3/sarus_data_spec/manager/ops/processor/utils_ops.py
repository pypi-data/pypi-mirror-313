import typing as t

import pyarrow as pa

from sarus_data_spec.transform import (
    has_sarus_default_output,
    extract_sarus_default_output,
)
from sarus_data_spec.manager.async_utils import (
    async_iter,
)
from sarus_data_spec.manager.ops.base import (
    _ensure_batch_correct,
)
import sarus_data_spec.typing as st
from sarus_data_spec.status import DataSpecErrorStatus


async def check_first_batch_empty(
    ait: t.AsyncIterator[pa.RecordBatch],
) -> t.Tuple[bool, t.AsyncIterator[pa.RecordBatch]]:
    """Returns False if the async iterator have a first not empty batch, and return the original iterator. R"""
    try:
        first_item = await ait.__anext__()

        async def chained_iterator() -> t.AsyncIterator[pa.RecordBatch]:
            yield first_item
            async for item in ait:
                yield item

        return first_item.num_rows == 0, chained_iterator()
    except StopAsyncIteration:
        return True, ait


async def ensure_batch_correct_and_not_empty(
    dataset: st.DataSpec,
    async_iterator: t.AsyncIterator[pa.RecordBatch],
    batch_size: int,
) -> t.AsyncIterator[pa.RecordBatch]:
    """Ensures that the provided asynchronous iterator over a dataset does not yield empty batches.

    This function checks if the iterator is initially empty. If not, it simply returns the original iterator.
    If the iterator is empty and has a default output defined (i.e., 'sarus_default_output').
    For datasets with a default output, it creates and returns a new async iterator that yields batches created from the default output.
    If no default output is present, it raises a ValueError indicating that the computation results in an empty dataset without a schema,
    thus limiting the transformations that can be applied."""

    async def identity(x: pa.Array) -> pa.Array:
        return x

    ait = _ensure_batch_correct(
        async_iterator=async_iterator,
        func_to_apply=identity,
        batch_size=batch_size,
    )

    is_empty, original_async_iterator = await check_first_batch_empty(ait)
    if not is_empty:
        return original_async_iterator
    # use default value if it exists
    elif has_sarus_default_output(dataset.transform()):
        if not dataset.is_pup():
            default_table = extract_sarus_default_output(dataset.transform())
            return async_iter(
                default_table.to_batches(max_chunksize=batch_size)
            )
        else:
            raise NotImplementedError(
                "Sarus default output is not implemented for pup dataset"
            )
    else:
        message_empty_ait = f"""Warning: The computation of dataspec: {dataset.uuid()} returns an empty result, which does not have a schema. This limits the transformations you can apply to the resulting object.
    If you believe that the computation on real data is not empty, you may provide the schema by adding a dummy example using the parameter 'sarus_default_output'.
    You can find more details at https://docs.sarus.tech/User%20Guide/data_science_%26_AI.html#handling-empty-mocks-error. """
        raise DataSpecErrorStatus(
            (
                False,
                message_empty_ait,
            )
        )
