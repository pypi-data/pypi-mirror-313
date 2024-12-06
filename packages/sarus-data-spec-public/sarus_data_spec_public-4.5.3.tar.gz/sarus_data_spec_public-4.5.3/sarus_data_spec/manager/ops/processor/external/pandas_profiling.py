from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from .external_op import ExternalOpImplementation

try:
    from ydata_profiling import ProfileReport
except ModuleNotFoundError:
    pass  # error message in typing.py


VisionsTypeset = Any
BaseSummarizer = Any
Settings = Any


class pd_profile_report(ExternalOpImplementation):
    _transform_id = "pandas_profiling.PD_PROFILE_REPORT"
    _signature = SarusSignature(
        SarusParameter(
            name="df",
            annotation=Optional[pd.DataFrame],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="minimal",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="tsmode",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="sortby",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="sensitive",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="explorative",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="dark_mode",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="orange_mode",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="sample",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="config_file",
            annotation=Optional[Union[Path, str]],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="lazy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="typeset",
            annotation=Optional[VisionsTypeset],
            default=None,
        ),
        SarusParameter(
            name="summarizer",
            annotation=Optional[BaseSummarizer],
            default=None,
        ),
        SarusParameter(
            name="config",
            annotation=Optional[Settings],
            default=None,
        ),
        SarusParameter(
            name="type_schema",
            annotation=Optional[dict],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return ProfileReport(**kwargs)
