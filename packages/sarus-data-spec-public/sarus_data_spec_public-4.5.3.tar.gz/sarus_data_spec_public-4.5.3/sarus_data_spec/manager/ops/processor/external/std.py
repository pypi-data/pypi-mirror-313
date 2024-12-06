from typing import Any, Dict, Iterable, List, Optional, Union
import sarus_data_spec.typing as st
from sarus_data_spec.dataspec_validator.signature import (
    SarusBoundSignature,
    SarusParameter,
    SarusParameterArray,
    SarusParameterMapping,
    SarusSignature,
    SarusSignatureValue,
)
from sarus_data_spec.dataspec_validator.typing import PUPKind

from .external_op import ExternalOpImplementation


class add(ExternalOpImplementation):
    _transform_id = "std.ADD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this + other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class radd(ExternalOpImplementation):
    _transform_id = "std.RADD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return other + this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class sub(ExternalOpImplementation):
    _transform_id = "std.SUB"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
        name="substract",
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this - other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class rsub(ExternalOpImplementation):
    _transform_id = "std.RSUB"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return other - this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class mul(ExternalOpImplementation):
    _transform_id = "std.MUL"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
        name="multiply",
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this * other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class div(ExternalOpImplementation):
    _transform_id = "std.DIV"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this / other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class rdiv(ExternalOpImplementation):
    _transform_id = "std.RDIV"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return other / this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class invert(ExternalOpImplementation):
    _transform_id = "std.INVERT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return ~this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class length(ExternalOpImplementation):
    _transform_id = "std.LEN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return len(this)


class getitem(ExternalOpImplementation):
    _transform_id = "std.GETITEM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="key",
            annotation=Any,
        ),
        name=_transform_id,
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, key = signature.collect_args()
        return this[key]

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.PUP


class setitem(ExternalOpImplementation):
    _transform_id = "std.SETITEM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="key",
            annotation=Any,
        ),
        SarusParameter(
            name="value",
            annotation=Any,
        ),
        name=_transform_id,
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, key, value = signature.collect_args()
        this[key] = value
        return this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        token_value = bound_signature["value"].pup_token()
        token_previous = bound_signature["this"].pup_token()
        if token_value == token_previous:
            return PUPKind.TOKEN_PRESERVING
        return PUPKind.NOT_PUP


class greater_than(ExternalOpImplementation):
    _transform_id = "std.GT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this > other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class greater_equal(ExternalOpImplementation):
    _transform_id = "std.GE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this >= other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class lower_than(ExternalOpImplementation):
    _transform_id = "std.LT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this < other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class lower_equal(ExternalOpImplementation):
    _transform_id = "std.LE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this <= other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class not_equal(ExternalOpImplementation):
    _transform_id = "std.NE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this != other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class equal(ExternalOpImplementation):
    _transform_id = "std.EQ"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this == other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class neg(ExternalOpImplementation):
    _transform_id = "std.NEG"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return -this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class pos(ExternalOpImplementation):
    _transform_id = "std.POS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return +this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class _abs(ExternalOpImplementation):
    _transform_id = "std.ABS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return abs(this)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class _round(ExternalOpImplementation):
    _transform_id = "std.ROUND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return round(this)

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class modulo(ExternalOpImplementation):
    _transform_id = "std.MOD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this % other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class rmodulo(ExternalOpImplementation):
    _transform_id = "std.RMOD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return other % this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class _or(ExternalOpImplementation):
    _transform_id = "std.OR"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this | other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class ror(ExternalOpImplementation):
    _transform_id = "std.ROR"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return other | this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class _and(ExternalOpImplementation):
    _transform_id = "std.AND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return this & other

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class rand(ExternalOpImplementation):
    _transform_id = "std.RAND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, other = signature.collect_args()
        return other & this

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        return PUPKind.TOKEN_PRESERVING


class _int(ExternalOpImplementation):
    _transform_id = "std.INT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return int(this)


class _float(ExternalOpImplementation):
    _transform_id = "std.FLOAT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return float(this)


