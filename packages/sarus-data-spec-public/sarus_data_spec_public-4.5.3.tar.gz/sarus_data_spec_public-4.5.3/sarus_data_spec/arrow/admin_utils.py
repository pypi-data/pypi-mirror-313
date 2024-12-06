import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.pandas_utils import (
    convert_pandas_metadata_to_admin_columns,
    pandas_index_columns,
    remove_pandas_index_columns,
)
from sarus_data_spec.constants import DATA, PU_COLUMN, PUBLIC, WEIGHTS
import sarus_data_spec.typing as st


async def async_to_arrow_extract_admin(
    dataset: st.Dataset, batch_size: int = 10000
) -> t.Optional[t.AsyncIterator[pa.RecordBatch]]:
    """This function return an async iterator record batches of the
    admin data if there is administrative columns.
    """

    schema = await dataset.async_schema()
    if not schema.has_admin_columns():
        return None

    # Extract admin data from DATA
    batches_async_it = await dataset.async_to_arrow(batch_size)
    pe_field_names = [PUBLIC, PU_COLUMN, WEIGHTS]

    async def extract_admin_columns(
        batches_async_it: t.AsyncIterator[pa.RecordBatch],
    ) -> t.AsyncIterator[t.Tuple[pa.RecordBatch, t.Optional[pa.RecordBatch]]]:
        async for batch in batches_async_it:
            field_names = list(batch.schema.names)
            index_cols = pandas_index_columns(batch.schema)
            pe_batch = pa.RecordBatch.from_arrays(
                [
                    batch.columns[field_names.index(field_name)]
                    for field_name in pe_field_names + index_cols
                ],
                names=pe_field_names + index_cols,
            )
            pe_batch = pe_batch.replace_schema_metadata(batch.schema.metadata)
            yield pe_batch

    return extract_admin_columns(batches_async_it)


async def async_to_arrow_extract_data_only(
    dataset: st.Dataset, batch_size: int = 10000
) -> t.AsyncIterator[pa.RecordBatch]:
    """This function return an async iterator of record batches.

    The RecordBatches contain the data only, without the admin columns.
    """
    batches_async_it = await dataset.async_to_arrow(batch_size)
    schema = await dataset.async_schema()

    if not schema.has_admin_columns():
        return batches_async_it

    # Extract PE from DATA
    data_cols = list(schema.type().data_type().children().keys())

    async def extract_data(
        batches_async_it: t.AsyncIterator[pa.RecordBatch],
    ) -> t.AsyncIterator[pa.RecordBatch]:
        async for batch in batches_async_it:
            # We add the index columns to the data
            field_names = list(batch.schema.names)
            index_cols = pandas_index_columns(batch.schema)
            index_arrays = [
                batch.columns[field_names.index(col)]
                for col in pandas_index_columns(batch.schema)
            ]

            data_arrays = batch.columns[field_names.index(DATA)].flatten()
            arrays = index_arrays + data_arrays
            names = index_cols + data_cols

            if len(arrays) != len(names):
                raise ValueError(
                    f"Incompatible number of arrays {len(arrays)} and"
                    f" names {len(names)}.\n"
                    f"Names are index cols {index_cols} and data "
                    f"cols {data_cols}.\n"
                    f"There are {len(index_arrays)} index arrays "
                    f"and {len(data_arrays)} data arrays.\n"
                    f"Arrow batch schema is {batch.schema}."
                )
            new_struct_array = pa.StructArray.from_arrays(arrays, names)
            data_batch = pa.RecordBatch.from_struct_array(new_struct_array)
            data_batch = data_batch.replace_schema_metadata(
                batch.schema.metadata
            )
            yield data_batch

    return extract_data(batches_async_it)


async def async_admin_data(dataset: st.Dataset) -> t.Optional[pa.Table]:
    """Return the privacy unit as a pa.Table if it exists."""
    pe_batches_async_it = await async_to_arrow_extract_admin(dataset)
    if pe_batches_async_it is None:
        return None
    pe_batches = [batch async for batch in pe_batches_async_it]
    return pa.Table.from_batches(pe_batches)


