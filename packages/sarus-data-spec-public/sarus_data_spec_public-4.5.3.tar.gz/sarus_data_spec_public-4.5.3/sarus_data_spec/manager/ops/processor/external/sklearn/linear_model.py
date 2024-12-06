from typing import Any, Optional

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import linear_model
except ModuleNotFoundError:
    pass  # error message in typing.py


class sk_linear_regression(ExternalOpImplementation):
    _transform_id = "sklearn.SK_LINEAR_REGRESSION"
    _signature = SarusSignature(
        SarusParameter(
            name="fit_intercept",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="copy_X",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="positive",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return linear_model.LinearRegression(**kwargs)


class sk_logistic_regression(ExternalOpImplementation):
    _transform_id = "sklearn.SK_LOGISTIC_REGRESSION"
    _signature = SarusSignature(
        SarusParameter(
            name="penalty",
            annotation=str,
            default="l2",
        ),
        SarusParameter(
            name="dual",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=0.0001,
        ),
        SarusParameter(
            name="C",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="fit_intercept",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="intercept_scaling",
            annotation=int,
            default=1,
        ),
        SarusParameter(
            name="class_weight",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="solver",
            annotation=str,
            default="lbfgs",
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="multi_class",
            annotation=str,
            default="auto",
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="l1_ratio",
            annotation=Optional[float],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return linear_model.LogisticRegression(**kwargs)
