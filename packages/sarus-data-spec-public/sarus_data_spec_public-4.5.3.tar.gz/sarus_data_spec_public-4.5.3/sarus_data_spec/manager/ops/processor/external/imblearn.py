from __future__ import annotations

from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

import numpy as np

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from .external_op import ExternalOpImplementation

try:
    from imblearn import over_sampling, pipeline, under_sampling
except ModuleNotFoundError:
    pass  # error message in typing.py

SamplingStrategy = Literal[
    "majority", "not minority", "not majority", "all", "auto"
]


# ------ CONSTRUCTORS ------
class imb_pipeline(ExternalOpImplementation):
    _transform_id = "imblearn.IMB_PIPELINE"
    _signature = SarusSignature(
        SarusParameter(
            name="steps",
            annotation=List[Tuple[str, Any]],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="memory",
            annotation=Optional,
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


class imb_random_under_sampler(ExternalOpImplementation):
    _transform_id = "imblearn.IMB_RANDOM_UNDER_SAMPLER"
    _signature = SarusSignature(
        SarusParameter(
            name="sampling_strategy",
            annotation=Union[float, SamplingStrategy, Callable, Dict],
            default="auto",
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="replacement",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return under_sampling.RandomUnderSampler(**kwargs)


class imb_smotenc(ExternalOpImplementation):
    _transform_id = "imblearn.IMB_SMOTENC"
    _signature = SarusSignature(
        SarusParameter(
            name="categorical_features",
            annotation=Union[List[int], List[bool]],
        ),
        SarusParameter(
            name="sampling_strategy",
            annotation=Union[float, SamplingStrategy, Callable, Dict],
            default="auto",
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="k_neighbors",
            annotation=Union[int, object],
            default=5,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return over_sampling.SMOTENC(**kwargs)
