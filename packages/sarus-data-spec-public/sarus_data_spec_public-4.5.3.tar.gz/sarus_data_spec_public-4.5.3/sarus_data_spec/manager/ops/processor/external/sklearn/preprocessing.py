from typing import Any, Callable, Dict, List, Literal, Optional, Union

import numpy.typing as npt

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from sklearn import preprocessing
except ModuleNotFoundError:
    spmatrix = Any


class sk_function_transformer(ExternalOpImplementation):
    _transform_id = "sklearn.SK_FUNCTION_TRANSFORMER"
    _signature = SarusSignature(
        SarusParameter(
            name="func",
            annotation=Optional[Callable],
            default=None,
        ),
        SarusParameter(
            name="inverse_func",
            annotation=Optional[Callable],
            default=None,
        ),
        SarusParameter(
            name="validate",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="accept_sparse",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="check_inverse",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="feature_names_out",
            annotation=Optional[Union[Callable, Literal["one-to-one"]]],
            default=None,
        ),
        SarusParameter(
            name="kw_args",
            annotation=Optional[Dict],
            default=None,
        ),
        SarusParameter(
            name="inv_kw_args",
            annotation=Optional[Dict],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return preprocessing.FunctionTransformer(**kwargs)


class sk_onehot(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ONEHOT"
    _signature = SarusSignature(
        SarusParameter(
            name="categories",
            annotation=Union[Literal["auto"], List[npt.ArrayLike]],
            default="auto",
        ),
        SarusParameter(
            name="drop",
            annotation=Optional[
                Union[Literal["first", "if_binary"], npt.ArrayLike]
            ],
            default=None,
        ),
        SarusParameter(
            name="sparse",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="sparse_output",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="dtype",
            annotation=npt.DTypeLike,
            default=float,
        ),
        SarusParameter(
            name="handle_unknown",
            annotation=Literal["error", "ignore", "infrequent_if_exist"],
            default="error",
        ),
        SarusParameter(
            name="min_frequency",
            annotation=Optional[Union[int, float]],
            default=None,
        ),
        SarusParameter(
            name="max_categories",
            annotation=Optional[int],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return preprocessing.OneHotEncoder(**kwargs)


class sk_label_encoder(ExternalOpImplementation):
    _transform_id = "sklearn.SK_LABEL_ENCODER"
    _signature = SarusSignature()

    def call(self, signature: SarusSignatureValue) -> Any:
        return preprocessing.LabelEncoder()


class sk_scale(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SCALE"
    _signature = SarusSignature(
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
        SarusParameter(
            name="axis",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="with_mean",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="with_std",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return preprocessing.scale(**kwargs)
