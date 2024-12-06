import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.pandas_utils import remove_pandas_index_columns
from sarus_data_spec.json_serialisation import (
    SarusJSONDecoder,
    SarusJSONEncoder,
)
from sarus_data_spec.manager.async_utils import (
    sync_iterator_from_async_iterator,
)
import sarus_data_spec.typing as st

NO_SERIES_NAME = "__sarus_no_name__"
GROUPBY_COLUMN_NAME = "__sarus_groupby_index_"
GROUPBY_KEYS_NAME = "sarus_groupby_keys_names"


async def async_cast_arrow_batches(
    batches_async_iterator: t.AsyncIterator[pa.RecordBatch],
    kind: st.DatasetCastable,
) -> st.DatasetCastable:
    """Convert an async record batches iterator to another Python type."""
    if kind not in t.get_args(st.DatasetCastable):
        raise TypeError(f"Cannot cast a Dataset to type {kind}")
    if kind == t.AsyncIterator[pa.RecordBatch]:
        return batches_async_iterator
    if kind == t.Iterator[pa.RecordBatch]:
        return sync_iterator_from_async_iterator(batches_async_iterator)
    if kind == pd.DataFrame:
        return await async_arrow_batches_to_dataframe(batches_async_iterator)
    elif kind == pd.Series:
        return await async_arrow_batches_to_series(batches_async_iterator)
    elif kind == pd.core.groupby.DataFrameGroupBy:
        return await async_arrow_batches_to_dataframegroupby(
            batches_async_iterator
        )
    elif kind == pd.core.groupby.SeriesGroupBy:
        return await async_arrow_batches_to_seriesgroupby(
            batches_async_iterator
        )
    else:
        raise NotImplementedError(
            f"Arrow to Python: No converter implemented for type {kind}"
        )


async def async_arrow_batches_to_dataframe(
    batches_async_iterator: t.AsyncIterator[pa.RecordBatch],
) -> pd.DataFrame:
    arrow_batches = [batch async for batch in batches_async_iterator]
    # follow advices in
    # https://arrow.apache.org/docs/python/pandas.html#reducing
    # -memory-use-in-table-to-pandas
    tab = pa.Table.from_batches(arrow_batches)
    # split_blocks=True prevent from assigning values to dataframe
    # in the SDK:
    # error: ValueError: assignment destination is read-only
    df = tab.to_pandas(split_blocks=False, self_destruct=True)
    del tab  # not necessary, but a good practice
    return df


async def async_df_to_series(df: pd.DataFrame) -> pd.Series:
    n_rows, n_cols = df.shape
    if n_cols == 1:
        first_col = df.columns[0]
        series = df[first_col]
        if first_col == NO_SERIES_NAME:
            # This is a default value for a column.
            # The series actually has no name.
            series.name = None
    elif n_rows == 1:
        series = df.iloc[0]
    else:
        raise ValueError(
            "Trying to convert to series Arrow batches "
            "with more than 1 line and 1 column."
        )

    return series


async def async_arrow_batches_to_series(
    batches_async_iterator: t.AsyncIterator[pa.RecordBatch],
) -> pd.Series:
    """Returns the first columns of the DataFrame."""
    df = await async_arrow_batches_to_dataframe(batches_async_iterator)
    series = await async_df_to_series(df)
    return series


async def async_arrow_batches_to_dataframegroupby(
    batches_async_iterator: t.AsyncIterator[pa.RecordBatch],
) -> pd.Series:
    """Returns the group by object from the data."""
    arrow_batches = [batch async for batch in batches_async_iterator]
    tab = pa.Table.from_batches(arrow_batches)
    groupby_keys_bytes = bytes(GROUPBY_KEYS_NAME, "utf-8")
    if groupby_keys_bytes in tab.schema.metadata:
        keys_encoded = tab.schema.metadata[groupby_keys_bytes]
        keys = SarusJSONDecoder.decode_bytes(keys_encoded)
    else:
        raise ValueError(
            "Trying to convert to series Arrow batches "
            "without groupby keys already defined."
        )

    df = tab.to_pandas(split_blocks=False, self_destruct=True)
    del tab  # not necessary, but a good practice
    groupby_object = df.groupby(keys)
    return groupby_object


async def async_arrow_batches_to_seriesgroupby(
    batches_async_iterator: t.AsyncIterator[pa.RecordBatch],
) -> pd.Series:
    """Returns the group by object from the data."""
    arrow_batches = [batch async for batch in batches_async_iterator]
    tab = pa.Table.from_batches(arrow_batches)
    df = tab.to_pandas(split_blocks=False, self_destruct=True)
    groupby_keys_bytes = bytes(GROUPBY_KEYS_NAME, "utf-8")
    if groupby_keys_bytes in tab.schema.metadata:
        keys_encoded = tab.schema.metadata[groupby_keys_bytes]
        keys = SarusJSONDecoder.decode_bytes(keys_encoded)
    else:
        raise ValueError(
            "Trying to convert to series Arrow batches "
            "without groupby keys already defined."
        )
    del tab  # not necessary, but a good practice

    series = await async_df_to_series(df)

    groupby_object = series.groupby(keys)
    return groupby_object


def to_pyarrow_table(data: t.Any) -> pa.Table:
    """Convert the result of an external transform to a Pyarrow Table."""
    if type(data) not in t.get_args(st.DatasetCastable):
        raise TypeError(f"Cannot convert {type(data)} to Arrow batches.")

    if isinstance(data, pd.DataFrame):
        df = t.cast(pd.DataFrame, data)
        return pa.Table.from_pandas(df, preserve_index=True)
    elif isinstance(data, pd.Series):
        sr = t.cast(pd.Series, data)
        if sr.name is None:
            # We need to set a name otherwise pandas adds a default one.
            sr.name = NO_SERIES_NAME
        return pa.Table.from_pandas(pd.DataFrame(sr), preserve_index=True)
    elif isinstance(data, pd.core.groupby.DataFrameGroupBy):
        df_grouped_by = t.cast(pd.core.groupby.DataFrameGroupBy, data)
        combined_df = df_grouped_by.obj

        keys = df_grouped_by.keys
        encoded_keys = SarusJSONEncoder.encode_bytes(keys)

        table_without_keys = remove_pandas_index_columns(
            pa.Table.from_pandas(combined_df)
        )
        table_with_keys = table_without_keys.replace_schema_metadata(
            {GROUPBY_KEYS_NAME: encoded_keys}
        )

        return table_with_keys
    elif isinstance(data, pd.core.groupby.SeriesGroupBy):
        series_grouped_by = t.cast(pd.core.groupby.SeriesGroupBy, data)
        combined_series = series_grouped_by.obj
        if combined_series.name is None:
            combined_series.name = NO_SERIES_NAME

        keys = series_grouped_by.keys
        encoded_keys = SarusJSONEncoder.encode_bytes(keys)

        table_without_keys = remove_pandas_index_columns(
            pa.Table.from_pandas(pd.DataFrame(combined_series))
        )
        table_with_keys = table_without_keys.replace_schema_metadata(
            {GROUPBY_KEYS_NAME: encoded_keys}
        )

        return table_with_keys
    elif isinstance(data, t.Iterator):
        # We test this case last because DataFrames and Series are also
        # Iterators. We cannot easily test that an object is an Iterator of a
        # specific type. So we put the Iterator[pa.RecordBatch] last as the
        # last possible case.
        batches = t.cast(t.Iterator[pa.RecordBatch], data)
        return pa.Table.from_batches(batches)
    else:
        raise NotImplementedError(
            f"Python to Arrow: No converter implemented for type {type(data)}"
        )
