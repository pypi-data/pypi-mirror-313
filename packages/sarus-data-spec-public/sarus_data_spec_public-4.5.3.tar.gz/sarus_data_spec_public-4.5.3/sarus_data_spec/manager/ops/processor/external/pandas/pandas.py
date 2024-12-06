from datetime import datetime, timedelta
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)
import typing as t

from pandas._libs import lib
from pandas._libs.tslibs import BaseOffset
from pandas.api.indexers import BaseIndexer
import numpy as np
import pandas as pd
import pandas._typing as pdt

from sarus_data_spec.dataspec_validator.parameter_kind import (
    DATASPEC,
    STATIC,
    TRANSFORM,
)
from sarus_data_spec.dataspec_validator.signature import (
    SarusBoundSignature,
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)
from sarus_data_spec.dataspec_validator.typing import PUPKind
import sarus_data_spec.typing as st

from ..external_op import ExternalOpImplementation

# Defined in pandas version > 1.3.5
IgnoreRaise = t.Literal["ignore", "raise"]
ValueKeyFunc = Optional[
    Callable[[pd.Series], Union[pd.Series, pdt.AnyArrayLike]]
]
DropKeep = Literal["first", "last", False]
QuantileInterpolation = Literal[
    "linear", "lower", "higher", "midpoint", "nearest"
]
CorrelationMethod = Union[
    Literal["pearson", "kendall", "spearman"],
    Callable[[np.ndarray, np.ndarray], float],
]
MergeHow = Literal["left", "right", "inner", "outer", "cross"]
ArrayConvertible = Union[List, Tuple, pdt.AnyArrayLike]
DatetimeScalar = Union[pdt.Scalar, datetime]
DatetimeScalarOrArrayConvertible = Union[DatetimeScalar, ArrayConvertible]


# ------ CONSTRUCTORS -------
class pd_dataframe(ExternalOpImplementation):
    _transform_id = "pandas.PD_DATAFRAME"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=Optional[
                Union[
                    Sequence[Sequence[Any]],
                    Mapping[Hashable, Sequence[Any]],
                    pd.DataFrame,
                ]
            ],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="index",
            annotation=Optional[pdt.Axes],
            default=None,
        ),
        SarusParameter(
            name="columns",
            annotation=Optional[pdt.Axes],
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[pdt.Dtype],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=Optional[bool],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return pd.DataFrame(**kwargs)

    def py_output_hint(
        self,
        transform: st.Transform,
        *arguments: Union[st.DataSpec, st.Transform],
        **named_arguments: Union[st.DataSpec, st.Transform],
    ) -> Optional[str]:
        return str(pd.DataFrame)


class pd_series(ExternalOpImplementation):
    _transform_id = "pandas.PD_SERIES"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=Optional[
                Union[pdt.ArrayLike, Iterable, Dict, pdt.Scalar]
            ],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="index",
            annotation=pd.Index,
            default=None,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[pdt.Dtype],
            default=None,
        ),
        SarusParameter(
            name="name",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="fastpath",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return pd.Series(**kwargs)

    def py_output_hint(
        self,
        transform: st.Transform,
        *arguments: Union[st.DataSpec, st.Transform],
        **named_arguments: Union[st.DataSpec, st.Transform],
    ) -> Optional[str]:
        return str(pd.Series)


# ------ DataFrame & Series METHODS ------
class pd_loc(ExternalOpImplementation):
    _transform_id = "pandas.PD_LOC"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="key",
            annotation=Tuple[Union[str, slice, List[str]], ...],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> pd.DataFrame:
        (this, key) = signature.collect_args()
        return this.loc[key]

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """Token preserving if the key is a tuple or a slice that
        selects all the rows (e.g. loc[:, "col"], loc[:]).
        PUP in the other cases.
        """
        key_arg = bound_signature["key"]
        if STATIC.isin(key_arg.parameter_kind()):
            key_value = key_arg.static_value()
            if isinstance(key_value, tuple) and len(key_value) == 2:
                row_key, _ = key_value
                if row_key == slice(None, None, None):
                    return PUPKind.TOKEN_PRESERVING
            elif isinstance(key_value, slice):
                if key_value == slice(None, None, None):
                    return PUPKind.TOKEN_PRESERVING
            elif isinstance(key_value, (int, str)):
                # a scalar selects a single row
                return PUPKind.ROW

        return PUPKind.PUP


class pd_set_loc(ExternalOpImplementation):
    _transform_id = "pandas.PD_SET_LOC"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="key",
            annotation=Tuple[Union[str, slice, List[str]], ...],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="value",
            annotation=t.Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, key, value) = signature.collect_args()
        this.loc[key] = value
        return this


