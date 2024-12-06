from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt
import pandas as pd

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import inspection
    from sklearn.base import BaseEstimator
except ModuleNotFoundError:
    BaseEstimator = Any


class sk_permutation_importance(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PERMUTATION_IMPORTANCE"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
        ),
        SarusParameter(
            name="y",
            annotation=Optional[npt.ArrayLike],
        ),
        SarusParameter(
            name="scoring",
            annotation=Optional[
                Union[
                    str,
                    Callable,
                    List,
                    Tuple,
                    Dict,
                ]
            ],
            default=None,
        ),
        SarusParameter(
            name="n_repeats",
            annotation=int,
            default=5,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Union[int, float],
            default=1.0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return inspection.permutation_importance(**kwargs)
