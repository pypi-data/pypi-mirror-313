from datetime import timedelta
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    List,
    Literal,
    Optional,
    Union,
)

from pandas._libs.tslibs import BaseOffset
from pandas.api.indexers import BaseIndexer
import pandas as pd
import pandas._typing as pdt

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

GroupBy = Union[
    pd.core.groupby.DataFrameGroupBy,
    pd.core.groupby.SeriesGroupBy,
]


class pd_agg_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_AGG_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="func",
            annotation=Optional[Union[Callable, Dict, List]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.agg(**kwargs)


class pd_count_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_COUNT_GROUPBY"
    _dp_equivalent_id = "pandas.PD_COUNT_GROUPBY_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.count(**kwargs)


class pd_max_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_MAX_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="min_count",
            annotation=int,
            default=-1,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.max(**kwargs)


class pd_mean_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEAN_GROUPBY"
    _dp_equivalent_id = "pandas.PD_MEAN_GROUPBY_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.mean(**kwargs)


class pd_min_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_MIN_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="min_count",
            annotation=int,
            default=-1,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.min(**kwargs)


class pd_rolling_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_ROLLING_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="window",
            annotation=Union[int, timedelta, BaseOffset, BaseIndexer],
        ),
        SarusParameter(
            name="min_periods",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="center",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="win_type",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="on",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="closed",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="method",
            annotation=Literal["single", "table"],
            default="single",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.rolling(**kwargs)


class pd_shift_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_SHIFT_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="periods",
            annotation=int,
            default=1,
        ),
        SarusParameter(
            name="freq",
            annotation=Optional[pdt.Frequency],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="fill_value",
            annotation=Hashable,
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shift(**kwargs)


class pd_groups_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_GROUPS_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.groups


class pd_sum_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_SUM_GROUPBY"
    _dp_equivalent_id = "pandas.PD_SUM_GROUPBY_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="min_count",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.sum(**kwargs)


class pd_std_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_STD_GROUPBY"
    _dp_equivalent_id = "pandas.PD_STD_GROUPBY_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="ddof",
            annotation=int,
            default=1,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.std(**kwargs)


class pd_median_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEDIAN_GROUPBY"
    _dp_equivalent_id = "pandas.PD_MEDIAN_GROUPBY_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=GroupBy,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.median(**kwargs)
