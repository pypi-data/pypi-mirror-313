from typing import Any, List, Literal, Optional, Union

import numpy.typing as npt

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from sklearn import metrics
except ModuleNotFoundError:
    spmatrix = Any


# metrics
class sk_accuracy_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ACCURACY_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_pred",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="normalize",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.accuracy_score(**kwargs)


class sk_average_precision_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_AVERAGE_PRECISION_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_score",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="average",
            annotation=Optional[
                Literal["micro", "samples", "weighted", "macro"]
            ],
            default="macro",
        ),
        SarusParameter(
            name="pos_label",
            annotation=Union[int, str],
            default=1,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.average_precision_score(**kwargs)


class sk_classification_report(ExternalOpImplementation):
    _transform_id = "sklearn.SK_CLASSIFICATION_REPORT"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_pred",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="target_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="digits",
            annotation=int,
            default=2,
        ),
        SarusParameter(
            name="output_dict",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="zero_division",
            annotation=Literal["warn", 0, 1],
            default="warn",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.classification_report(**kwargs)


class sk_confusion_matrix(ExternalOpImplementation):
    _transform_id = "sklearn.SK_CONFUSION_MATRIX"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_pred",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="normalize",
            annotation=Optional[Literal["true", "pred", "all"]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.confusion_matrix(**kwargs)


class sk_f1_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_F1_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_pred",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="pos_label",
            annotation=Union[int, str],
            default=1,
        ),
        SarusParameter(
            name="average",
            annotation=Optional[
                Literal["micro", "macro", "samples", "weighted", "binary"]
            ],
            default="binary",
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="zero_division",
            annotation=Literal["warn", 0, 1],
            default="warn",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.f1_score(**kwargs)


class sk_precision_recall_curve(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PRECISION_RECALL_CURVE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="probas_pred",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="pos_label",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.precision_recall_curve(**kwargs)


class sk_precision_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PRECISION_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_pred",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="pos_label",
            annotation=Union[int, str],
            default=1,
        ),
        SarusParameter(
            name="average",
            annotation=Optional[
                Literal["micro", "macro", "samples", "weighted", "binary"]
            ],
            default="binary",
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="zero_division",
            annotation=Literal["warn", 0, 1],
            default="warn",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.precision_score(**kwargs)


class sk_recall_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_RECALL_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_pred",
            annotation=Union[npt.ArrayLike, spmatrix],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="pos_label",
            annotation=Union[str, int],
            default=1,
        ),
        SarusParameter(
            name="average",
            annotation=Optional[
                Literal["micro", "macro", "samples", "weighted", "binary"]
            ],
            default="binary",
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="zero_division",
            annotation=Literal["warn", 0, 1],
            default="warn",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.recall_score(**kwargs)


class sk_roc_auc_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ROC_AUC_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_score",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="average",
            annotation=Optional[
                Literal["micro", "macro", "samples", "weighted"]
            ],
            default="macro",
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="max_fpr",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="multi_class",
            annotation=Literal["raise", "ovo", "ovr"],
            default="raise",
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.roc_auc_score(**kwargs)


class sk_auc(ExternalOpImplementation):
    _transform_id = "sklearn.SK_AUC"
    _signature = SarusSignature(
        SarusParameter(
            name="x",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.auc(**kwargs)


class sk_roc_curve(ExternalOpImplementation):
    _transform_id = "sklearn.SK_ROC_CURVE"
    _signature = SarusSignature(
        SarusParameter(
            name="y_true",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="y_score",
            annotation=npt.ArrayLike,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="pos_label",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="drop_intermediate",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return metrics.roc_curve(**kwargs)
