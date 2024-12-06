from typing import Any, Literal, Optional, Union

import numpy as np
import pandas as pd

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import impute
except ModuleNotFoundError:
    pass  # error message in typing.py


class sk_simple_imputer(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SIMPLE_IMPUTER"
    _signature = SarusSignature(
        SarusParameter(
            name="missing_values",
            annotation=Optional[
                Union[int, float, str, type(np.nan), type(pd.NA)]
            ],
            default=np.nan,
        ),
        SarusParameter(
            name="strategy",
            annotation=Literal["mean", "median", "most_frequent", "constant"],
            default="mean",
        ),
        SarusParameter(
            name="fill_value",
            annotation=Optional[Union[str, np.number]],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="add_indicator",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="keep_empty_features",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return impute.SimpleImputer(**kwargs)
