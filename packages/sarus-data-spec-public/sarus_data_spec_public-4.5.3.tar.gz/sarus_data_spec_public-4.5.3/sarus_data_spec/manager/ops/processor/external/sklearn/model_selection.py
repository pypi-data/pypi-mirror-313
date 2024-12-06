from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np
import numpy.typing as npt
import pandas as pd

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusParameterArray,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from sklearn import model_selection
    from sklearn.base import BaseEstimator
    from sklearn.model_selection import BaseCrossValidator, GridSearchCV
except ModuleNotFoundError:
    BaseEstimator = Any
    BaseCrossValidator = Any
    spmatrix = Any
    GridSearchCV = Any


class sk_kfold(ExternalOpImplementation):
    _transform_id = "sklearn.SK_KFOLD"
    _signature = SarusSignature(
        SarusParameter(
            name="n_splits",
            annotation=int,
            default=5,
        ),
        SarusParameter(
            name="shuffle",
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
        return model_selection.KFold(**kwargs)


class sk_repeated_stratified_kfold(ExternalOpImplementation):
    _transform_id = "sklearn.SK_REPEATED_STRATIFIED_KFOLD"
    _signature = SarusSignature(
        SarusParameter(
            name="n_splits",
            annotation=int,
            default=5,
        ),
        SarusParameter(
            name="n_repeats",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return model_selection.RepeatedStratifiedKFold(**kwargs)


class sk_cross_val_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_CROSS_VAL_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=npt.ArrayLike,
        ),
        SarusParameter(
            name="y",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="groups",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="scoring",
            annotation=Optional[Union[str, Callable]],
            default=None,
        ),
        SarusParameter(
            name="cv",
            annotation=Optional[Union[int, BaseCrossValidator, Iterable]],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="fit_params",
            annotation=Optional[Dict[str, Any]],
            default=None,
        ),
        SarusParameter(
            name="pre_dispatch",
            annotation=Optional[Union[str, int]],
            default="2*n_jobs",
        ),
        SarusParameter(
            name="error_score",
            annotation=Union[Literal["raise"], np.number],
            default=np.nan,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return model_selection.cross_val_score(**kwargs)


class sk_train_test_split(ExternalOpImplementation):
    _transform_id = "sklearn.SK_TRAIN_TEST_SPLIT"
    _signature = SarusSignature(
        SarusParameterArray(
            name="arrays",
            annotation=Sequence[
                Union[List, np.ndarray, spmatrix, pd.DataFrame]
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="test_size",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="train_size",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="shuffle",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="stratify",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        arrays, kwargs = signature.collect()
        return model_selection.train_test_split(*arrays, **kwargs)


class sk_time_series_split(ExternalOpImplementation):
    _transform_id = "sklearn.SK_TIME_SERIES_SPLIT"
    _signature = SarusSignature(
        SarusParameter(
            name="n_splits",
            annotation=int,
            default=5,
        ),
        SarusParameter(
            name="max_train_size",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="test_size",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="gap",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return model_selection.TimeSeriesSplit(**kwargs)


class SkGridSearchCV(ExternalOpImplementation):
    _transform_id = "sklearn.SK_GRID_SEARCH_CV"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=BaseEstimator,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="param_grid",
            annotation=Union[Dict[str, Any], List[Dict[str, Any]]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="scoring",
            annotation=Optional[Union[str, Callable, List, Tuple, Dict]],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="refit",
            annotation=Union[bool, str, Callable],
            default=True,
        ),
        SarusParameter(
            name="cv",
            annotation=Optional[Union[int, BaseCrossValidator, Iterable]],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="pre_dispatch",
            annotation=Union[str, int],
            default="2*n_jobs",
        ),
        SarusParameter(
            name="error_score",
            annotation=Union[Literal["raise"], np.number],
            default=np.nan,
        ),
        SarusParameter(
            name="return_train_score",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return model_selection.GridSearchCV(**kwargs)


class sk_best_params(ExternalOpImplementation):
    _transform_id = "sklearn.SK_BEST_PARAMS_"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GridSearchCV,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this = signature.collect_args()[0]
        return this.best_params_


class sk_best_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_BEST_SCORE_"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GridSearchCV,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this = signature.collect_args()[0]
        return this.best_score_