def merge_schemas_metadata(schema1: pa.Schema, schema2: pa.Schema) -> dict:
    """Merge metadata from two PyArrow schemas."""
    metadata1 = schema1.metadata or {}
    metadata2 = schema2.metadata or {}

    # Combine metadata from both schemas
    merged_metadata = {**metadata1, **metadata2}

    return merged_metadata


def merge_data_and_admin(
    data: pa.Table, admin_data: t.Optional[pa.Table]
) -> pa.Table:
    """Merge a protection and the data.

    If the data Table has some pandas metadata attached, we remove them before
    merging with the privacy unit.
    """
    if admin_data is None:
        # TODO also wrap the data in an empty protection
        return data

    data_index_columns = pandas_index_columns(data.schema)
    if len(data_index_columns) > 0:
        # There are some pandas metadata
        assert data_index_columns == pandas_index_columns(admin_data.schema)
        data = remove_pandas_index_columns(data)

    merged_metadata = merge_schemas_metadata(data.schema, admin_data.schema)

    # We merge the privacy unit and data in Pyarrow
    data_arrays = [
        chunked_array.combine_chunks() for chunked_array in data.columns
    ]
    data_array = pa.StructArray.from_arrays(
        data_arrays, names=data.column_names
    )
    merged_table = admin_data.append_column(DATA, data_array)
    merged_table = merged_table.replace_schema_metadata(merged_metadata)
    return merged_table


def compute_admin_data(
    input_admin_data: pa.Table, result: st.DatasetCastable
) -> pa.Table:
    """Compute the output privacy unit of an external transform."""
    # We guarantee that the data.index is a reliable way to trace how
    # the rows were rearranged using PyArrow's  internal implementation
    # See: https://arrow.apache.org/docs/python/pandas.html#handling-pandas-indexes

    if isinstance(result, pd.DataFrame):
        df = t.cast(pd.DataFrame, result)
        input_pe_df = input_admin_data.to_pandas()
        output_admin_data = pa.Table.from_pandas(input_pe_df.loc[df.index])
    elif isinstance(result, pd.Series):
        sr = t.cast(pd.Series, result)
        input_pe_df = input_admin_data.to_pandas()
        output_admin_data = pa.Table.from_pandas(input_pe_df.loc[sr.index])
    elif isinstance(result, pd.core.groupby.DataFrameGroupBy):
        df_grouped_by = t.cast(pd.core.groupby.DataFrameGroupBy, result)
        combined_df = df_grouped_by.obj
        input_pe_df = input_admin_data.to_pandas()
        output_admin_data = pa.Table.from_pandas(
            input_pe_df.loc[combined_df.index]
        )
    elif isinstance(result, pd.core.groupby.SeriesGroupBy):
        series_grouped_by = t.cast(pd.core.groupby.SeriesGroupBy, result)
        combined_series = series_grouped_by.obj
        input_pe_df = input_admin_data.to_pandas()
        output_admin_data = pa.Table.from_pandas(
            input_pe_df.loc[combined_series.index]
        )
    else:
        raise TypeError(
            f"Cannot compute the admin data for type {type(result)}"
        )

    columns_to_cast = set(input_admin_data.column_names) & set(
        output_admin_data.column_names
    )

    for col in columns_to_cast:
        field = input_admin_data.field(col)

        if field != output_admin_data.field(col):
            i = output_admin_data.schema.get_field_index(col)
            column = output_admin_data.column(col).cast(field.type)
            output_admin_data = output_admin_data.set_column(i, field, column)

    return output_admin_data


def validate_privacy_unit(
    admin_data: t.List[pa.Table],
) -> pa.Table:
    """Check privacy unit related administrative data are equal across several
    tables."""
    if len(admin_data) == 0:
        raise ValueError("The list of input admin data is empty.")

    pu = next(iter(admin_data), None)
    if pu is None:
        raise ValueError(
            "The dataset was infered PUP but has no input admin data"
        )

    cols_to_check = [PU_COLUMN, WEIGHTS, PUBLIC]

    if not all(
        [
            candidate.select(cols_to_check).equals(pu.select(cols_to_check))
            for candidate in admin_data
        ]
    ):
        raise ValueError(
            "The dataset is PUP but has several differing input admin "
            "data values"
        )
    return pu


def create_admin_columns(table: pa.Table) -> pa.Table:
    """Isolate special columns to admin columns."""
    return convert_pandas_metadata_to_admin_columns(table)
