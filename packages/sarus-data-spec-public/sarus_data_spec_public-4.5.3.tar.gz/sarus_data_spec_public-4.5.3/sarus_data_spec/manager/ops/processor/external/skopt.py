from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from .external_op import ExternalOpImplementation

try:
    from sklearn.base import BaseEstimator
    from sklearn.model_selection import BaseCrossValidator
    import skopt
except ModuleNotFoundError:
    BaseEstimator = Any
    BaseCrossValidator = Any


class skopt_bayes_search_cv(ExternalOpImplementation):
    _transform_id = "skopt.SKOPT_BAYES_SEARCH_CV"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="search_spaces",
            annotation=Union[Dict, List[Union[Dict, Tuple]]],
        ),
        SarusParameter(
            name="n_iter",
            annotation=int,
            default=50,
        ),
        SarusParameter(
            name="optimizer_kwargs",
            annotation=Optional[Dict],
            default=None,
        ),
        SarusParameter(
            name="scoring",
            annotation=Optional[Union[str, Callable]],
            default=None,
        ),
        SarusParameter(
            name="fit_params",
            annotation=Optional[Dict],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=int,
            default=1,
            predicate=lambda x: bool(x < 4),
        ),
        SarusParameter(
            name="n_points",
            annotation=int,
            default=1,
        ),
        SarusParameter(
            name="pre_dispatch",
            annotation=Optional[Union[int, str]],
            default="2*n_jobs",
        ),
        SarusParameter(
            name="iid",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="cv",
            annotation=Optional[Union[int, BaseCrossValidator, Iterable]],
            default=None,
        ),
        SarusParameter(
            name="refit",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="random_state",
            annotation=Union[int, np.random.RandomState],
            default=None,
        ),
        SarusParameter(
            name="error_score",
            annotation=Union[str, float],
            default="raise",
        ),
        SarusParameter(
            name="return_train_score",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return skopt.BayesSearchCV(**kwargs)
