from typing import Any, List, Optional, Tuple, Union

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import pipeline
    from sklearn.base import BaseEstimator
except ModuleNotFoundError:
    BaseEstimator = Any


class sk_pipeline(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PIPELINE"
    _signature = SarusSignature(
        SarusParameter(
            name="steps",
            annotation=List[Tuple[str, BaseEstimator]],
        ),
        SarusParameter(
            name="memory",
            annotation=Optional[Union[str, Any]],
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
        return pipeline.Pipeline(**kwargs)
