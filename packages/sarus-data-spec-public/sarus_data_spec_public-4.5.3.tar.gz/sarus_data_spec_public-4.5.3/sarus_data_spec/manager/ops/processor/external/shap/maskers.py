from typing import Any, Callable, Dict, Optional, Union

import numpy as np
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
    from shap.maskers import (
        Composite,
        Image,
        Independent,
        Masker,
        Partition,
        Text,
    )
    import shap
except ModuleNotFoundError:
    Independent = Any
    Partition = Any
    Text = Any
    Composite = Any
    Masker = Any
    Text = Any
    Image = Any


# ------ CONSTRUCTORS -------
class shap_masker(ExternalOpImplementation):
    _transform_id = "shap.SHAP_MASKER"
    _signature = SarusSignature()

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.Masker(**kwargs)


# ------ CONSTRUCTORS -------


class shap_independent(ExternalOpImplementation):
    _transform_id = "shap.SHAP_INDEPENDENT"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="max_samples",
            annotation=Optional[int],
            default=100,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.Independent(**kwargs)


# ------ Independent METHODS ------


class shap_invariants(ExternalOpImplementation):
    _transform_id = "shap.SHAP_INVARIANTS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Independent,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="x",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.invariants(**kwargs)


# ------ CONSTRUCTORS -------
class shap_masker_partition(ExternalOpImplementation):
    _transform_id = "shap.SHAP_MASKER_PARTITION"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=Union[np.ndarray, pd.DataFrame],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="max_samples",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="clustering",
            annotation=str,
            default="correlation",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.Partition(**kwargs)


# ------ Partition METHODS ------


class shap_partition_invariants(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PARTITION_INVARIANTS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Partition,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="x",
            annotation=np.ndarray,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.invariants(**kwargs)


# ------ CONSTRUCTORS -------
class shap_impute(ExternalOpImplementation):
    _transform_id = "shap.SHAP_IMPUTE"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=Union[np.ndarray, pd.DataFrame, Dict[str, np.ndarray]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="method",
            annotation=str,
            default="linear",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.Impute(**kwargs)


# ------ CONSTRUCTORS -------


class shap_fixed(ExternalOpImplementation):
    _transform_id = "shap.SHAP_FIXED"
    _signature = SarusSignature()

    def call(self, signature: SarusSignatureValue) -> Any:
        return shap.maskers.Fixed()


# ------ FIXED METHODS ------


class shap_mask_shapes(ExternalOpImplementation):
    _transform_id = "shap.SHAP_FIXED_MASK_SHAPES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame, Dict[str, np.ndarray]],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, X = signature.collect_args()
        return this.mask_shapes(X)


# ------ CONSTRUCTORS -------
class shap_composite(ExternalOpImplementation):
    _transform_id = "shap.SHAP_COMPOSITE"
    _signature = SarusSignature(
        SarusParameterArray(
            name="maskers",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        maskers = signature.collect_args()
        return shap.maskers.Composite(*maskers)


# ------ Composite METHODS ------


class shap_data_transform(ExternalOpImplementation):
    _transform_id = "shap.SHAP_DATA_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Composite,
            condition=DATASPEC | STATIC,
        ),
        SarusParameterArray(
            name="args",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, args = signature.collect_args()
        return this.data_transform(*args)


# ------ CONSTRUCTORS -------
class shap_fixed_composite(ExternalOpImplementation):
    _transform_id = "shap.SHAP_FIXED_COMPOSITE"
    _signature = SarusSignature(
        SarusParameter(
            name="masker",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.FixedComposite(**kwargs)


# ------ CONSTRUCTORS -------


class shap_output_composite(ExternalOpImplementation):
    _transform_id = "shap.SHAP_OUTPUT_COMPOSITE"
    _signature = SarusSignature(
        SarusParameter(
            name="masker",
            annotation=Masker,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="model",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.OutputComposite(**kwargs)


# ------- CONSTRUCTORS -------
class shap_text_masker(ExternalOpImplementation):
    _transform_id = "shap.SHAP_TEXT"
    _signature = SarusSignature(
        SarusParameter(
            name="tokenizer",
            annotation=Optional[Union[Callable, None]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="mask_token",
            annotation=Optional[Union[str, int, None]],
            default=None,
        ),
        SarusParameter(
            name="collapse_mask_token",
            annotation=Optional[Union[bool, str]],
            default="auto",
        ),
        SarusParameter(
            name="output_type",
            annotation=Optional[str],
            default="string",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.Text(**kwargs)


# ------ METHODS ------
class shap_clustering(ExternalOpImplementation):
    _transform_id = "shap.SHAP_CLUSTERING"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.clustering(**kwargs)


class shap_data_text_transform(ExternalOpImplementation):
    _transform_id = "shap.SHAP_DATA_TEXT_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.data_transform(**kwargs)


class shap_feature_names(ExternalOpImplementation):
    _transform_id = "shap.SHAP_FEATURE_NAMES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.feature_names(**kwargs)


class shap_text_invariants(ExternalOpImplementation):
    _transform_id = "shap.SHAP_TEXT_INVARIANTS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.invariants(**kwargs)


class shap_mask_text_shapes(ExternalOpImplementation):
    _transform_id = "shap.SHAP_MASK_TEXT_SHAPES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.mask_shapes(**kwargs)


class shap_shape(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SHAPE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shape(**kwargs)


class shap_token_segments(ExternalOpImplementation):
    _transform_id = "shap.SHAP_TOKEN_SEGMENTS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Text,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="s",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.token_segments(**kwargs)


# ------ CONSTRUCTORS -------
class shap_image(ExternalOpImplementation):
    _transform_id = "shap.SHAP_IMAGE"
    _signature = SarusSignature(
        SarusParameter(
            name="mask_value",
            annotation=Union[np.array, str],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shape",
            annotation=Optional[tuple],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.maskers.Image(**kwargs)


# ------ ImageMasker METHODS ------


class shap_build_partition_tree(ExternalOpImplementation):
    _transform_id = "shap.SHAP_BUILD_PARTITION_TREE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Image,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.build_partition_tree(**kwargs)


class shap_inpaint(ExternalOpImplementation):
    _transform_id = "shap.SHAP_INPAINT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Image,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="x",
            annotation=Union[pd.Series, pd.DataFrame, np.array],
        ),
        SarusParameter(
            name="mask",
            annotation=Union[pd.Series, pd.DataFrame, np.array],
        ),
        SarusParameter(
            name="method",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.inpaint(**kwargs)
