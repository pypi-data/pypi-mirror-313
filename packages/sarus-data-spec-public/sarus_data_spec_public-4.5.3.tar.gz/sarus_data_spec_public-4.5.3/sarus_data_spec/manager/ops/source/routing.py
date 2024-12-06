from typing import AsyncIterator
import logging
import typing as t

import pyarrow as pa

from sarus_data_spec.manager.ops.base import ScalarImplementation
import sarus_data_spec.typing as st

from .privacy_params import PrivacyParams
from .random_seed import RandomSeed

logger = logging.getLogger(__name__)

try:
    from sarus_data_spec.manager.ops.source.pretrained_model import (
        PretrainedModel,
    )
except ModuleNotFoundError:
    pass


try:
    from sarus_data_spec.manager.ops.source.sql_source import SourceSQL
except ModuleNotFoundError:
    logger.info(
        "sqlalquemy not installed, source SQL operations not available."
    )

try:
    from sarus_data_spec.manager.ops.source.csv.arrow import csv_to_arrow
    from sarus_data_spec.manager.ops.source.csv.schema import csv_schema
except ModuleNotFoundError:
    logger.info("CSV package not found, source CSV operations not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.synthetic_data.synthetic import (  # noqa: E501
        SyntheticModel,
    )
except ModuleNotFoundError:
    logger.info("Synthetic generation not available")

try:
    from sarus_data_spec.manager.ops.source.huggingface import (
        Huggingface,
        HuggingfaceStaticChecker,
    )
except ModuleNotFoundError:
    logging.info("Huggingface datasets not available.")


def get_scalar_op(scalar: st.Scalar) -> t.Type[ScalarImplementation]:
    if scalar.is_random_seed():
        return RandomSeed
    elif scalar.is_privacy_params():
        return PrivacyParams
    elif scalar.is_synthetic_model():
        return SyntheticModel
    elif scalar.is_pretrained_model():
        return PretrainedModel
    else:
        raise NotImplementedError(f"Source scalar for {scalar}")


class SourceScalar(ScalarImplementation):
    async def value(self) -> t.Any:
        OpClass = get_scalar_op(self.scalar)
        return await OpClass(self.scalar).value()


async def source_dataset_to_arrow(
    dataset: st.Dataset, batch_size: int
) -> AsyncIterator[pa.RecordBatch]:
    if dataset.is_file():
        file_format = dataset.protobuf().spec.file.format
        if file_format == "csv":
            return csv_to_arrow(dataset, batch_size=batch_size)
        else:
            raise NotImplementedError(f"File format {file_format}")

    elif dataset.protobuf().spec.HasField("sql"):
        return await SourceSQL(dataset=dataset).to_arrow(batch_size=batch_size)
    elif dataset.protobuf().spec.HasField("huggingface"):
        return await Huggingface(dataset=dataset).to_arrow(
            batch_size=batch_size
        )
    else:
        source_type = dataset.protobuf().spec.WhichOneof("spec")
        raise NotImplementedError(f"Source {source_type}")


async def source_dataset_schema(dataset: st.Dataset) -> st.Schema:
    if dataset.protobuf().spec.HasField("sql"):
        return await SourceSQL(dataset=dataset).schema()
    elif dataset.protobuf().spec.HasField("huggingface"):
        return await HuggingfaceStaticChecker(dataset=dataset).schema()
    elif dataset.is_file():
        file_format = dataset.protobuf().spec.file.format
        if file_format == "csv":
            return await csv_schema(dataset)
        else:
            raise NotImplementedError(f"File format {file_format}")
    else:
        raise NotImplementedError