class _list(ExternalOpImplementation):
    _transform_id = "std.LIST"
    _signature = SarusSignature(
        SarusParameterArray(
            name="elem",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        elems = signature.collect_args()
        return list(elems)


class _dict(ExternalOpImplementation):
    _transform_id = "std.DICT"
    _signature = SarusSignature(
        SarusParameterMapping(
            name="elem",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        _, elems = signature.collect()
        return dict(**elems)


class _slice(ExternalOpImplementation):
    _transform_id = "std.SLICE"
    _signature = SarusSignature(
        SarusParameter(
            name="start",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="stop",
            annotation=int,
            default=-1,
        ),
        SarusParameter(
            name="step",
            annotation=Optional[int],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (start, stop, step) = signature.collect_args()
        return slice(start, stop, step)


class _set(ExternalOpImplementation):
    _transform_id = "std.SET"
    _signature = SarusSignature(
        SarusParameterArray(
            name="elem",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        elems = signature.collect_args()
        return set(elems)


class _tuple(ExternalOpImplementation):
    _transform_id = "std.TUPLE"
    _signature = SarusSignature(
        SarusParameterArray(
            name="elem",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        elems = signature.collect_args()
        return tuple(elems)


class _string(ExternalOpImplementation):
    _transform_id = "std.STRING"
    _signature = SarusSignature(
        SarusParameterArray(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return str(this)


class _bool(ExternalOpImplementation):
    _transform_id = "std.BOOL"
    _signature = SarusSignature(
        SarusParameterArray(
            name="this",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return bool(this)


class keys(ExternalOpImplementation):
    _transform_id = "std.KEYS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Dict,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return list(this.keys())


class values(ExternalOpImplementation):
    _transform_id = "std.VALUES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Dict,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return list(this.values())


class sudo(ExternalOpImplementation):
    _transform_id = "std.SUDO"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=Any,
        ),
        name="sudo",
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this

    def py_output_hint(
        self,
        transform: st.Transform,
        *arguments: Union[st.DataSpec, st.Transform],
        **named_arguments: Union[st.DataSpec, st.Transform],
    ) -> Optional[str]:
        assert len(named_arguments) == 0
        assert len(arguments) == 1
        dataspec = arguments[0]
        assert isinstance(dataspec, st.DataSpec)
        return dataspec.manager().python_type(dataspec)


class extend(ExternalOpImplementation):
    _transform_id = "std.EXTEND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=List,
        ),
        SarusParameter(
            name="other",
            annotation=List,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, other) = signature.collect_args()
        this.extend(other)
        return this


class append(ExternalOpImplementation):
    _transform_id = "std.APPEND"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=List,
        ),
        SarusParameter(
            name="other",
            annotation=Any,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, other) = signature.collect_args()
        this.append(other)
        return this


class pop(ExternalOpImplementation):
    _transform_id = "std.POP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=List,
        ),
        SarusParameter(
            name="index",
            annotation=int,
            default=-1,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, index) = signature.collect_args()
        return this.pop(index)


class split(ExternalOpImplementation):
    _transform_id = "std.SPLIT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="separator",
            annotation=str,
            default=" ",
        ),
        SarusParameter(
            name="maxsplit",
            annotation=int,
            default=-1,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, separator, maxsplit = signature.collect_args()
        return this.split(separator, maxsplit)


class join(ExternalOpImplementation):
    _transform_id = "std.JOIN"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="iterable",
            annotation=Iterable,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, iterable = signature.collect_args()
        return this.join(iterable)


class capitalize(ExternalOpImplementation):
    _transform_id = "std.CAPITALIZE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.capitalize()


class casefold(ExternalOpImplementation):
    _transform_id = "std.CASEFOLD"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.casefold()


class center(ExternalOpImplementation):
    _transform_id = "std.CENTER"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="width",
            annotation=int,
        ),
        SarusParameter(name="fillchar", annotation=str, default=" "),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, width, fillchar) = signature.collect_args()
        return this.center(width, fillchar)


class expandtabs(ExternalOpImplementation):
    _transform_id = "std.EXPANDTABS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="tabsize",
            annotation=int,
            default=8,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, tabsize) = signature.collect_args()
        return this.expandtabs(tabsize)


class lower(ExternalOpImplementation):
    _transform_id = "std.LOWER"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.lower()


class upper(ExternalOpImplementation):
    _transform_id = "std.UPPER"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.upper()


class lstrip(ExternalOpImplementation):
    _transform_id = "std.LSTRIP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="chars",
            annotation=str,
            default=" ",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, chars) = signature.collect_args()
        return this.lstrip(chars)


class rstrip(ExternalOpImplementation):
    _transform_id = "std.RSTRIP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="chars",
            annotation=str,
            default=" ",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, chars) = signature.collect_args()
        return this.rstrip(chars)


class strip(ExternalOpImplementation):
    _transform_id = "std.STRIP"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="chars",
            annotation=str,
            default=" ",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, chars) = signature.collect_args()
        return this.strip(chars)


class replace(ExternalOpImplementation):
    _transform_id = "std.REPLACE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
        SarusParameter(
            name="old",
            annotation=str,
        ),
        SarusParameter(
            name="new",
            annotation=str,
        ),
        SarusParameter(
            name="count",
            annotation=int,
            default=-1,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, old, new, count) = signature.collect_args()
        return this.replace(old, new, count)


class splitlines(ExternalOpImplementation):
    _transform_id = "std.SPLITLINES"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=str,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.splitlines()