class pd_iloc(ExternalOpImplementation):
    _transform_id = "pandas.PD_ILOC"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="key",
            annotation=Tuple[Union[str, slice, List[str]], ...],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> pd.DataFrame:
        (this, key) = signature.collect_args()
        return this.iloc[key]

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """Token preserving the alignment if the key is a slice that
        selects all the rows (e.g. iloc[:]).
        PUP in the other cases.
        """
        key_arg = bound_signature["key"]
        if STATIC.isin(key_arg.parameter_kind()):
            key_value = key_arg.static_value()
            if isinstance(key_value, slice):
                if key_value == slice(None, None, None):
                    return PUPKind.TOKEN_PRESERVING
            elif isinstance(key_value, (int, str)):
                # a scalar selects a single row
                return PUPKind.ROW

        return PUPKind.PUP


class pd_set_iloc(ExternalOpImplementation):
    _transform_id = "pandas.PD_SET_ILOC"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="key",
            annotation=Tuple[Union[str, slice, List[str]], ...],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="value",
            annotation=t.Any,
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, key, value) = signature.collect_args()
        this.iloc[key] = value
        return this


class pd_head(ExternalOpImplementation):
    _transform_id = "pandas.PD_HEAD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="n",
            annotation=int,
            default=5,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        return this.head(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.PUP


class pd_astype(ExternalOpImplementation):
    _transform_id = "pandas.PD_ASTYPE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="dtype",
            annotation=pdt.Dtype,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="errors",
            annotation=IgnoreRaise,
            default="raise",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> pd.DataFrame:
        (this, kwargs) = signature.collect_kwargs_method()
        return this.astype(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_getitem(ExternalOpImplementation):
    _transform_id = "pandas.PD_GETITEM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="key",
            annotation=t.Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, key) = signature.collect_args()
        return this[key]

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """PUP in any case. Token preserving if the key is a string or a list
        of strings."""
        if isinstance(bound_signature["key"].static_value(), st.DataSpec):
            key_type = bound_signature["key"].python_type()
            return (
                PUPKind.TOKEN_PRESERVING
                if key_type in [str(str)]
                else PUPKind.PUP
            )
        else:
            key_value = bound_signature["key"].static_value()
            if isinstance(key_value, list):
                # can select columns or rows depending on the type of the list
                # values
                all_strings = all([isinstance(x, str) for x in key_value])
                return PUPKind.TOKEN_PRESERVING if all_strings else PUPKind.PUP
            return (
                PUPKind.TOKEN_PRESERVING
                if isinstance(key_value, str)
                else PUPKind.PUP
            )


class pd_sum(ExternalOpImplementation):
    _transform_id = "pandas.PD_SUM"
    _dp_equivalent_id = "pandas.PD_SUM_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=t.Optional[pdt.Axis],
            default=None,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="level",
            annotation=t.Optional[pdt.Level],
            default=None,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=t.Optional[bool],
            default=None,
        ),
        SarusParameter(
            name="min_count",
            annotation=int,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["numeric_only"]
        return this.sum(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`axis=1`"""
        if bound_signature["this"].python_type() == str(pd.Series):
            return PUPKind.NOT_PUP

        axis = bound_signature["axis"].static_value()
        return PUPKind.TOKEN_PRESERVING if axis == 1 else PUPKind.NOT_PUP


class pd_mean(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEAN"
    _dp_equivalent_id = "pandas.PD_MEAN_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="level",
            annotation=t.Optional[pdt.Level],
            default=None,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["numeric_only"]
        return this.mean(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`axis=1`"""
        if bound_signature["this"].python_type() == str(pd.Series):
            return PUPKind.NOT_PUP

        axis = bound_signature["axis"].static_value()
        return PUPKind.TOKEN_PRESERVING if axis == 1 else PUPKind.NOT_PUP


class pd_std(ExternalOpImplementation):
    _transform_id = "pandas.PD_STD"
    _dp_equivalent_id = "pandas.PD_STD_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="level",
            annotation=t.Optional[pdt.Level],
            default=None,
        ),
        SarusParameter(
            name="ddof",
            annotation=int,
            default=1,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["numeric_only"]
        return this.std(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`axis=1`"""
        axis = bound_signature["axis"].static_value()
        return PUPKind.TOKEN_PRESERVING if axis == 1 else PUPKind.NOT_PUP


class pd_median(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEDIAN"
    _dp_equivalent_id = "pandas.PD_MEDIAN_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="level",
            annotation=t.Optional[int],
            default=None,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["numeric_only"]
        return this.median(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`axis=1`"""
        if bound_signature["this"].python_type() == str(pd.Series):
            return PUPKind.NOT_PUP

        axis = bound_signature["axis"].static_value()
        return PUPKind.TOKEN_PRESERVING if axis == 1 else PUPKind.NOT_PUP


class pd_abs(ExternalOpImplementation):
    _transform_id = "pandas.PD_ABS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this = signature["this"].value
        return this.abs()

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_drop(ExternalOpImplementation):
    _transform_id = "pandas.PD_DROP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[
                Union[str, List[Union[str, Tuple[str, ...]]], Type[pdt.Level]]
            ],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Union[int, str],
            default=0,
        ),
        SarusParameter(
            name="index",
            annotation=Optional[Union[pd.Index, List[Union[str, int]]]],
            default=None,
        ),
        SarusParameter(
            name="columns",
            annotation=Optional[Union[pd.Index, List[Union[str, int]]]],
            default=None,
        ),
        SarusParameter(
            name="level",
            annotation=Optional[Union[int, str, Tuple[Union[int, str], ...]]],
            default=None,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="errors",
            annotation=str,
            default="raise",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
        return this.drop(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        axis = bound_signature["axis"].static_value()
        if axis in [0, "columns"]:
            return PUPKind.PUP
        else:
            return PUPKind.TOKEN_PRESERVING


class pd_dropna(ExternalOpImplementation):
    _transform_id = "pandas.PD_DROPNA"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[Union[int, str]],
            default=0,
        ),
        SarusParameter(
            name="how",
            annotation=Optional[str],
            default="any",
        ),
        SarusParameter(
            name="thresh",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="subset",
            annotation=Optional[Union[pd.Index, List[Union[str, int]]]],
            default=None,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        name=_transform_id,
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["subset"]
            del kwargs["thresh"]
        return this.dropna(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        axis = bound_signature["axis"].static_value()
        if axis in [0, "columns"]:
            return PUPKind.PUP
        else:
            return PUPKind.TOKEN_PRESERVING


class pd_fillna(ExternalOpImplementation):
    _transform_id = "pandas.PD_FILLNA"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="value",
            annotation=Optional[
                t.Union[pdt.Scalar, Mapping, Sequence, pd.DataFrame]
            ],
            default=None,
        ),
        SarusParameter(
            name="method",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[pdt.Axis],
            default=None,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="limit",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="downcast",
            annotation=Optional[str],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.fillna(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`method` is `None`"""
        method = bound_signature["method"].static_value()
        if method is None:
            return PUPKind.TOKEN_PRESERVING
        else:
            return PUPKind.NOT_PUP


class pd_isin(ExternalOpImplementation):
    _transform_id = "pandas.PD_ISIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="values",
            annotation=Union[pd.Series, List[Any], Tuple[Any], pd.DataFrame],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.isin(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_isnull(ExternalOpImplementation):
    _transform_id = "pandas.PD_ISNULL"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, _ = signature.collect_kwargs_method()
        return this.isnull()

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_mask(ExternalOpImplementation):
    _transform_id = "pandas.PD_MASK"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="cond",
            annotation=Union[pd.Series, pd.DataFrame, pdt.ArrayLike, Callable],
        ),
        SarusParameter(
            name="other",
            annotation=Optional[
                Union[pd.Series, pd.DataFrame, pdt.Scalar, Callable]
            ],
            default=float("nan"),
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[
                Union[int, Literal["index", "columns", "rows"]]
            ],
            default=None,
        ),
        SarusParameter(
            name="level",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.mask(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`cond` and `other` are not callable"""
        cond = bound_signature["cond"].static_value()
        other = bound_signature["other"].static_value()
        if callable(cond) or callable(other):
            return PUPKind.NOT_PUP
        else:
            return PUPKind.TOKEN_PRESERVING


class pd_notnull(ExternalOpImplementation):
    _transform_id = "pandas.PD_NOTNULL"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, _ = signature.collect_kwargs_method()
        return this.notnull()

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_rename(ExternalOpImplementation):
    _transform_id = "pandas.PD_RENAME"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="mapper",
            annotation=Optional[Union[Dict[str, str], Callable[[str], str]]],
            default=None,
        ),
        SarusParameter(
            name="index",
            annotation=Optional[Union[Dict[str, str], Callable[[str], str]]],
            default=None,
        ),
        SarusParameter(
            name="columns",
            annotation=Optional[Union[Dict[str, str], Callable[[str], str]]],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=Optional[bool],
            default=None,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="level",
            default=None,
            annotation=Hashable,
        ),
        SarusParameter(
            name="errors",
            annotation=Literal["ignore", "raise"],
            default="ignore",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["mapper"]
            del kwargs["columns"]
            del kwargs["axis"]
        return this.rename(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`mapper`, `index` and `columns` are not callable"""
        mapper = bound_signature["mapper"].static_value()
        index = bound_signature["index"].static_value()
        columns = bound_signature["columns"].static_value()
        if callable(mapper) or callable(index) or callable(columns):
            return PUPKind.NOT_PUP
        else:
            return PUPKind.TOKEN_PRESERVING


class pd_replace(ExternalOpImplementation):
    _transform_id = "pandas.PD_REPLACE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="to_replace",
            annotation=Union[pdt.Scalar, Mapping, Sequence],
            default=None,
        ),
        SarusParameter(
            name="value",
            annotation=Union[pdt.Scalar, Mapping, Sequence],
            default=None,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="limit",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="regex",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="method",
            annotation=Literal["pad", "ffill", "bfill"],
            default=lib.no_default,
        ),
        name=_transform_id,
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.replace(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """`value` is not `None`"""
        value = bound_signature["value"].static_value()
        if value is None:
            return PUPKind.NOT_PUP
        else:
            return PUPKind.TOKEN_PRESERVING


class pd_round(ExternalOpImplementation):
    _transform_id = "pandas.PD_ROUND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="decimals",
            annotation=Union[int, dict, pd.Series],
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.round(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_select_dtypes(ExternalOpImplementation):
    _transform_id = "pandas.PD_SELECT_DTYPES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="include",
            annotation=t.Optional[t.Union[pdt.Scalar, t.List]],
            default=None,
        ),
        SarusParameter(
            name="exclude",
            annotation=t.Optional[t.Union[pdt.Scalar, t.List]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, kwargs) = signature.collect_kwargs_method()
        return this.select_dtypes(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.PUP


class pd_add(ExternalOpImplementation):
    _transform_id = "pandas.PD_ADD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.Series, pd.DataFrame, pd.Index, float, int],
        ),
        SarusParameter(
            name="fill_value",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[
                Union[int, Literal["index", "columns", "rows"]]
            ],
            default="columns",
        ),
        SarusParameter(
            name="level",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
        return this.add(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


# for test only to remove
class pd_add_test(ExternalOpImplementation):
    _transform_id = "pandas.PD_ADD_TEST"
    _pup_equivalent_id = "pandas.PD_ADD_TEST_PUP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.Series, pd.DataFrame, pd.Index, float, int],
        ),
        SarusParameter(
            name="fill_value",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[
                Union[int, Literal["index", "columns", "rows"]]
            ],
            default="columns",
        ),
        SarusParameter(
            name="level",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
        return this.add(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.NOT_PUP


# for test only to remove
class pd_add_test_pup(ExternalOpImplementation):
    _transform_id = "pandas.PD_ADD_TEST_PUP"
    _non_pup_equivalent_id = "pandas.PD_ADD_TEST"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.Series, pd.DataFrame, pd.Index, float, int],
        ),
        SarusParameter(
            name="fill_value",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[
                Union[int, Literal["index", "columns", "rows"]]
            ],
            default="columns",
        ),
        SarusParameter(
            name="level",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
        return this.add(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_sub(ExternalOpImplementation):
    _transform_id = "pandas.PD_SUB"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.Series, pd.DataFrame, pd.Index, float, int],
        ),
        SarusParameter(
            name="fill_value",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[
                Union[int, Literal["index", "columns", "rows"]]
            ],
            default="columns",
        ),
        SarusParameter(
            name="level",
            annotation=Optional[Union[int, str]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
        return this.sub(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_reset_index(ExternalOpImplementation):
    _transform_id = "pandas.PD_RESET_INDEX"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="level",
            annotation=pdt.IndexLabel,
            default=None,
        ),
        SarusParameter(
            name="drop",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="col_level",
            annotation=Hashable,
            default=0,
        ),
        SarusParameter(
            name="col_fill",
            annotation=Hashable,
            default="",
        ),
        # > 1.3.5
        # SarusParameter(
        #     name="allow_duplicates",
        #     annotation=Union[bool, lib.NoDefault],
        #     default=lib.no_default,
        # ),
        # SarusParameter(
        #     name="names",
        #     annotation=Optional[Union[Hashable, Sequence[Hashable]]],
        #     default=None,
        # ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["col_level"]
            del kwargs["col_fill"]
        return this.reset_index(**kwargs)


class pd_min(ExternalOpImplementation):
    _transform_id = "pandas.PD_MIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[int],
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.min(**kwargs)


class pd_max(ExternalOpImplementation):
    _transform_id = "pandas.PD_MAX"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[int],
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.max(**kwargs)


class pd_shift(ExternalOpImplementation):
    _transform_id = "pandas.PD_SHIFT"
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
            default=lib.no_default,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.shift(**kwargs)


class pd_any(ExternalOpImplementation):
    _transform_id = "pandas.PD_ANY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="bool_only",
            annotation=Optional[bool],
            default=None,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.any(**kwargs)


class pd_describe(ExternalOpImplementation):
    _transform_id = "pandas.PD_DESCRIBE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="percentiles",
            annotation=Optional[Sequence[float]],
            default=None,
        ),
        SarusParameter(
            name="include",
            annotation=Optional[Union[Literal["all"], List[pdt.Dtype]]],
            default=None,
        ),
        SarusParameter(
            name="exclude",
            annotation=Optional[List[pdt.Dtype]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.describe(**kwargs)


class pd_quantile(ExternalOpImplementation):
    _transform_id = "pandas.PD_QUANTILE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="q",
            annotation=Union[float, pdt.AnyArrayLike, Sequence[float]],
            default=0.5,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="interpolation",
            annotation=QuantileInterpolation,
            default="linear",
        ),
        # > 1.3.5
        # SarusParameter(
        #     name="method",
        #     annotation=Literal["single", "table"],
        #     default="single",
        # ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
            del kwargs["numeric_only"]
        return this.quantile(**kwargs)


class pd_reindex(ExternalOpImplementation):
    _transform_id = "pandas.PD_REINDEX"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="labels",
            annotation=Optional[pdt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="index",
            annotation=Optional[pdt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="columns",
            annotation=Optional[pdt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[pdt.Axis],
            default=None,
        ),
        SarusParameter(
            name="method",
            annotation=Optional[
                Literal["backfill", "bfill", "pad", "ffill", "nearest"]
            ],
            default=None,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="level",
            annotation=Optional[pdt.Level],
            default=None,
        ),
        SarusParameter(
            name="fill_value",
            annotation=Optional[pdt.Scalar],
            default=np.nan,
        ),
        SarusParameter(
            name="limit",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="tolerance",
            annotation=Optional[Union[pdt.Scalar, List[pdt.Scalar]]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        # The pandas method is a bit weird and allows only one of
        # these to be specified at a time
        for name in ["labels", "index", "columns", "axis"]:
            if kwargs[name] is None:
                del kwargs[name]
        return this.reindex(**kwargs)


class pd_count(ExternalOpImplementation):
    _transform_id = "pandas.PD_COUNT"
    _dp_equivalent_id = "pandas.PD_COUNT_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
            del kwargs["numeric_only"]
        return this.count(**kwargs)


class pd_transpose(ExternalOpImplementation):
    _transform_id = "pandas.PD_TRANSPOSE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.transpose(**kwargs)


class pd_value_counts(ExternalOpImplementation):
    _transform_id = "pandas.PD_VALUE_COUNTS"
    _dp_equivalent_id = "pandas.PD_VALUE_COUNTS_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="subset",
            annotation=Optional[Sequence[Hashable]],
            default=None,
        ),
        SarusParameter(
            name="normalize",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="ascending",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="dropna",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["subset"]
        return this.value_counts(**kwargs)


class pd_to_dict(ExternalOpImplementation):
    _transform_id = "pandas.PD_TO_DICT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="orient",
            annotation=Literal[
                "dict", "list", "series", "split", "tight", "records", "index"
            ],
            default="dict",
        ),
        SarusParameter(
            name="into",
            annotation=Type[dict],
            default=dict,
        ),
        # > 1.3.5
        # SarusParameter(
        #     name="index",
        #     annotation=bool,
        #     default=True,
        # ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.to_dict(**kwargs)


class pd_apply(ExternalOpImplementation):
    _transform_id = "pandas.PD_APPLY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="func",
            annotation=pdt.AggFuncTypeBase,
            condition=STATIC | TRANSFORM,
            predicate=lambda x: isinstance(x, str),
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="raw",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="result_type",
            annotation=Optional[Literal["expand", "reduce", "broadcast"]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
            del kwargs["result_type"]
            del kwargs["raw"]
        return this.apply(**kwargs)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        axis_arg = bound_signature["axis"]
        if STATIC.isin(axis_arg.parameter_kind()):
            axis_value = axis_arg.static_value()
            if axis_value == 1:
                return PUPKind.TOKEN_PRESERVING
        return super().pup_kind(bound_signature)


class pd_applymap(ExternalOpImplementation):
    _transform_id = "pandas.PD_APPLYMAP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="func",
            annotation=pdt.AggFuncTypeBase,
            condition=STATIC | TRANSFORM,
            predicate=lambda x: isinstance(x, str),
        ),
        SarusParameter(
            name="na_action",
            annotation=Optional[Literal["ignore"]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.applymap(**kwargs)

    def pup_kind(self, signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_map(ExternalOpImplementation):
    _transform_id = "pandas.PD_MAP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Series,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="arg",
            annotation=pdt.AggFuncTypeBase,
            condition=STATIC | TRANSFORM,
            predicate=lambda x: isinstance(x, (dict, str)),
        ),
        SarusParameter(
            name="na_action",
            annotation=Optional[Literal["ignore"]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.map(**kwargs)

    def pup_kind(self, signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_skew(ExternalOpImplementation):
    _transform_id = "pandas.PD_SKEW"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[pdt.Axis],
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.skew(**kwargs)


class pd_kurtosis(ExternalOpImplementation):
    _transform_id = "pandas.PD_KURTOSIS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=Optional[pdt.Axis],
            default=0,
        ),
        SarusParameter(
            name="skipna",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="numeric_only",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.kurtosis(**kwargs)


class pd_agg(ExternalOpImplementation):
    _transform_id = "pandas.PD_AGG"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="func",
            annotation=Optional[pdt.AggFuncTypeBase],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.agg(**kwargs)


class pd_droplevel(ExternalOpImplementation):
    _transform_id = "pandas.PD_DROPLEVEL"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="level",
            annotation=pd.Index,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.droplevel(**kwargs)


class pd_sort_values(ExternalOpImplementation):
    _transform_id = "pandas.PD_SORT_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="by",
            annotation=pdt.IndexLabel,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="ascending",
            annotation=Union[bool, List[bool], Tuple[bool, ...]],
            default=True,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="kind",
            annotation=str,
            default="quicksort",
        ),
        SarusParameter(
            name="na_position",
            annotation=str,
            default="last",
        ),
        SarusParameter(
            name="ignore_index",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="key",
            annotation=ValueKeyFunc,
            default=None,
        ),
        name=_transform_id,
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.sort_values(**kwargs)


class pd_sort_values_series(ExternalOpImplementation):
    _transform_id = "pandas.PD_SORT_VALUES_SERIES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Series,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="ascending",
            annotation=Union[bool, List[bool], Tuple[bool, ...]],
            default=True,
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="kind",
            annotation=str,
            default="quicksort",
        ),
        SarusParameter(
            name="na_position",
            annotation=str,
            default="last",
        ),
        SarusParameter(
            name="ignore_index",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="key",
            annotation=ValueKeyFunc,
            default=None,
        ),
        name=_transform_id,
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.sort_values(**kwargs)


class pd_drop_duplicates(ExternalOpImplementation):
    _transform_id = "pandas.PD_DROP_DUPLICATES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="subset",
            annotation=Optional[Union[Hashable, Sequence[Hashable]]],
            default=None,
        ),
        SarusParameter(
            name="keep",
            annotation=DropKeep,
            default="first",
        ),
        SarusParameter(
            name="inplace",
            annotation=bool,
            default=False,
            predicate=lambda x: x is False,
        ),
        SarusParameter(
            name="ignore_index",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["subset"]
            del kwargs["ignore_index"]
        return this.drop_duplicates(**kwargs)


class pd_corr(ExternalOpImplementation):
    _transform_id = "pandas.PD_CORR"
    _dp_equivalent_id = "pandas.PD_CORR_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="method",
            annotation=CorrelationMethod,
            default="pearson",
        ),
        SarusParameter(
            name="min_periods",
            annotation=int,
            default=1,
        ),
        # > 1.3.5
        # SarusParameter(
        #     name="numeric_only",
        #     annotation=bool,
        #     default=False,
        # ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.corr(**kwargs)


class pd_corr_series(ExternalOpImplementation):
    _transform_id = "pandas.PD_CORR_SERIES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Series,
        ),
        SarusParameter(
            name="other",
            annotation=pd.Series,
        ),
        SarusParameter(
            name="method",
            annotation=CorrelationMethod,
            default="pearson",
        ),
        SarusParameter(
            name="min_periods",
            annotation=int,
            default=1,
        ),
        # > 1.3.5
        # SarusParameter(
        #     name="numeric_only",
        #     annotation=bool,
        #     default=False,
        # ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.corr(**kwargs)


# ------ DataFrame & Series PROPERTIES ------
class pd_shape(ExternalOpImplementation):
    _transform_id = "pandas.PD_SHAPE"
    _dp_equivalent_id = "pandas.PD_SHAPE_DP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=t.Union[pd.Series, pd.DataFrame],
            condition=DATASPEC,
        )
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.shape


class pd_ndim(ExternalOpImplementation):
    _transform_id = "pandas.PD_NDIM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.ndim


class pd_name(ExternalOpImplementation):
    _transform_id = "pandas.PD_NAME"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Series,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.name


class pd_size(ExternalOpImplementation):
    _transform_id = "pandas.PD_SIZE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.size


class pd_axes(ExternalOpImplementation):
    _transform_id = "pandas.PD_AXES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.axes


class pd_columns(ExternalOpImplementation):
    _transform_id = "pandas.PD_COLUMNS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.columns


class pd_index(ExternalOpImplementation):
    _transform_id = "pandas.PD_INDEX"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.index


class pd_dtype(ExternalOpImplementation):
    _transform_id = "pandas.PD_DTYPE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Series,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.dtype


class pd_dtypes(ExternalOpImplementation):
    _transform_id = "pandas.PD_DTYPES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.dtypes


class pd_values(ExternalOpImplementation):
    _transform_id = "pandas.PD_VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.values


class pd_join(ExternalOpImplementation):
    _transform_id = "pandas.PD_JOIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="on",
            annotation=Optional[pdt.IndexLabel],
            default=None,
        ),
        SarusParameter(
            name="how",
            annotation=MergeHow,
            default="left",
        ),
        SarusParameter(
            name="lsuffix",
            annotation=str,
            default="",
        ),
        SarusParameter(
            name="rsuffix",
            annotation=str,
            default="",
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.join(**kwargs)


class pd_groupby(ExternalOpImplementation):
    _transform_id = "pandas.PD_GROUPBY"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="by",
            annotation=Union[Mapping, Callable, str, List[str], Tuple[str]],
            default=None,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="level",
            annotation=Optional[pdt.IndexLabel],
            default=None,
        ),
        SarusParameter(
            name="as_index",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="group_keys",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="observed",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="dropna",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.groupby(**kwargs)

    def pup_kind(self, signature: SarusBoundSignature) -> PUPKind:
        by = signature["axis"].static_value()
        if callable(by):
            return PUPKind.NOT_PUP
        else:
            return PUPKind.PUP


class pd_merge(ExternalOpImplementation):
    _transform_id = "pandas.PD_MERGE"
    _signature = SarusSignature(
        SarusParameter(
            name="left",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="right",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="how",
            annotation=MergeHow,
            default="inner",
        ),
        SarusParameter(
            name="on",
            annotation=Optional[Union[pdt.IndexLabel, List[pdt.IndexLabel]]],
            default=None,
        ),
        SarusParameter(
            name="left_on",
            annotation=Optional[Union[pdt.IndexLabel, List[pdt.IndexLabel]]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="right_on",
            annotation=Optional[Union[pdt.IndexLabel, List[pdt.IndexLabel]]],
            default=None,
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="left_index",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="right_index",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="suffixes",
            annotation=Tuple[str, str],
            default=("_x", "_y"),
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="indicator",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="validate",
            annotation=Optional[str],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.merge(**kwargs)


class pd_append(ExternalOpImplementation):
    _transform_id = "pandas.PD_APPEND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.DataFrame,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="ignore_index",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="verify_integrity",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.append(**kwargs)


class pd_nunique(ExternalOpImplementation):
    _transform_id = "pandas.PD_NUNIQUE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="dropna",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if signature["this"].python_type() == str(pd.Series):
            del kwargs["axis"]
        return this.nunique(**kwargs)


class pd_unique(ExternalOpImplementation):
    _transform_id = "pandas.PD_UNIQUE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Series,
            condition=DATASPEC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.unique()


class pd_rolling(ExternalOpImplementation):
    _transform_id = "pandas.PD_ROLLING"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
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
            annotation=str,
            default="single",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.rolling(**kwargs)


# ------ FUNCTIONS ------
class pd_eq(ExternalOpImplementation):
    _transform_id = "pandas.PD_EQ"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC | STATIC,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, other) = signature.collect_args()
        return this == other

    def pup_kind(self, signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pd_concat(ExternalOpImplementation):
    _transform_id = "pandas.PD_CONCAT"
    _signature = SarusSignature(
        SarusParameter(
            name="objs",
            annotation=Union[
                Iterable[pd.core.generic.NDFrame],
                Mapping[Hashable, pd.core.generic.NDFrame],
            ],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="axis",
            annotation=pdt.Axis,
            default=0,
        ),
        SarusParameter(
            name="join",
            annotation=str,
            default="outer",
        ),
        SarusParameter(
            name="ignore_index",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="keys",
            annotation=Optional[Any],
            default=None,
        ),
        SarusParameter(
            name="levels",
            annotation=Optional[Any],
            default=None,
        ),
        SarusParameter(
            name="names",
            annotation=Optional[Any],
            default=None,
        ),
        SarusParameter(
            name="verify_integrity",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="sort",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="copy",
            annotation=Optional[bool],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return pd.concat(**kwargs)


class pd_get_dummies(ExternalOpImplementation):
    _transform_id = "pandas.PD_GET_DUMMIES"
    _signature = SarusSignature(
        SarusParameter(
            name="data",
            annotation=Union[pd.DataFrame, pd.Series],
            condition=DATASPEC,
        ),
        SarusParameter(
            name="prefix",
            annotation=Optional[Union[str, Iterable[str], Dict[str, str]]],
            default=None,
        ),
        SarusParameter(
            name="prefix_sep",
            annotation=Union[str, Iterable[str], Dict[str, str]],
            default="_",
        ),
        SarusParameter(
            name="dummy_na",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="columns",
            annotation=Optional[List[str]],
            default=None,
        ),
        SarusParameter(
            name="sparse",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="drop_first",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="dtype",
            annotation=Optional[np.dtype],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> pd.DataFrame:
        kwargs = signature.collect_kwargs()
        return pd.get_dummies(**kwargs)


class pd_to_datetime(ExternalOpImplementation):
    _transform_id = "pandas.PD_TO_DATETIME"
    _signature = SarusSignature(
        SarusParameter(
            name="arg",
            annotation=DatetimeScalarOrArrayConvertible,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="errors",
            annotation=str,
            default="raise",
        ),
        SarusParameter(
            name="dayfirst",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="yearfirst",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="utc",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="format",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="exact",
            annotation=Union[bool, lib.NoDefault],
            default=lib.no_default,
        ),
        SarusParameter(
            name="unit",
            annotation=Optional[str],
            default=None,
        ),
        SarusParameter(
            name="infer_datetime_format",
            annotation=Union[bool, lib.NoDefault],
            default=lib.no_default,
        ),
        SarusParameter(
            name="origin",
            annotation=str,
            default="unix",
        ),
        SarusParameter(
            name="cache",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return pd.to_datetime(**kwargs)


# ------ INDEX METHODS ------
class pd_union(ExternalOpImplementation):
    _transform_id = "pandas.PD_UNION"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=pd.Index,
            condition=DATASPEC,
        ),
        SarusParameter(
            name="other",
            annotation=Union[pd.Index, pdt.ArrayLike],
            condition=DATASPEC | STATIC,
        ),
        SarusParameter(
            name="sort",
            annotation=Optional[bool],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.union(**kwargs)
