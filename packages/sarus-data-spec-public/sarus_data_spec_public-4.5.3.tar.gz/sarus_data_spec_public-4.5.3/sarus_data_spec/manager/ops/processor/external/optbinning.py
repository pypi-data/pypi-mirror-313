from typing import Any, Dict, Iterable, Optional, Sequence, Union

import numpy as np
import pandas as pd

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from .external_op import ExternalOpImplementation

try:
    from optbinning import BinningProcess, OptimalBinning, Scorecard
    from optbinning.binning.binning_statistics import BinningTable
except ModuleNotFoundError:
    OptimalBinning = Any
    Scorecard = Any
    BinningTable = Any
    BinningProcess = Any


class optimal_binning(ExternalOpImplementation):
    _transform_id = "optbinning.OPTIMAL_BINNING"
    _signature = SarusSignature(
        SarusParameter(name="name", annotation=Optional[str], default=""),
        SarusParameter(
            name="dtype", annotation=Optional[str], default="numerical"
        ),
        SarusParameter(
            name="prebinning_method", annotation=Optional[str], default="cart"
        ),
        SarusParameter(name="solver", annotation=Optional[str], default="cp"),
        SarusParameter(
            name="divergence", annotation=Optional[str], default="iv"
        ),
        SarusParameter(
            name="max_n_prebins", annotation=Optional[int], default=20
        ),
        SarusParameter(
            name="min_prebin_size", annotation=Optional[float], default=0.05
        ),
        SarusParameter(
            name="min_n_bins",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="max_n_bins",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="min_bin_size",
            annotation=Optional[Union[float, None]],
            default=None,
        ),
        SarusParameter(
            name="max_bin_size",
            annotation=Optional[Union[float, None]],
            default=None,
        ),
        SarusParameter(
            name="min_bin_n_nonevent",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="max_bin_n_nonevent",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="min_bin_n_event",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="max_bin_n_event",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="monotonic_trend", annotation=Optional[str], default="auto"
        ),
        SarusParameter(
            name="min_event_rate_diff", annotation=Optional[float], default=0
        ),
        SarusParameter(
            name="max_pvalue",
            annotation=Optional[Union[float, None]],
            default=None,
        ),
        SarusParameter(
            name="max_pvalue_policy",
            annotation=Optional[str],
            default="consecutive",
        ),
        SarusParameter(name="gamma", annotation=Optional[float], default=0),
        SarusParameter(
            name="outlier_detector",
            annotation=Optional[Union[str, None]],
            default=None,
        ),
        SarusParameter(
            name="outlier_params",
            annotation=Optional[Union[Dict, None]],
            default=None,
        ),
        SarusParameter(
            name="class_weight",
            annotation=Optional[Union[Dict, str, None]],
            default=None,
        ),
        SarusParameter(
            name="cat_cutoff",
            annotation=Optional[Union[float, None]],
            default=None,
        ),
        SarusParameter(
            name="cat_unknown",
            annotation=Optional[Union[float, str, None]],
            default=None,
        ),
        SarusParameter(
            name="user_splits",
            annotation=Optional[Union[Iterable, None]],
            default=None,
        ),
        SarusParameter(
            name="user_splits_fixed",
            annotation=Optional[Union[Iterable, None]],
            default=None,
        ),
        SarusParameter(
            name="special_codes",
            annotation=Optional[Union[Iterable, Dict, None]],
            default=None,
        ),
        SarusParameter(
            name="split_digits",
            annotation=Optional[Union[int, None]],
            default=None,
        ),
        SarusParameter(
            name="mip_solver", annotation=Optional[str], default="bop"
        ),
        SarusParameter(
            name="time_limit", annotation=Optional[int], default=100
        ),
        SarusParameter(
            name="verbose", annotation=Optional[bool], default=False
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return OptimalBinning(**kwargs)


class optimal_binning_fit(ExternalOpImplementation):
    _transform_id = "optbinning.OPTIMAL_BINNING_FIT"
    _signature = SarusSignature(
        SarusParameter(
            name="opt_binning",
            annotation=OptimalBinning,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="x", annotation=np.ndarray, condition=DATASPEC | STATIC
        ),
        SarusParameter(
            name="y", annotation=np.ndarray, condition=DATASPEC | STATIC
        ),
        SarusParameter(
            name="sample_weight", annotation=Optional[np.ndarray], default=None
        ),
        SarusParameter(name="check_input", annotation=bool, default=False),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.fit(**kwargs)


class optimal_binning_fit_transform(ExternalOpImplementation):
    _transform_id = "optbinning.OPTIMAL_BINNING_FIT_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="opt_binning",
            annotation=OptimalBinning,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="x", annotation=np.ndarray, condition=DATASPEC | STATIC
        ),
        SarusParameter(
            name="y", annotation=np.ndarray, condition=DATASPEC | STATIC
        ),
        SarusParameter(
            name="sample_weight", annotation=Optional[np.ndarray], default=None
        ),
        SarusParameter(name="metric", annotation=str, default="woe"),
        SarusParameter(
            name="metric_special", annotation=Union[float, str], default=0
        ),
        SarusParameter(
            name="metric_missing", annotation=Union[float, str], default=0
        ),
        SarusParameter(
            name="show_digits", annotation=Optional[int], default=2
        ),
        SarusParameter(name="check_input", annotation=bool, default=False),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.fit_transform(**kwargs)


class optimal_binning_transform(ExternalOpImplementation):
    _transform_id = "optbinning.OPTIMAL_BINNING_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="opt_binning",
            annotation=OptimalBinning,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(name="x", annotation=np.ndarray),
        SarusParameter(name="metric", annotation=str, default="woe"),
        SarusParameter(
            name="metric_special", annotation=Union[float, str], default=0
        ),
        SarusParameter(
            name="metric_missing", annotation=Union[float, str], default=0
        ),
        SarusParameter(
            name="show_digits", annotation=Optional[int], default=2
        ),
        SarusParameter(name="check_input", annotation=bool, default=False),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.transform(**kwargs)


class optimal_binning_binning_table(ExternalOpImplementation):
    _transform_id = "optbinning.OPTIMAL_BINNING_BINNING_TABLE"
    _signature = SarusSignature(
        SarusParameter(
            name="opt_binning",
            annotation=OptimalBinning,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        # Extract the OptimalBinning instance
        opt_binning = signature["opt_binning"].value
        bintable = opt_binning.binning_table
        bintable.build()
        # Retrieve the binning table already built
        return bintable


class optbinning_binningProcess(ExternalOpImplementation):
    _transform_id = "optbinning.BINNING_PROCESS"
    _signature = SarusSignature(
        SarusParameter(
            name="variable_names",
            annotation=Sequence[str],
        ),
        SarusParameter(
            name="max_n_prebins",
            annotation=int,
            default=20,
        ),
        SarusParameter(
            name="min_prebin_size",
            annotation=float,
            default=0.05,
        ),
        SarusParameter(
            name="min_n_bins",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="max_n_bins",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="min_bin_size",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="max_bin_size",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="max_pvalue",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="max_pvalue_policy",
            annotation=str,
            default="consecutive",
        ),
        SarusParameter(
            name="selection_criteria",
            annotation=Optional[Dict],
            default=None,
        ),
        SarusParameter(
            name="fixed_variables",
            annotation=Optional[Union[Sequence[str], None]],
            default=None,
        ),
        SarusParameter(
            name="categorical_variables",
            annotation=Optional[Union[Sequence[str], None]],
            default=None,
        ),
        SarusParameter(
            name="special_codes",
            annotation=Optional[Union[Sequence, None]],
            default=None,
        ),
        SarusParameter(
            name="split_digits",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="binning_fit_params",
            annotation=Optional[Dict],
            default=None,
        ),
        SarusParameter(
            name="binning_transform_params",
            annotation=Optional[Dict],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return BinningProcess(**kwargs)


class fit(ExternalOpImplementation):
    _transform_id = "optbinning.BINNING_PROCESS_FIT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BinningProcess,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
        ),
        SarusParameter(
            name="y",
            annotation=np.ndarray,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[np.ndarray],
            default=None,
        ),
        SarusParameter(
            name="check_input",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.fit(**kwargs)


class fit_transform(ExternalOpImplementation):
    _transform_id = "optbinning.BINNING_PROCESS_FIT_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BinningProcess,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
        ),
        SarusParameter(
            name="y",
            annotation=np.ndarray,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[np.ndarray],
            default=None,
        ),
        SarusParameter(
            name="metric",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="metric_special",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="metric_missing",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="show_digits",
            annotation=int,
            default=2,
        ),
        SarusParameter(
            name="check_input",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.fit_transform(**kwargs)


class transform(ExternalOpImplementation):
    _transform_id = "optbinning.BINNING_PROCESS_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BinningProcess,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=Union[np.ndarray, pd.DataFrame],
        ),
        SarusParameter(
            name="metric",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="metric_special",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="metric_missing",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="show_digits",
            annotation=int,
            default=2,
        ),
        SarusParameter(
            name="check_input",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.transform(**kwargs)


class optbinning_binning_table(ExternalOpImplementation):
    _transform_id = "optbinning.BINNING_TABLE"
    _signature = SarusSignature(
        SarusParameter(
            name="name",
            annotation=Optional[str],
            default="",
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[str],
            default="numerical",
        ),
        SarusParameter(
            name="special_codes",
            annotation=Optional[Union[np.ndarray, dict, None]],
            default=None,
        ),
        SarusParameter(
            name="splits",
            annotation=np.ndarray,
        ),
        SarusParameter(
            name="n_nonevent",
            annotation=np.ndarray,
            condition=STATIC,
        ),
        SarusParameter(
            name="n_event",
            annotation=np.ndarray,
        ),
        SarusParameter(
            name="min_x",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="max_x",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="categories",
            annotation=Optional[Union[list, np.ndarray]],
            default=None,
        ),
        SarusParameter(
            name="cat_others",
            annotation=Optional[Union[list, np.ndarray]],
            default=None,
        ),
        SarusParameter(
            name="user_splits",
            annotation=Optional[np.ndarray],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        # Extract arguments using signature.collect_kwargs()
        kwargs = signature.collect_kwargs()
        return BinningTable(**kwargs)


class optbinning_table_build(ExternalOpImplementation):
    _transform_id = "optbinning.BINNING_TABLE_BUILD"
    _signature = SarusSignature(
        SarusParameter(
            name="binning_table",
            annotation=BinningTable,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="show_digits",
            annotation=Optional[int],
            default=2,
        ),
        SarusParameter(
            name="add_totals",
            annotation=Optional[bool],
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        df = this.build(**kwargs)
        # small edit of the result to convert it in arrow
        if kwargs["add_totals"]:
            df["WoE"]["Totals"] = 0.0
            df["WoE"] = df["WoE"].astype(float)
            df_reset = df.reset_index()
            df_reset["index"] = df_reset["index"].astype(
                str
            )  # Replace str with the desired type
            df_reset = df_reset.set_index("index")
        return df_reset


class scorecard(ExternalOpImplementation):
    _transform_id = "optbinning.SCORECARD"
    _signature = SarusSignature(
        SarusParameter(
            name="binning_process",
            annotation=object,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="estimator",
            annotation=object,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="scaling_method",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="scaling_method_params",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="intercept_based",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="reverse_scorecard",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="rounding",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return Scorecard(**kwargs)


class scorecard_predict(ExternalOpImplementation):
    _transform_id = "optbinning.SCORECARD_PREDICT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=scorecard,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="X",
            annotation=pd.DataFrame,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        return this.predict(**kwargs)


class scorecard_predict_proba(ExternalOpImplementation):
    _transform_id = "optbinning.SCORECARD_PREDICT_PROBA"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=scorecard,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="X",
            annotation=pd.DataFrame,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        return this.predict_proba(**kwargs)


class scorecard_fit(ExternalOpImplementation):
    _transform_id = "optbinning.SCORECARD_FIT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=scorecard,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="X",
            annotation=pd.DataFrame,
        ),
        SarusParameter(
            name="y",
            annotation=np.ndarray,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[np.ndarray],
            default=None,
        ),
        SarusParameter(
            name="metric_special",
            annotation=Union[float, str],
            default=0,
        ),
        SarusParameter(
            name="metric_missing",
            annotation=Union[float, str],
            default=0,
        ),
        SarusParameter(
            name="show_digits",
            annotation=int,
            default=2,
        ),
        SarusParameter(
            name="check_input",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        return this.fit(**kwargs)
