from typing import Any, Callable, List, Optional, Tuple, Union

from numpy import ndarray
from pandas import DataFrame
import numpy as np
import pandas as pd

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from shap import (
        Explainer,
        KernelExplainer,
        LinearExplainer,
        SamplingExplainer,
    )
    from shap.maskers import Masker
    from shap.models import Model
    from sklearn.base import BaseEstimator
    import shap
except ModuleNotFoundError:
    Explainer = Any
    KernelExplainer = Any
    LinearExplainer = Any
    SamplingExplainer = Any
    spmatrix = Any
    Masker = Any
    Model = Any
    BaseEstimator = Any

# ------ CONSTRUCTORS -------


class shap_explainer(ExternalOpImplementation):
    _transform_id = "shap.SHAP_EXPLAINER"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[Callable, BaseEstimator],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="masker",
            annotation=Optional[Union[Callable, ndarray, DataFrame]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="link",
            annotation=Optional[Callable],
            default=None,
        ),
        SarusParameter(
            name="algorithm",
            annotation=str,
            default="auto",
        ),
        SarusParameter(
            name="output_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="linearize_link",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="seed",
            annotation=Optional[int],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.Explainer(**kwargs)


# ------ SHAP EXPLAINER METHODS ------


class shap_save(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SAVE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explainer,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="out_file",
            annotation=Any,
            condition=STATIC,
        ),
        SarusParameter(
            name="model_saver",
            annotation=str,
            default=".save",
        ),
        SarusParameter(
            name="masker_saver",
            annotation=str,
            default=".save",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.save(**kwargs)


class shap_load(ExternalOpImplementation):
    _transform_id = "shap.SHAP_LOAD"
    _signature = SarusSignature(
        SarusParameter(
            name="in_file",
            annotation=Any,
            condition=STATIC,
        ),
        SarusParameter(
            name="model_loader",
            annotation=Callable,
            default=Any,
            condition=STATIC,
        ),
        SarusParameter(
            name="masker_loader",
            annotation=Callable,
            default=Any,
            condition=STATIC,
        ),
        SarusParameter(
            name="instantiate",
            annotation=bool,
            default=True,
            condition=STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.Explainer.load(**kwargs)


class SHAP_explain_row(ExternalOpImplementation):
    _transform_id = "shap.SHAP_EXPLAIN_ROW"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explainer,
            condition=STATIC | DATASPEC,
        ),
        SarusParameter(
            name="row_args",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="max_evals",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="main_effects",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="error_bounds",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="batch_size",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="outputs",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="silent",
            annotation=bool,
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.explain_row(**kwargs)


class shap_shap_values(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SHAP_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shap_values(**kwargs)


class shap_call(ExternalOpImplementation):
    _transform_id = "shap.SHAP_CALL"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[ndarray, DataFrame],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        return this(kwargs["X"])


# ------ CONSTRUCTORS TREE -------


class shap_tree(ExternalOpImplementation):
    _transform_id = "shap.SHAP_TREE"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="data",
            annotation=Optional[Union[ndarray, DataFrame]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="model_output",
            annotation=str,
            default="raw",
            condition=STATIC,
        ),
        SarusParameter(
            name="feature_perturbation",
            annotation=str,
            default="interventional",
            condition=STATIC,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
            condition=STATIC,
        ),
        SarusParameter(
            name="approximate",
            annotation=bool,
            default=False,
            condition=STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.explainers.Tree(**kwargs)


# ------ CONSTRUCTORS GPUTREE -------


class shap_gputree(ExternalOpImplementation):
    _transform_id = "shap.SHAP_GPUTREE"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="data",
            annotation=Optional[Union[np.ndarray, pd.DataFrame]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="model_output",
            annotation=str,
            default="raw",
        ),
        SarusParameter(
            name="feature_perturbation",
            annotation=str,
            default="interventional",
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="approximate",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.explainers.GPUTree(**kwargs)


# ------ SHAP TREE AND GPUTREE METHODS ------


class shap_tree_shap_values(ExternalOpImplementation):
    _transform_id = "shap.SHAP_TREE_SHAP_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y",
            annotation=Optional[np.ndarray],
            default=None,
        ),
        SarusParameter(
            name="tree_limit",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="approximate",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="check_additivity",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="from_call",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shap_values(**kwargs)


class shap_tree_interaction_values(ExternalOpImplementation):
    _transform_id = "shap.SHAP_TREE_SHAP_INTERACTION_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Explainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y",
            annotation=Optional[np.ndarray],
            default=None,
        ),
        SarusParameter(
            name="tree_limit",
            annotation=Optional[int],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shap_interaction_values(**kwargs)


# ------ CONSTRUCTORS KERNEL -------


class shap_kernel(ExternalOpImplementation):
    _transform_id = "shap.SHAP_KERNEL"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Callable,
            condition=DATASPEC | STATIC,
            predicate=lambda x: isinstance(x, str),
        ),
        SarusParameter(
            name="data",
            annotation=Union[np.ndarray, pd.DataFrame, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="link",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.KernelExplainer(**kwargs)


# ------ SHAP KERNEL METHODS ------


class shap_run(ExternalOpImplementation):
    _transform_id = "shap.SHAP_RUN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=KernelExplainer,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.run()


class shap_allocate(ExternalOpImplementation):
    _transform_id = "shap.SHAP_ALLOCATE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=KernelExplainer,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.allocate()


class shap_solve(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SOLVE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=KernelExplainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="fraction_evaluated",
            annotation=Any,
            condition=STATIC,
        ),
        SarusParameter(
            name="dim",
            annotation=Any,
            condition=STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.solve(**kwargs)


class shap_varying_groups(ExternalOpImplementation):
    _transform_id = "shap.SHAP_VARYING_GROUPS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=KernelExplainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.varying_groups(**kwargs)


class shap_explain(ExternalOpImplementation):
    _transform_id = "shap.SHAP_EXPLAIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=KernelExplainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="incoming_instance",
            annotation=Any,
            condition=STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.explain(**kwargs)


class add_sample(ExternalOpImplementation):
    _transform_id = "shap.SHAP_ADD_SAMPLE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=KernelExplainer,
            condition=STATIC | DATASPEC,
        ),
        SarusParameter(
            name="x",
            annotation=np.array,
        ),
        SarusParameter(
            name="m",
            annotation=np.array,
        ),
        SarusParameter(
            name="w",
            annotation=float,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.addsample(**kwargs)


# ------ CONSTRUCTORS LINEAR -------


class shap_linear(ExternalOpImplementation):
    _transform_id = "shap.SHAP_LINEAR"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="masker",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="link",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="nsamples",
            annotation=int,
            default=1000,
        ),
        SarusParameter(
            name="feature_perturbation",
            annotation=Optional[str],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.explainers.Linear(**kwargs)


# ------ CONSTRUCTORS PARTITION -------
class shap_partition(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PARTITION"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="masker",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="output_names",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="link",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="nsamples",
            annotation=int,
            default=1000,
        ),
        SarusParameter(
            name="feature_perturbation",
            annotation=Optional[str],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.explainers.Partition(**kwargs)


# ------ CONSTRUCTORS PERMUTATION -------


class shap_permutation(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PERMUTATION"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="masker",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="output_names",
            annotation=Optional[List[str]],
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="link",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="linearize_link",
            annotation=bool,
            condition=STATIC,
            default=True,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="nsamples",
            annotation=int,
            default=1000,
        ),
        SarusParameter(
            name="feature_perturbation",
            annotation=Optional[str],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.explainers.Permutation(**kwargs)


# ------ SHAP PERMUTATION METHODS ------


class shap_permutation_explainer_shap_values(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PERMUTATION_SHAP_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=LinearExplainer,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="npermutations",
            annotation=Optional[int],
            default=10,
        ),
        SarusParameter(
            name="main_effects",
            annotation=Optional[bool],
            default=False,
        ),
        SarusParameter(
            name="error_bounds",
            annotation=Optional[bool],
            default=False,
        ),
        SarusParameter(
            name="batch_evals",
            annotation=Optional[bool],
            default=True,
        ),
        SarusParameter(
            name="silent",
            annotation=Optional[bool],
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shap_values(**kwargs)


# ------ CONSTRUCTORS SAMPLING -------


class shap_sampling(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SAMPLING"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="data",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.explainers.Sampling(**kwargs)


# ------ SHAP SAMPLING METHODS ------


class shap_sampling_estimate(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SAMPLING_ESTIMATE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=SamplingExplainer,
            condition=STATIC | DATASPEC,
        ),
        SarusParameter(
            name="j",
            annotation=int,
        ),
        SarusParameter(
            name="f",
            annotation=Callable,
        ),
        SarusParameter(
            name="x",
            annotation=Union[pd.Series, pd.DataFrame, np.ndarray],
        ),
        SarusParameter(
            name="X",
            annotation=Union[pd.Series, pd.DataFrame, np.ndarray],
        ),
        SarusParameter(
            name="nsamples",
            annotation=Optional[int],
            default=10,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.sampling_estimate(**kwargs)


# ------ CONSTRUCTORS EXACT -------
class shap_exact(ExternalOpImplementation):
    _transform_id = "shap.SHAP_EXACT"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="masker",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="link",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="linearize_link",
            annotation=bool,
            condition=STATIC,
            default=True,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            condition=STATIC,
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.explainers.Exact(**kwargs)


# ------ CONSTRUCTORS ADDIDTIVE -------
class shap_additive(ExternalOpImplementation):
    _transform_id = "shap.SHAP_ADDITIVE"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="masker",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="link",
            annotation=Any,
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            condition=STATIC,
            default=None,
        ),
        SarusParameter(
            name="linearize_link",
            annotation=Optional[bool],
            condition=STATIC,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["link"] is None:
            del kwargs["link"]
        return shap.explainers.Additive(**kwargs)


# ------ CONSTRUCTORS DEEP -------
class shap_deep(ExternalOpImplementation):
    _transform_id = "shap.SHAP_DEEP"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="data",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="session",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="learning_phase_flags",
            annotation=Any,
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.explainers.Deep(**kwargs)


# ------ CONSTRUCTORS GRADIENT -------
class shap_gradient(ExternalOpImplementation):
    _transform_id = "shap.SHAP_GRADIENT"
    _signature = SarusSignature(
        SarusParameter(
            name="model",
            annotation=Union[BaseEstimator, Tuple[Any, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="data",
            annotation=Union[
                Tuple[Any, Any], np.ndarray, pd.DataFrame, spmatrix
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="session",
            annotation=Any,
            default=None,
        ),
        SarusParameter(
            name="batch_size",
            annotation=int,
            default=50,
        ),
        SarusParameter(
            name="local_smoothing",
            annotation=Optional[float],
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.GradientExplainer(**kwargs)
