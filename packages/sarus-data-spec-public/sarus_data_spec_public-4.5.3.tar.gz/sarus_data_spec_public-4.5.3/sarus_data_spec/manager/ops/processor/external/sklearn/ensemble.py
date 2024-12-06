from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from numpy.typing import ArrayLike
import numpy as np

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import ensemble
    from sklearn.base import BaseEstimator
    from sklearn.model_selection import BaseCrossValidator
except ModuleNotFoundError:
    BaseEstimator = Any
    BaseCrossValidator = Any


class sk_adaboost_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ADABOOST_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=Optional[BaseEstimator],
            default=None,
        ),
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=50,
        ),
        SarusParameter(
            name="learning_rate",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="algorithm",
            annotation=Literal["SAMME", "SAMME.R"],
            default="SAMME.R",
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.AdaBoostClassifier(**kwargs)


class sk_adaboost_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ADABOOST_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=Optional[BaseEstimator],
            default=None,
        ),
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=50,
        ),
        SarusParameter(
            name="learning_rate",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="loss",
            annotation=Literal["linear", "square", "exponential"],
            default="linear",
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.AdaBoostRegressor(**kwargs)


class sk_bagging_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_BAGGING_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=Optional[BaseEstimator],
            default=None,
        ),
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Union[int, float],
            default=1.0,
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[int, float],
            default=1.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="bootstrap_features",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="oob_score",
            annotation=bool,
            default=False,
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
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.BaggingClassifier(**kwargs)


class sk_bagging_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_BAGGING_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="estimator",
            annotation=Optional[BaseEstimator],
            default=None,
        ),
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Union[int, float],
            default=1.0,
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[int, float],
            default=1.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="bootstrap_features",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="oob_score",
            annotation=bool,
            default=False,
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
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.BaggingRegressor(**kwargs)


