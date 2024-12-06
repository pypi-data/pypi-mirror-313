import pyarrow as pa
import typing as t
import sarus_data_spec.typing as st
from sarus_data_spec.manager.ops.processor.standard.visitor_selector import (
    select_columns,
)
from sarus_data_spec.constants import DATA
from sarus_data_spec.arrow.pandas_utils import pandas_index_columns


def convert_record_batch(
    record_batch: pa.RecordBatch, _type: st.Type
) -> pa.Array:
    if str(_type.protobuf().WhichOneof("type")) not in ["struct", "union"]:
        return record_batch.column(0)
    record_schema = record_batch.schema
    fields = [record_schema.field(i) for i in range(len(record_schema.types))]
    return pa.StructArray.from_arrays(record_batch.columns, fields=fields)


async def fit_array_to_schema_type_async_gen(
    batch_async_iterator: t.AsyncIterator[pa.RecordBatch], schema_type: st.Type
) -> t.AsyncIterator[pa.RecordBatch]:
    """It makes sure that each pyarrow recordbatch is conform to the schema
    type provided.
    """
    async for batch in batch_async_iterator:
        if schema_type.has_admin_columns():
            assert DATA in batch.schema.names

        # retrieve pandas index that may not be present in the schema type
        field_names = list(batch.schema.names)

        # select columns present in the schema type.
        # it fails if columns in the schema are not in the array
        updated_array = select_columns(
            schema_type,
            convert_record_batch(record_batch=batch, _type=schema_type),
        )
        updated_batch = pa.RecordBatch.from_struct_array(updated_array)

        index_cols = [
            col
            for col in pandas_index_columns(batch.schema)
            if col not in list(updated_batch.schema.names)
        ]
        index_arrays = [
            batch.columns[field_names.index(col)] for col in index_cols
        ]
        if len(index_cols) > 0:
            # add index cols
            updated_field_names = list(updated_batch.schema.names)
            arrays = index_arrays + updated_batch.columns
            names = index_cols + updated_field_names
            new_struct_array = pa.StructArray.from_arrays(arrays, names)
            updated_batch = pa.RecordBatch.from_struct_array(new_struct_array)

        updated_batch = updated_batch.replace_schema_metadata(
            batch.schema.metadata
        )
        yield updated_batch
