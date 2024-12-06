import typing as t
import pyarrow as pa

from sarus_data_spec.constants import DATA


def pandas_index_columns(schema: pa.Schema) -> t.List[str]:
    """Return the list of columns that have to be considered as Pandas index
    columns and ignored by the Sarus type.
    """
    pandas_metadata = schema.pandas_metadata
    if pandas_metadata is None:
        return []

    def column_name(index: t.Any) -> t.Optional[str]:
        if isinstance(index, str):
            return index
        elif isinstance(index, dict):
            return t.cast(t.Optional[str], index["name"])
        else:
            raise ValueError("Unrecognized Arrow `index_column` format")

    columns = [
        column_name(index) for index in pandas_metadata["index_columns"]
    ]
    return [col for col in columns if col is not None]


def remove_pandas_index_columns(table: pa.Table) -> pa.Table:
    """Remove pandas metadata and drop additional
    index columns used for Pandas indexing.
    """
    index_columns_names = pandas_index_columns(table.schema)
    return table.drop(index_columns_names).replace_schema_metadata(None)


def convert_pandas_metadata_to_admin_columns(table: pa.Table) -> pa.Table:
    """Isolate the pandas index from the data."""
    index_columns = pandas_index_columns(table.schema)
    if len(index_columns) == 0:
        return table

    # Create admin columns
    data_columns = [
        col for col in table.column_names if col not in index_columns
    ]

    data_arrays = [
        chunked_array.combine_chunks()
        for name, chunked_array in zip(table.column_names, table.columns)
        if name in data_columns
    ]
    index_arrays = [
        chunked_array.combine_chunks()
        for name, chunked_array in zip(table.column_names, table.columns)
        if name in index_columns
    ]

    data_array = pa.StructArray.from_arrays(data_arrays, names=data_columns)

    new_table = pa.Table.from_arrays(index_arrays, names=index_columns)
    new_table = new_table.append_column(DATA, data_array)
    return new_table.replace_schema_metadata(table.schema.metadata)
