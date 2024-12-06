from importlib import import_module
from typing import Dict, List, Optional, Type, cast
import inspect

from .typing import NO_TRANSFORM_ID, ExternalOpImplementation

MODULES = [
    "pandas",
    "sklearn",
    "numpy",
    "imblearn",
    "pandas_profiling",
    "skopt",
    "std",
    "xgboost",
    "shap",
    "scipy",
    "optbinning",
]


def op_name(module_name: str, transform_id: str) -> str:
    """Extract the last part of a transform ID.

    Example: sklearn.SK_FIT -> SK_FIT.
    """
    mod_name, op_name = transform_id.split(".")
    assert module_name == mod_name
    return op_name


def valid_ops(module_name: str) -> List[ExternalOpImplementation]:
    """Get all ExternalOpImplementation from a module."""

    module = import_module(
        f"sarus_data_spec.manager.ops.processor.external.{module_name}"
    )
    members = inspect.getmembers(
        module,
        lambda __obj: inspect.isclass(__obj)
        and issubclass(__obj, ExternalOpImplementation),
    )
    ops_classes = [
        cast(Type[ExternalOpImplementation], op) for _, op in members
    ]
    ops_instances = [op_class() for op_class in ops_classes]
    valid_ops = [
        op for op in ops_instances if op.transform_id() != NO_TRANSFORM_ID
    ]
    return valid_ops


def ops_mapping(module_name: str) -> Dict[str, ExternalOpImplementation]:
    """Get all ExternalOpImplementation from a module.

    Return a Mapping (op_name -> op_implementation).
    """
    ops_mapping = {
        op_name(module_name, op.transform_id()): op
        for op in valid_ops(module_name)
    }
    return ops_mapping


def replace_none(x: Optional[str]) -> str:
    return x if x else ""


_INITIALIZED = globals().get("_INITIALIZED", False)

if not _INITIALIZED:
    ROUTING = {
        module_name: ops_mapping(module_name) for module_name in MODULES
    }

    # These are lists of PUP and DP transforms. They are mappings {OP_ID:
    # DOCSTRING}. The docstrings are displayed in the documentation to explain
    # under which condition the op is PUP or DP.

    ALL_OPS: List[ExternalOpImplementation] = sum(
        [valid_ops(module_name) for module_name in MODULES], []
    )
    PUP_TRANSFORMS = {
        op.transform_id(): replace_none(op.pup_kind.__doc__)
        for op in ALL_OPS
        if op.pup_kind.__doc__ != ExternalOpImplementation.pup_kind.__doc__
    }

    DP_TRANSFORMS = {
        op.transform_id(): replace_none(
            cast(ExternalOpImplementation, op.dp_equivalent()).is_dp.__doc__
        )
        for op in ALL_OPS
        if op.dp_equivalent_id() is not None
    }
    _INITIALIZED = True  # Set the flag to True after initialization
