from typing import Any, Literal, Optional, Union

import numpy as np

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import svm
except ModuleNotFoundError:
    pass  # error message in typing.py


class sk_svc(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SVC"
    _signature = SarusSignature(
        SarusParameter(
            name="C",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="kernel",
            annotation=Union[
                Literal["linear", "poly", "rbf", "sigmoid", "precomputed"],
                callable,
            ],
            default="rbf",
        ),
        SarusParameter(
            name="degree",
            annotation=int,
            default=3,
        ),
        SarusParameter(
            name="gamma",
            annotation=Union[Literal["scale", "auto"], float],
            default="scale",
        ),
        SarusParameter(
            name="coef0",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="shrinking",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="probability",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=1e-3,
        ),
        SarusParameter(
            name="cache_size",
            annotation=float,
            default=200,
        ),
        SarusParameter(
            name="class_weight",
            annotation=Optional[Union[Literal["balanced"], dict]],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=-1,
        ),
        SarusParameter(
            name="decision_function_shape",
            annotation=Literal["ovo", "ovr"],
            default="ovr",
        ),
        SarusParameter(
            name="break_ties",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return svm.SVC(**kwargs)
