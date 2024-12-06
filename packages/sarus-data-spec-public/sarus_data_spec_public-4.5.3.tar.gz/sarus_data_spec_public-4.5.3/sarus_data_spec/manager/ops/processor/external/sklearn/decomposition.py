from typing import Any, Literal, Optional, Union

import numpy as np

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import decomposition
except ModuleNotFoundError:
    pass  # error message in typing.py


class sk_pca(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PCA"
    _signature = SarusSignature(
        SarusParameter(
            name="n_components",
            annotation=Optional[Union[int, float, Literal["mle"]]],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="whiten",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="svd_solver",
            annotation=Literal["auto", "full", "arpack", "randomized"],
            default="auto",
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="iterated_power",
            annotation=Union[int, Literal["auto"]],
            default="auto",
        ),
        SarusParameter(
            name="n_oversamples",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="power_iteration_normalizer",
            annotation=Literal["auto", "QR", "LU", "none"],
            default="auto",
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return decomposition.PCA(**kwargs)
