from typing import Final

from sarus_data_spec.attribute import Attribute
from sarus_data_spec.context import push_global_context
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.status import Status
from sarus_data_spec.transform import Transform
from sarus_data_spec.variant_constraint import VariantConstraint

__all__ = [
    "Attribute",
    "Dataset",
    "Scalar",
    "Status",
    "Transform",
    "VariantConstraint",
]

"""A library to manage Sarus datasets"""
# pylint: disable=unused-variable

PACKAGE_NAME: Final[str] = "sarus_data_spec"
VERSION: Final[str] = "4.5.3"

try:
    import sarus_data_spec.context.worker as sw

    push_global_context(sw.WorkerContext())
except ModuleNotFoundError as exception:
    if exception.name == "sarus_data_spec.context.worker":
        pass  # The worker context is absent from the public release
    else:
        raise exception
