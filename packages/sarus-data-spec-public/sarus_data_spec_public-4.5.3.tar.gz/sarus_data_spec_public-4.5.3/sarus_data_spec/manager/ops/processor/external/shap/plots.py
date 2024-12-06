from typing import Any, List, Optional, Tuple, Union
import warnings

from numpy import ndarray
from pandas import DataFrame
import numpy as np
import pandas as pd

from sarus_data_spec.dataspec_validator.parameter_kind import DATASPEC, STATIC
from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from shap import Explanation, summary_plot
    from shap.utils import OpChain
    import shap

    explanation_abs = Explanation.abs
except ModuleNotFoundError:
    OpChain = Any
    explanation_abs = Any
    Explanation = Any
    warnings.warn("Shap not available")


class shap_plots_bar(ExternalOpImplementation):
    _transform_id = "shap.SHAP_PLOTS_BAR"
    _signature = SarusSignature(
        SarusParameter(
            name="shap_values",
            annotation=Any,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="max_display",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="order",
            annotation=explanation_abs,
            default=None,
            condition=STATIC,
        ),
        SarusParameter(
            name="clustering",
            annotation=Optional[Any],
            default=None,
        ),
        SarusParameter(
            name="clustering_cutoff",
            annotation=float,
            default=0.5,
        ),
        SarusParameter(
            name="merge_cohorts",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="show_data",
            annotation=str,
            default="auto",
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["order"] is None:
            kwargs["order"] = shap.Explanation.abs
        return shap.plots.bar(**kwargs)


class shap_waterfall(ExternalOpImplementation):
    _transform_id = "shap.SHAP_WATERFALL"
    _signature = SarusSignature(
        SarusParameter(
            name="shap_values",
            annotation=Explanation,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="max_display",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.plots.waterfall(**kwargs)


class shap_beeswarm(ExternalOpImplementation):
    _transform_id = "shap.SHAP_BEESWARM"
    _signature = SarusSignature(
        SarusParameter(
            name="shap_values",
            annotation=Explanation,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="max_display",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="color_bar",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="plot_size",
            annotation=Union[str, float, Tuple[float, float]],
            default="auto",
        ),
        SarusParameter(
            name="order",
            annotation=Optional[OpChain],
            default=None,
        ),
        SarusParameter(
            name="clustering",
            annotation=Optional[OpChain],
            default=None,
        ),
        SarusParameter(
            name="cluster_threshold",
            annotation=Optional[float],
            default=0.5,
        ),
        SarusParameter(
            name="color",
            annotation=Optional[OpChain],
            default=None,
        ),
        SarusParameter(
            name="axis_color",
            annotation=Optional[str],
            default="#333333",
        ),
        SarusParameter(
            name="alpha",
            annotation=Optional[float],
            default=1,
        ),
        SarusParameter(
            name="show",
            annotation=Optional[bool],
            default=True,
        ),
        SarusParameter(
            name="log_scale",
            annotation=Optional[bool],
            default=False,
        ),
        SarusParameter(
            name="color_bar_label",
            annotation=Optional[str],
            default="Feature value",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["order"] is None:
            kwargs["order"] = shap.Explanation.abs.mean(0)
        return shap.plots.beeswarm(**kwargs)


class shap_heatmap(ExternalOpImplementation):
    _transform_id = "shap.SHAP_HEATMAP"
    _signature = SarusSignature(
        SarusParameter(
            name="shap_values",
            annotation=Explanation,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="instance_order",
            annotation=Union[OpChain, np.ndarray],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="feature_values",
            annotation=Union[OpChain, np.ndarray],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="feature_order",
            annotation=Optional[Union[None, OpChain, np.ndarray]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="max_display",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="plot_width",
            annotation=int,
            default=8,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        if kwargs["instance_order"] is None:
            del kwargs["instance_order"]
        if kwargs["feature_values"] is None:
            del kwargs["feature_values"]
        return shap.plots.heatmap(**kwargs)


class shap_summary_plot(ExternalOpImplementation):
    _transform_id = "shap.SHAP_SUMMARY_PLOT"
    _signature = SarusSignature(
        SarusParameter(
            name="shap_values",
            annotation=np.ndarray,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="features",
            annotation=Optional[Union[np.ndarray, pd.DataFrame, List]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="max_display",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="plot_type",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="color",
            annotation=Optional[Any],
            default=None,
        ),
        SarusParameter(
            name="axis_color",
            annotation=str,
            default="#333333",
        ),
        SarusParameter(
            name="title",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="alpha",
            annotation=float,
            default=1,
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="color_bar",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="plot_size",
            annotation=Union[str, float, Tuple[float, float]],
            default="auto",
        ),
        SarusParameter(
            name="layered_violin_max_num_bins",
            annotation=int,
            default=20,
        ),
        SarusParameter(
            name="class_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="class_inds",
            annotation=Optional[List[int]],
            default=None,
        ),
        SarusParameter(
            name="color_bar_label",
            annotation=str,
            default="Feature value",
        ),
        SarusParameter(
            name="cmap",
            annotation=Any,  # Adjust accordingly
            default=None,
        ),
        SarusParameter(
            name="auto_size_plot",
            annotation=Optional[bool],
            default=None,
        ),
        SarusParameter(
            name="use_log_scale",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return summary_plot(**kwargs)


class shap_dependence_plot(ExternalOpImplementation):
    _transform_id = "shap.SHAP_DEPENDENCE_PLOT"
    _signature = SarusSignature(
        SarusParameter(
            name="ind",
            annotation=Union[int, str],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shap_values",
            annotation=ndarray,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="features",
            annotation=Union[ndarray, DataFrame],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="display_features",
            annotation=Optional[Union[ndarray, DataFrame]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="interaction_index",
            annotation=Union[str, int],
            default="auto",
        ),
        SarusParameter(
            name="color",
            annotation=str,
            default="#1E88E5",
        ),
        SarusParameter(
            name="axis_color",
            annotation=str,
            default="#333333",
        ),
        SarusParameter(
            name="cmap",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="dot_size",
            annotation=int,
            default=16,
        ),
        SarusParameter(
            name="x_jitter",
            annotation=float,
            default=0,
        ),
        SarusParameter(
            name="alpha",
            annotation=float,
            default=1,
        ),
        SarusParameter(
            name="title",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="xmin",
            annotation=Optional[Union[float, str]],
            default=None,
        ),
        SarusParameter(
            name="xmax",
            annotation=Optional[Union[float, str]],
            default=None,
        ),
        SarusParameter(
            name="ax",
            annotation=Optional[Any],  # Use proper type for matplotlib axes
            default=None,
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.dependence_plot(**kwargs)


class ShapForcePlot(ExternalOpImplementation):
    _transform_id = "shap.SHAP_FORCE_PLOT"
    _signature = SarusSignature(
        SarusParameter(
            name="base_value",
            annotation=float,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="shap_values",
            annotation=Optional[np.ndarray],
            condition=DATASPEC | STATIC,
            default=None,
        ),
        SarusParameter(
            name="features",
            annotation=Optional[np.ndarray],
            condition=DATASPEC | STATIC,
            default=None,
        ),
        SarusParameter(
            name="feature_names",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="out_names",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="link",
            annotation=str,
            default="identity",
        ),
        SarusParameter(
            name="plot_cmap",
            annotation=str,
            default="RdBu",
        ),
        SarusParameter(
            name="matplotlib",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="show",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="figsize",
            annotation=Tuple[float, float],
            default=(20, 3),
        ),
        SarusParameter(
            name="ordering_keys",
            annotation=Optional[Any],  # Adjust this type based on your needs
            default=None,
        ),
        SarusParameter(
            name="ordering_keys_time_format",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="text_rotation",
            annotation=float,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return shap.force_plot(**kwargs)
