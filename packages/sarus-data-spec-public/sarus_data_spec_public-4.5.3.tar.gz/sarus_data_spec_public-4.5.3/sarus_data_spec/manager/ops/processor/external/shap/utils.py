from typing import Any, List, Optional

import numpy as np

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    import shap
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class shap_hclust(ExternalOpImplementation):
    _transform_id = "shap.SHAP_HCLUST"
    _signature = SarusSignature(
        SarusParameter(
            name="X",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y",
            annotation=Optional[Any],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="linkage",
            annotation=str,
            default="single",
        ),
        SarusParameter(
            name="metric",
            annotation=str,
            default="auto",
        ),
        SarusParameter(
            name="random_state",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.hclust(**kwargs)


class shap_hclust_ordering(ExternalOpImplementation):
    _transform_id = "shap.SHAP_HCLUST_ORDERING"
    _signature = SarusSignature(
        SarusParameter(
            name="X",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="metric",
            annotation=str,
            default="sqeuclidean",
        ),
        SarusParameter(
            name="anchor_first",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.hclust_ordering(**kwargs)


class shap_partition_tree(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PARTITION_TREE"
    _signature = SarusSignature(
        SarusParameter(
            name="X",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="metric",
            annotation=str,
            default="correlation",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.partition_tree(**kwargs)


class shap_partition_tree_shuffle(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PARTITION_TREE_SHUFFLE"
    _signature = SarusSignature(
        SarusParameter(
            name="indexes",
            annotation=np.array,
        ),
        SarusParameter(
            name="index_mask",
            annotation=np.array,
        ),
        SarusParameter(
            name="partition_tree",
            annotation=np.array,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.partition_tree_shuffle(**kwargs)


class shap_delta_minimization_order(ExternalOpImplementation):
    _transform_id = "shap.SHAP_DELTA_MINIMIZATION_ORDER"
    _signature = SarusSignature(
        SarusParameter(
            name="all_masks",
            annotation=Any,
        ),
        SarusParameter(
            name="max_swap_size",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="num_passes",
            annotation=int,
            default=2,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.delta_minimization_order(**kwargs)


class shap_approximate_interactions(ExternalOpImplementation):
    _transform_id = "shap.SHAP_APPROXIMATE_INTERACTIONS"
    _signature = SarusSignature(
        SarusParameter(
            name="index",
            annotation=Any,
        ),
        SarusParameter(
            name="shap_values",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.approximate_interactions(**kwargs)


class shap_potential_interactions(ExternalOpImplementation):
    _transform_id = "shap.SHAP_POTENTIAL_INTERACTIONS"
    _signature = SarusSignature(
        SarusParameter(
            name="shap_values_column",
            annotation=Any,
            condition=STATIC,
        ),
        SarusParameter(
            name="shap_values_matrix",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        args = signature.collect_args()
        return shap.utils.potential_interactions(*args)


class shap_sample(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SAMPLE"
    _signature = SarusSignature(
        SarusParameter(
            name="X",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="nsamples",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="random_state",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.utils.sample(**kwargs)


class shap_convert_name(ExternalOpImplementation):
    _transform_id = "shap.SHAP_CONVERT_NAME"
    _signature = SarusSignature(
        SarusParameter(
            name="ind",
            annotation=Any,
        ),
        SarusParameter(
            name="shap_values",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="input_names",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        args = signature.collect_args()
        return shap.utils.convert_name(*args)
