from typing import Any, List, Literal, Optional, Tuple, Union

from numpy.typing import ArrayLike

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from sklearn import compose
    from sklearn.base import BaseEstimator
except ModuleNotFoundError:
    BaseEstimator = Any
    spmatrix = Any


class sk_column_transformer(ExternalOpImplementation):
    _transform_id = "sklearn.SK_COLUMN_TRANSFORMER"
    _signature = SarusSignature(
        SarusParameter(
            name="transformers",
            annotation=List[
                Tuple[
                    str,
                    Union[Literal["drop", "passthrough"], BaseEstimator],
                    Union[str, int, ArrayLike],
                ]
            ],
        ),
        SarusParameter(
            name="remainder",
            annotation=Union[Literal["drop", "passthrough"], BaseEstimator],
            default="drop",
        ),
        SarusParameter(
            name="sparse_threshold",
            annotation=float,
            default=0.3,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="transformer_weights",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="verbose_feature_names_out",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return compose.ColumnTransformer(**kwargs)