class sk_extra_trees_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_EXTRA_TREES_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="criterion",
            annotation=Literal["gini", "entropy", "log_loss"],
            default="gini",
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[Literal["sqrt", "log2"], int, float, None],
            default="sqrt",
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="oob_score",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
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
            name="class_weight",
            annotation=Union[
                Literal["balanced", "balanced_subsample"], dict, list
            ],
            default=None,
        ),
        SarusParameter(
            name="ccp_alpha",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Optional[Union[int, float]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.ExtraTreesClassifier(**kwargs)


class sk_extra_trees_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_EXTRA_TREES_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="criterion",
            annotation=Literal[
                "squared_error", "absolute_error", "friedman_mse", "poisson"
            ],
            default="squared_error",
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[Literal["sqrt", "log2", None], int, float],
            default=1.0,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="oob_score",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
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
            name="ccp_alpha",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Optional[Union[int, float]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.ExtraTreesRegressor(**kwargs)


class sk_gradient_boosting_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_GRADIENT_BOOSTING_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="loss",
            annotation=Literal["deviance", "exponential", "log_loss"],
            default="log_loss",
        ),
        SarusParameter(
            name="learning_rate",
            annotation=float,
            default=0.1,
        ),
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="subsample",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="criterion",
            annotation=Literal["friedman_mse", "squared_error"],
            default="friedman_mse",
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=3,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="init",
            annotation=Optional[Union[BaseEstimator, Literal["zero"]]],
            default=None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[
                Literal["auto", "sqrt", "log2"], int, float, None
            ],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="validation_fraction",
            annotation=float,
            default=0.1,
        ),
        SarusParameter(
            name="n_iter_no_change",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=1e-4,
        ),
        SarusParameter(
            name="ccp_alpha",
            annotation=float,
            default=0.0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.GradientBoostingClassifier(**kwargs)


class sk_gradient_boosting_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_GRADIENT_BOOSTING_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="loss",
            annotation=Literal[
                "squared_error",
                "absolute_error",
                "huber",
                "quantile",
            ],
            default="squared_error",
        ),
        SarusParameter(
            name="learning_rate",
            annotation=float,
            default=0.1,
        ),
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="subsample",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="criterion",
            annotation=Literal["friedman_mse", "squared_error"],
            default="friedman_mse",
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=3,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="init",
            annotation=Optional[Union[BaseEstimator, Literal["zero"]]],
            default=None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="max_features",
            annotation=Optional[
                Union[Literal["auto", "sqrt", "log2"], int, float]
            ],
            default=None,
        ),
        SarusParameter(
            name="alpha",
            annotation=float,
            default=0.9,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="validation_fraction",
            annotation=float,
            default=0.1,
        ),
        SarusParameter(
            name="n_iter_no_change",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=1e-4,
        ),
        SarusParameter(
            name="ccp_alpha",
            annotation=float,
            default=0.0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.GradientBoostingRegressor(**kwargs)


class sk_isolation_forest(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ISOLATION_FOREST"
    _signature = SarusSignature(
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Union[Literal["auto"], int, float],
            default="auto",
        ),
        SarusParameter(
            name="contamination",
            annotation=Union[Literal["auto"], float],
            default="auto",
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[int, float],
            default=1.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=False,
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
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.IsolationForest(**kwargs)


class sk_random_forest_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_RANDOM_FOREST_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="criterion",
            annotation=Literal["gini", "entropy", "log_loss"],
            default="gini",
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_features",
            annotation=Union[Literal["sqrt", "log2", None], int, float],
            default="sqrt",
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="oob_score",
            annotation=bool,
            default=False,
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
            name="class_weight",
            annotation=Optional[
                Union[
                    Literal["balanced", "balanced_subsample"], Dict, List[Dict]
                ]
            ],
            default=None,
        ),
        SarusParameter(
            name="ccp_alpha",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Optional[Union[int, float]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.RandomForestClassifier(**kwargs)


class sk_random_forest_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_RANDOM_FOREST_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="criterion",
            annotation=Literal[
                "squared_error", "absolute_error", "friedman_mse", "poisson"
            ],
            default="squared_error",
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_features",
            annotation=Optional[Union[Literal["sqrt", "log2"], int, float]],
            default=1.0,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="bootstrap",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="oob_score",
            annotation=bool,
            default=False,
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
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="warm_start",
            annotation=Optional[bool],
            default=False,
        ),
        SarusParameter(
            name="ccp_alpha",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Optional[Union[int, float]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.RandomForestRegressor(**kwargs)


class sk_random_trees_embedding(ExternalOpImplementation):
    _transform_id = "sklearn.SK_RANDOM_TREES_EMBEDDING"
    _signature = SarusSignature(
        SarusParameter(
            name="n_estimators",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="max_depth",
            annotation=int,
            default=5,
        ),
        SarusParameter(
            name="min_samples_split",
            annotation=Union[int, float],
            default=2,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=Union[int, float],
            default=1,
        ),
        SarusParameter(
            name="min_weight_fraction_leaf",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_impurity_decrease",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="sparse_output",
            annotation=bool,
            default=True,
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
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.RandomTreesEmbedding(**kwargs)


class sk_stacking_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_STACKING_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="estimators",
            annotation=List[Tuple[str, BaseEstimator]],
        ),
        SarusParameter(
            name="final_estimator",
            annotation=Optional[BaseEstimator],
            default=None,
        ),
        SarusParameter(
            name="cv",
            annotation=Union[
                int, BaseCrossValidator, Iterable, Literal["prefit"]
            ],
            default=None,
        ),
        SarusParameter(
            name="stack_method",
            annotation=Literal[
                "auto", "predict_proba", "decision_function", "predict"
            ],
            default="auto",
        ),
        SarusParameter(
            name="n_jobs",
            annotation=int,
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="passthrough",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.StackingClassifier(**kwargs)


class sk_stacking_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_STACKING_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="estimators",
            annotation=List[Tuple[str, BaseEstimator]],
        ),
        SarusParameter(
            name="final_estimator",
            annotation=Optional[BaseEstimator],
            default=None,
        ),
        SarusParameter(
            name="cv",
            annotation=Optional[Union[int, BaseCrossValidator, Iterable[str]]],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="passthrough",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.StackingRegressor(**kwargs)


class sk_voting_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_VOTING_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="estimators",
            annotation=List[Tuple[str, BaseEstimator]],
            default=None,
        ),
        SarusParameter(
            name="voting",
            annotation=Literal["hard", "soft"],
            default="hard",
        ),
        SarusParameter(
            name="weights",
            annotation=Optional[List[float]],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="flatten_transform",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.VotingClassifier(**kwargs)


class sk_voting_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_VOTING_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="estimators",
            annotation=List[Tuple[str, BaseEstimator]],
        ),
        SarusParameter(
            name="weights",
            annotation=Optional[List[float]],
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
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.VotingRegressor(**kwargs)


class sk_hist_gradient_boosting_classifier(ExternalOpImplementation):
    _transform_id = "sklearn.SK_HIST_GRADIENT_BOOSTING_CLASSIFIER"
    _signature = SarusSignature(
        SarusParameter(
            name="loss",
            annotation=Literal[
                "log_loss",
                "auto",
                "binary_crossentropy",
                "categorical_crossentropy",
            ],
            default="log_loss",
        ),
        SarusParameter(
            name="learning_rate",
            annotation=float,
            default=0.1,
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=31,
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=int,
            default=20,
        ),
        SarusParameter(
            name="l2_regularization",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="max_bins",
            annotation=int,
            default=255,
        ),
        SarusParameter(
            name="categorical_features",
            annotation=Optional[ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="monotonic_cst",
            annotation=Optional[Union[ArrayLike, Dict]],
            default=None,
        ),
        SarusParameter(
            name="interaction_cst",
            annotation=Optional[
                Union[
                    Literal["pairwise", "no_interaction"],
                    Sequence[Union[List[int], Tuple[int], Set[int]]],
                ]
            ],
            default=None,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="early_stopping",
            annotation=Union[Literal["auto"], bool],
            default="auto",
        ),
        SarusParameter(
            name="scoring",
            annotation=Optional[Union[str, Callable, None]],
            default="loss",
        ),
        SarusParameter(
            name="validation_fraction",
            annotation=Optional[Union[int, float]],
            default=0.1,
        ),
        SarusParameter(
            name="n_iter_no_change",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=1e-7,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="class_weight",
            annotation=Optional[Union[str, dict]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.HistGradientBoostingClassifier(**kwargs)


class sk_hist_gradient_boosting_regressor(ExternalOpImplementation):
    _transform_id = "sklearn.SK_HIST_GRADIENT_BOOSTING_REGRESSOR"
    _signature = SarusSignature(
        SarusParameter(
            name="loss",
            annotation=Literal[
                "squared_error", "absolute_error", "poisson", "quantile"
            ],
            default="squared_error",
        ),
        SarusParameter(
            name="quantile",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="learning_rate",
            annotation=float,
            default=0.1,
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="max_leaf_nodes",
            annotation=Optional[int],
            default=31,
        ),
        SarusParameter(
            name="max_depth",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_samples_leaf",
            annotation=int,
            default=20,
        ),
        SarusParameter(
            name="l2_regularization",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="max_bins",
            annotation=int,
            default=255,
        ),
        SarusParameter(
            name="categorical_features",
            annotation=Optional[
                Union[Sequence[Union[bool, int, str]], Sequence[int]]
            ],
            default=None,
        ),
        SarusParameter(
            name="monotonic_cst",
            annotation=Optional[Union[Sequence[int], Dict[int, int]]],
            default=None,
        ),
        SarusParameter(
            name="interaction_cst",
            annotation=Optional[
                Union[
                    Literal["pairwise", "no_interaction"],
                    Sequence[Union[List[int], Tuple[int], Set[int]]],
                ]
            ],
            default=None,
        ),
        SarusParameter(
            name="warm_start",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="early_stopping",
            annotation=Union[Literal["auto"], bool],
            default="auto",
        ),
        SarusParameter(
            name="scoring",
            annotation=Optional[Union[str, Callable]],
            default="loss",
        ),
        SarusParameter(
            name="n_iter_no_change",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=1e-7,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ensemble.HistGradientBoostingRegressor(**kwargs)
