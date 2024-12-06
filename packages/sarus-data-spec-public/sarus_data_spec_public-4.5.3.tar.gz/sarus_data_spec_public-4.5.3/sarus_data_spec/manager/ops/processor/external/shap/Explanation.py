from typing import Any, Dict, List, Optional, Union

import numpy.typing as npt

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from shap import Explanation
    import shap
except ModuleNotFoundError:
    spmatrix = Any
    Explanation = Any


# ------ CONSTRUCTORS -------
class shap_explanation(ExternalOpImplementation):
    _transform_id = "shap.SHAP_EXPLANATION"
    _signature = SarusSignature(
        SarusParameter(
            name="values",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="base_values",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="data",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="display_data",
            annotation=Optional[Dict[str, npt.ArrayLike]],
            default=None,
        ),
        SarusParameter(
            name="instance_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="output_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="output_indexes",
            annotation=Optional[List[int]],
            default=None,
        ),
        SarusParameter(
            name="lower_bounds",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="upper_bounds",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="error_std",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="main_effects",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="hierarchical_values",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="clustering",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
        ),
        SarusParameter(
            name="compute_time",
            annotation=Optional[float],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.Explanation(**kwargs)


# ------ Explanation METHODS ------


class shap_values(ExternalOpImplementation):
    _transform_id = "shap.SHAP_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explanation,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.values


class shap_sum(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SUM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explanation,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.sum()
