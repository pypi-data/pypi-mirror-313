from __future__ import annotations

import datetime
import json
import typing as t

import numpy as np
import pandas as pd
import pyarrow as pa

from sarus_data_spec.base import Base
from sarus_data_spec.constants import (
    ARRAY_VALUES,
    DATA,
    LIST_VALUES,
    OPTIONAL_VALUE,
    PU_COLUMN,
    PUBLIC,
    TEXT_CHARSET,
    TEXT_MAX_LENGTH,
    WEIGHTS,
)
from sarus_data_spec.path import Path
from sarus_data_spec.path import path as path_builder
from sarus_data_spec.predicate import Predicate
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

try:
    import tensorflow as tf
except ModuleNotFoundError:
    pass

VisitedType = t.TypeVar("VisitedType")

DURATION_UNITS_TO_RANGE = {
    "us": (
        int(np.iinfo(np.int64).min / 1e3),
        int(np.iinfo(np.int64).max / 1e3),
    ),
    "ms": (
        int(np.iinfo(np.int64).min / 1e6),
        int(np.iinfo(np.int64).max / 1e6),
    ),
    "s": (
        int(np.iinfo(np.int64).min / 1e9),
        int(np.iinfo(np.int64).max / 1e9),
    ),
}

BASE_ID_TO_PROTO = {
    st.IdBase.INT64.value: sp.Type.Id.INT64,
    st.IdBase.INT32.value: sp.Type.Id.INT32,
    st.IdBase.INT16.value: sp.Type.Id.INT16,
    st.IdBase.INT8.value: sp.Type.Id.INT8,
    st.IdBase.STRING.value: sp.Type.Id.STRING,
    st.IdBase.BYTES.value: sp.Type.Id.BYTES,
}
BASE_INT_TO_PROTO = {
    st.IntegerBase.INT64.value: sp.Type.Integer.INT64,
    st.IntegerBase.INT32.value: sp.Type.Integer.INT32,
    st.IntegerBase.INT16.value: sp.Type.Integer.INT16,
    st.IntegerBase.INT8.value: sp.Type.Integer.INT8,
    st.IntegerBase.UINT64.value: sp.Type.Integer.UINT64,
    st.IntegerBase.UINT32.value: sp.Type.Integer.UINT32,
    st.IntegerBase.UINT16.value: sp.Type.Integer.UINT16,
    st.IntegerBase.UINT8.value: sp.Type.Integer.UINT8,
}
BASE_FLOAT_TO_PROTO = {
    st.FloatBase.FLOAT64.value: sp.Type.Float.FLOAT64,
    st.FloatBase.FLOAT32.value: sp.Type.Float.FLOAT32,
    st.FloatBase.FLOAT16.value: sp.Type.Float.FLOAT16,
}
BASE_DATE_TO_PROTO = {
    st.DateBase.INT32.value: sp.Type.Date.INT32,
    st.DateBase.STRING.value: sp.Type.Date.STRING,
}

BASE_TIME_TO_PROTO = {
    st.TimeBase.INT64_NS.value: sp.Type.Time.INT64_NS,
    st.TimeBase.INT64_US.value: sp.Type.Time.INT64_US,
    st.TimeBase.INT32_MS.value: sp.Type.Time.INT32_MS,
    st.TimeBase.STRING.value: sp.Type.Time.STRING,
}
BASE_DATETIME_TO_PROTO = {
    st.DatetimeBase.INT64_NS.value: sp.Type.Datetime.INT64_NS,
    st.DatetimeBase.INT64_MS.value: sp.Type.Datetime.INT64_MS,
    st.DatetimeBase.STRING.value: sp.Type.Datetime.STRING,
}


class Type(Base[sp.Type]):
    """A python class to describe types"""

    def prototype(self) -> t.Type[sp.Type]:
        """Return the type of the underlying protobuf."""
        return sp.Type

    def name(self) -> str:
        """Returns the name of the underlying protobuf."""
        return self.protobuf().name

    def has_privacy_unit_tracking(self) -> bool:
        """Return True if the Type has protection information."""
        protection_fields = {
            PUBLIC,
            PU_COLUMN,
            WEIGHTS,
        }

        if self.has_admin_columns():
            type = self.protobuf()
            field_names = {element.name for element in type.struct.fields}
            # there may be additional administrative columns
            return protection_fields.issubset(field_names)
        else:
            return False

    def has_admin_columns(self) -> bool:
        """Return True if the Type has administrative columns."""
        type = self.protobuf()
        if type.HasField("struct"):
            field_names = {element.name for element in type.struct.fields}
            # there may be additional administrative columns
            return DATA in field_names
        else:
            return False

    def data_type(self) -> Type:
        """Returns the first type level containing the data,
        hence skips the protected_entity struct if there is one"""
        if self.has_admin_columns():
            data_type = next(
                iter(
                    [
                        field.type
                        for field in self.protobuf().struct.fields
                        if field.name == DATA
                    ]
                ),
                None,
            )
            assert data_type
            return Type(data_type)
        else:
            return self

    # A Visitor acceptor
    def accept(self, visitor: st.TypeVisitor) -> None:
        dispatch: t.Callable[[], None] = {
            "null": lambda: visitor.Null(properties=self._protobuf.properties),
            "unit": lambda: visitor.Unit(properties=self._protobuf.properties),
            "boolean": lambda: visitor.Boolean(
                properties=self._protobuf.properties
            ),
            "integer": lambda: visitor.Integer(
                min=self._protobuf.integer.min,
                max=self._protobuf.integer.max,
                base=st.IntegerBase(self._protobuf.integer.base),
                possible_values=self._protobuf.integer.possible_values,
                properties=self._protobuf.properties,
            ),
            "id": lambda: visitor.Id(
                base=st.IdBase(self._protobuf.id.base),
                unique=self._protobuf.id.unique,
                reference=Path(self._protobuf.id.reference)
                if self._protobuf.id.reference != sp.Path()
                else None,
                properties=self._protobuf.properties,
            ),
            "enum": lambda: visitor.Enum(
                self._protobuf.name,
                [
                    (name_value.name, name_value.value)
                    for name_value in self._protobuf.enum.name_values
                ],
                self._protobuf.enum.ordered,
                properties=self._protobuf.properties,
            ),
            "float": lambda: visitor.Float(
                min=self._protobuf.float.min,
                max=self._protobuf.float.max,
                base=st.FloatBase(self._protobuf.float.base),
                possible_values=self._protobuf.float.possible_values,
                properties=self._protobuf.properties,
            ),
            "text": lambda: visitor.Text(
                self._protobuf.text.encoding,
                possible_values=self._protobuf.text.possible_values,
                properties=self._protobuf.properties,
            ),
            "bytes": lambda: visitor.Bytes(
                properties=self._protobuf.properties
            ),
            "struct": lambda: visitor.Struct(
                {
                    field.name: Type(field.type)
                    for field in self._protobuf.struct.fields
                },
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "union": lambda: visitor.Union(
                {
                    field.name: Type(field.type)
                    for field in self._protobuf.union.fields
                },
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "optional": lambda: visitor.Optional(
                Type(self._protobuf.optional.type),
                None if self._protobuf.name == "" else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "list": lambda: visitor.List(
                Type(self._protobuf.list.type),
                max_size=self._protobuf.list.max_size,
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "array": lambda: visitor.Array(
                Type(self._protobuf.array.type),
                tuple(self._protobuf.array.shape),
                None if self._protobuf.name == "" else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "datetime": lambda: visitor.Datetime(
                self._protobuf.datetime.format,
                self._protobuf.datetime.min,
                self._protobuf.datetime.max,
                st.DatetimeBase(self._protobuf.datetime.base),
                possible_values=self._protobuf.datetime.possible_values,
                properties=self._protobuf.properties,
            ),
            "date": lambda: visitor.Date(
                self._protobuf.date.format,
                self._protobuf.date.min,
                self._protobuf.date.max,
                st.DateBase(self._protobuf.date.base),
                possible_values=self._protobuf.date.possible_values,
                properties=self._protobuf.properties,
            ),
            "time": lambda: visitor.Time(
                self._protobuf.time.format,
                self._protobuf.time.min,
                self._protobuf.time.max,
                st.TimeBase(self._protobuf.time.base),
                possible_values=self._protobuf.time.possible_values,
                properties=self._protobuf.properties,
            ),
            "duration": lambda: visitor.Duration(
                self._protobuf.duration.unit,
                self._protobuf.duration.min,
                self._protobuf.duration.max,
                possible_values=self._protobuf.duration.possible_values,
                properties=self._protobuf.properties,
            ),
            "constrained": lambda: visitor.Constrained(
                Type(self._protobuf.constrained.type),
                Predicate(self._protobuf.constrained.constraint),
                None if self._protobuf.name == "" else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "hypothesis": lambda: visitor.Hypothesis(
                *[
                    (Type(scored.type), scored.score)
                    for scored in self._protobuf.hypothesis.types
                ],
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            None: lambda: None,
        }[self._protobuf.WhichOneof("type")]
        dispatch()

    # A NewVisitor acceptor
    def accept_(self, visitor: st.TypeVisitor_[VisitedType]) -> VisitedType:
        dispatch: t.Callable[[], VisitedType] = {
            "null": lambda: visitor.Null(properties=self._protobuf.properties),
            "unit": lambda: visitor.Unit(properties=self._protobuf.properties),
            "boolean": lambda: visitor.Boolean(
                properties=self._protobuf.properties
            ),
            "integer": lambda: visitor.Integer(
                min=self._protobuf.integer.min,
                max=self._protobuf.integer.max,
                base=st.IntegerBase(self._protobuf.integer.base),
                possible_values=self._protobuf.integer.possible_values,
                properties=self._protobuf.properties,
            ),
            "id": lambda: visitor.Id(
                base=st.IdBase(self._protobuf.id.base),
                unique=self._protobuf.id.unique,
                reference=Path(self._protobuf.id.reference)
                if self._protobuf.id.reference != sp.Path()
                else None,
                properties=self._protobuf.properties,
            ),
            "enum": lambda: visitor.Enum(
                self._protobuf.name,
                [
                    (name_value.name, name_value.value)
                    for name_value in self._protobuf.enum.name_values
                ],
                self._protobuf.enum.ordered,
                properties=self._protobuf.properties,
            ),
            "float": lambda: visitor.Float(
                min=self._protobuf.float.min,
                max=self._protobuf.float.max,
                base=st.FloatBase(self._protobuf.float.base),
                possible_values=self._protobuf.float.possible_values,
                properties=self._protobuf.properties,
            ),
            "text": lambda: visitor.Text(
                self._protobuf.text.encoding,
                possible_values=self._protobuf.text.possible_values,
                properties=self._protobuf.properties,
            ),
            "bytes": lambda: visitor.Bytes(
                properties=self._protobuf.properties
            ),
            "struct": lambda: visitor.Struct(
                {
                    field.name: Type(field.type).accept_(visitor)
                    for field in self._protobuf.struct.fields
                },
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "union": lambda: visitor.Union(
                {
                    field.name: Type(field.type).accept_(visitor)
                    for field in self._protobuf.union.fields
                },
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "optional": lambda: visitor.Optional(
                Type(self._protobuf.optional.type).accept_(visitor),
                None if self._protobuf.name == "" else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "list": lambda: visitor.List(
                Type(self._protobuf.list.type).accept_(visitor),
                max_size=self._protobuf.list.max_size,
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "array": lambda: visitor.Array(
                Type(self._protobuf.array.type).accept_(visitor),
                tuple(self._protobuf.array.shape),
                None if self._protobuf.name == "" else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "datetime": lambda: visitor.Datetime(
                self._protobuf.datetime.format,
                self._protobuf.datetime.min,
                self._protobuf.datetime.max,
                st.DatetimeBase(self._protobuf.datetime.base),
                possible_values=self._protobuf.datetime.possible_values,
                properties=self._protobuf.properties,
            ),
            "date": lambda: visitor.Date(
                self._protobuf.date.format,
                self._protobuf.date.min,
                self._protobuf.date.max,
                st.DateBase(self._protobuf.date.base),
                possible_values=self._protobuf.date.possible_values,
                properties=self._protobuf.properties,
            ),
            "time": lambda: visitor.Time(
                self._protobuf.time.format,
                self._protobuf.time.min,
                self._protobuf.time.max,
                st.TimeBase(self._protobuf.time.base),
                possible_values=self._protobuf.time.possible_values,
                properties=self._protobuf.properties,
            ),
            "duration": lambda: visitor.Duration(
                self._protobuf.duration.unit,
                self._protobuf.duration.min,
                self._protobuf.duration.max,
                possible_values=self._protobuf.duration.possible_values,
                properties=self._protobuf.properties,
            ),
            "constrained": lambda: visitor.Constrained(
                Type(self._protobuf.constrained.type).accept_(visitor),
                Predicate(self._protobuf.constrained.constraint),
                None if self._protobuf.name == "" else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            "hypothesis": lambda: visitor.Hypothesis(
                *[
                    (Type(scored.type).accept_(visitor), scored.score)
                    for scored in self._protobuf.hypothesis.types
                ],
                name=None
                if self._protobuf.name == ""
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            None: lambda: visitor.default(),
        }[self._protobuf.WhichOneof("type")]
        return dispatch()

    def latex(self) -> str:
        """return a latex representation of the type"""

        class Latex(TypeVisitor_[str]):
            def default(self) -> str:
                return r""

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"\emptyset"

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"\mathbb{1}"

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"\left\{0,1\right}"

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if (
                    min <= np.iinfo(np.int32).min
                    or max >= np.iinfo(np.int32).max
                ):
                    return r"\mathbb{N}"
                else:
                    return r"\left[" + str(min) + r".." + str(max) + r"\right]"

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                result = ""
                if len(name_values) > 3:
                    result += r"\left\{"
                    for name, _ in name_values[:2]:
                        result += r"\text{" + name + r"}, "
                    result += r",\ldots, "
                    for name, _ in name_values[-1:]:
                        result += r"\text{" + name + r"}, "
                    result = result[:-2] + r"\right\}"
                elif len(name_values) > 0:
                    result = r"\left\{"
                    for name, _ in name_values:
                        result += r"\text{" + name + r"}, "
                    result = result[:-2] + r"\right\}"
                else:
                    result = self.Unit()
                return result

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if (
                    min <= np.finfo(np.float32).min
                    or max >= np.finfo(np.float32).max
                ):
                    return r"\mathbb{R}"
                else:
                    return r"\left[" + str(min) + r", " + str(max) + r"\right]"

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"\text{Text}"

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"\text{Bytes}"

            def Struct(
                self,
                fields: t.Mapping[str, str],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if len(fields) > 0:
                    if name is None:
                        result = r"\left\{"
                    else:
                        result = r"\text{" + name + r"}: \left\{"
                    for type_name, type_ in fields.items():
                        result = (
                            result
                            + r"\text{"
                            + type_name
                            + r"}:"
                            + type_
                            + r", "
                        )
                    result = result[:-2] + r"\right\}"
                    return result
                else:
                    return self.Unit()

            def Union(
                self,
                fields: t.Mapping[str, str],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                result = ""
                if len(fields) > 0:
                    for type_ in fields.values():
                        result = result + type_ + r" | "
                    result = result[:-2]
                    result = r"\left(" + result + r"\right)"
                else:
                    result = self.Null()
                return result

            def Optional(
                self,
                type_: str,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return type_ + r"?"

            def List(
                self,
                type_: str,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if max_size < 100:
                    return type_ + r"^{" + str(max_size) + r"}"
                else:
                    return type_ + r"^*"

            def Array(
                self,
                type_: str,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return (
                    type_
                    + r"^{"
                    + r"\times ".join([str(i) for i in shape])
                    + r"}"
                )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"\text{Datetime}"

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"\text{Date}"

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"\text{Time}"

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"\text{Duration}"

            def Hypothesis(
                self,
                *types: t.Tuple[str, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                result = ""
                if len(types) > 0:
                    for type_, score in types:
                        result = result + type_ + f",{score}|"
                    result = result[:-2]
                    result = r"\langle" + result + r"\rangle"
                else:
                    result = self.Null()
                return result

        visitor = Latex()
        return self.accept_(visitor)

    def compact(self: st.Type) -> str:
        """return a compact representation of the type"""

        class Compact(TypeVisitor_[str]):
            def default(self) -> str:
                return r""

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"∅"

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"𝟙"

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"𝔹"

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if (
                    min <= np.iinfo(np.int32).min
                    or max >= np.iinfo(np.int32).max
                ):
                    return r"ℕ"
                else:
                    return r"[" + str(min) + r".." + str(max) + r"]"

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                result = r""
                if len(name_values) > 3:
                    result = r"{"
                    for name, _ in name_values[:2]:
                        result += name
                    result += r",..., "
                    for name, _ in name_values[-1:]:
                        result += name + r", "
                    result = result[:-2] + r"}"
                    return result
                elif len(name_values) > 0:
                    result = r"{"
                    for name, _ in name_values:
                        result += name + r", "
                    result = result[:-2] + r"}"
                else:
                    result = self.Unit()
                return result

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if (
                    min <= np.finfo(np.float32).min
                    or max >= np.finfo(np.float32).max
                ):
                    return r"ℝ"
                else:
                    return r"[" + str(min) + r", " + str(max) + r"]"

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"𝒯"

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> str:
                return r"ℬ"

            def Struct(
                self,
                fields: t.Mapping[str, str],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if len(fields) > 0:
                    if name is None:
                        result = "{"
                    else:
                        result = name + r": {"
                    for type_name, type_ in fields.items():
                        result = result + type_name + r": " + type_ + r", "
                    result = result[:-2] + r"}"
                    return result
                else:
                    return self.Unit()

            def Union(
                self,
                fields: t.Mapping[str, str],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if len(fields) > 0:
                    result = ""
                    for compact in fields.values():
                        result = result + compact + r" | "
                    result = r"(" + result[:-2] + r")"
                    return result
                else:
                    return self.Null()

            def Optional(
                self,
                type_: str,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return type_ + r"?"

            def List(
                self,
                type_: str,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return type_ + r"*"

            def Array(
                self,
                type_: str,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return (
                    type_ + r"**(" + r"x".join([str(i) for i in shape]) + r")"
                )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"𝒟𝓉"

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"𝒟𝒶"

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"𝒯𝓂"

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                return r"𝒟𝓊"

            def Hypothesis(
                self,
                *types: t.Tuple[str, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> str:
                if len(types) > 0:
                    result = r"<"
                    for type_, score in types:
                        result = result + type_ + f",{score}|"
                    result = result[:-1] + r">"
                    return result
                else:
                    return self.Null()

        visitor = Compact()
        return self.accept_(visitor)

    def get(self: Type, item: st.Path) -> Type:
        """Return a projection of the considered type defined by the path.
        The projection contains all the parents types of the leaves of
        the path. If the path stops at a Union, Struct or Optional,
        it also returns that type with everything it contains."""

        class Get(TypeVisitor):
            result = Type(sp.Type())

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Null()

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Id(base=base, unique=unique, reference=reference)

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Unit(properties=self.properties)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Boolean()

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Integer(
                    min=min,
                    max=max,
                    possible_values=possible_values,
                    properties=self.properties,
                )

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Enum(
                    name=name,
                    name_values=name_values,
                    ordered=ordered,
                    properties=self.properties,
                )

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Float(
                    min=min,
                    max=max,
                    possible_values=possible_values,
                    properties=self.properties,
                )

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Text(
                    encoding=encoding,
                    possible_values=possible_values,
                    properties=self.properties,
                )

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Bytes()

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                new_fields = {}
                for path in proto.paths:
                    # here struct each path must have a label
                    new_fields[path.label] = fields[path.label].get(Path(path))
                self.result = Struct(
                    fields=new_fields if len(new_fields) > 0 else fields,
                    name=name if name is not None else "Struct",
                    properties=self.properties,
                )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                new_fields = {}
                for path in proto.paths:
                    new_fields[path.label] = fields[path.label].get(Path(path))
                self.result = Union(
                    fields=new_fields if len(new_fields) > 0 else fields,
                    name=name if name is not None else "Union",
                    properties=self.properties,
                )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) <= 1
                self.result = Optional(
                    type.get(Path(proto.paths[0]))
                    if len(proto.paths) > 0
                    else type,
                    name=t.cast(str, name),
                    properties=self.properties,
                )

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) <= 1
                self.result = List(
                    type.get(Path(proto.paths[0]))
                    if len(proto.paths) > 0
                    else type,
                    name=t.cast(str, name),
                    max_size=max_size,
                    properties=self.properties,
                )

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) <= 1
                self.result = Array(
                    type.get(Path(proto.paths[0]))
                    if len(proto.paths) > 0
                    else type,
                    name=t.cast(str, name),
                    shape=shape,
                    properties=self.properties,
                )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Datetime(
                    format=format,
                    min=min,
                    max=max,
                    properties=self.properties,
                    base=base,
                    possible_values=possible_values,
                )

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Date(
                    format=format,
                    min=min,
                    max=max,
                    properties=self.properties,
                    base=base,
                    possible_values=possible_values,
                )

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Time(
                    format=format,
                    min=min,
                    max=max,
                    properties=self.properties,
                    base=base,
                    possible_values=possible_values,
                )

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert not item.has_sub_paths()
                self.result = Duration(
                    unit=unit,
                    min=min,
                    max=max,
                    properties=self.properties,
                    possible_values=possible_values,
                )

        visitor = Get(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def sub_types(self: Type, item: st.Path) -> t.List[st.Type]:
        """Returns a list of the subtypes corresponding to the
        leaves of the input path"""

        class SubTypes(TypeVisitor):
            def __init__(self, type_item: st.Type):
                self.result = [type_item]

            def default(self) -> None:
                pass

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for sub_path in item.sub_paths():
                    result.extend(fields[sub_path.label()].sub_types(sub_path))
                if len(result) > 0:
                    self.result = result
                    # otherwise struct is empty and it is a terminal node

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for sub_path in item.sub_paths():
                    result.extend(fields[sub_path.label()].sub_types(sub_path))
                if len(result) > 0:
                    self.result = result
                    # otherwise union is empty and it is a terminal node

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                if len(item.sub_paths()) == 1:
                    result.extend(type.sub_types(item.sub_paths()[0]))
                    self.result = result

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                if len(item.sub_paths()) == 1:
                    result.extend(type.sub_types(item.sub_paths()[0]))
                    self.result = result

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                if len(item.sub_paths()) == 1:
                    result.extend(type.sub_types(item.sub_paths()[0]))
                    self.result = result

        visitor = SubTypes(type_item=self)
        self.accept(visitor)
        return visitor.result

    def structs(self: Type) -> t.Optional[t.List[st.Path]]:
        """Returns the path to the first level structs encountered in the type.
        For example, Union[Struct1,Union[Struct2[Struct3]] will return only a
        path that brings to Struct1 and Struct2.
        """

        class Structs(TypeVisitor):
            result: t.Optional[t.List[st.Path]] = None

            def default(self) -> None:
                pass

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = []

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                paths = []
                for type_name, curr_type in fields.items():
                    if curr_type.protobuf().WhichOneof("type") == "struct":
                        paths.append(Path(sp.Path(label=type_name)))
                    else:
                        sub_paths = curr_type.structs()
                        if sub_paths is not None:
                            paths.extend(
                                [
                                    Path(
                                        sp.Path(
                                            label=type_name,
                                            paths=[subpath.protobuf()],
                                        )
                                    )
                                    for subpath in sub_paths
                                ]
                            )
                if len(paths) > 0:
                    self.result = t.cast(t.List[st.Path], paths)

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if type.protobuf().WhichOneof("type") == "struct":
                    self.result = [Path(sp.Path(label=OPTIONAL_VALUE))]
                else:
                    sub_paths = type.structs()
                    if sub_paths is not None:
                        self.result = [
                            Path(
                                sp.Path(
                                    label=OPTIONAL_VALUE,
                                    paths=[
                                        subpath.protobuf()
                                        for subpath in sub_paths
                                    ],
                                )
                            )
                        ]

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if type.protobuf().WhichOneof("type") == "struct":
                    self.result = [Path(sp.Path(label=LIST_VALUES))]
                else:
                    sub_paths = type.structs()
                    if sub_paths is not None:
                        self.result = [
                            Path(
                                sp.Path(
                                    label=LIST_VALUES,
                                    paths=[
                                        subpath.protobuf()
                                        for subpath in sub_paths
                                    ],
                                )
                            )
                        ]

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if type.protobuf().WhichOneof("type") == "struct":
                    self.result = [Path(sp.Path(label=ARRAY_VALUES))]
                else:
                    sub_paths = type.structs()
                    if sub_paths is not None:
                        self.result = [
                            Path(
                                sp.Path(
                                    label=ARRAY_VALUES,
                                    paths=[
                                        subpath.protobuf()
                                        for subpath in sub_paths
                                    ],
                                )
                            )
                        ]

        visitor = Structs()
        self.accept(visitor)
        return visitor.result

    def leaves(self: st.Type) -> t.List[st.Type]:
        """Returns a list of the sub-types corresponding to
        the leaves of the type tree structure"""

        class AddLeaves(TypeVisitor):
            result: t.List[st.Type] = []

            def __init__(self, type_item: st.Type):
                self.result = [type_item]

            def default(self) -> None:
                pass

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for item_name in fields.keys():
                    result.extend(fields[item_name].leaves())
                if len(result) > 0:
                    self.result = result

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for item_name in fields.keys():
                    result.extend(fields[item_name].leaves())
                if len(result) > 0:
                    self.result = result

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                result.extend(type.leaves())
                if len(result) > 0:
                    self.result = result

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                result.extend(type.leaves())
                if len(result) > 0:
                    self.result = result

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                result.extend(type.leaves())
                if len(result) > 0:
                    self.result = result

        visitor = AddLeaves(type_item=self)
        self.accept(visitor)
        return visitor.result

    def children(self: st.Type) -> t.Dict[str, st.Type]:
        """Returns the children contained in the type tree structure"""

        class GetChildren(TypeVisitor):
            result: t.Dict[str, st.Type] = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties

            def default(self) -> None:
                pass

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = t.cast(t.Dict[str, st.Type], fields)

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = t.cast(t.Dict[str, st.Type], fields)

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {OPTIONAL_VALUE: type}

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {LIST_VALUES: type}

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {ARRAY_VALUES: type}

        visitor = GetChildren(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def example(self) -> pa.Array:
        """This methods returns a pyarrow scalar that matches the type.
        For an optional type, we consider the case where, the field
        is not missing.
        """

        class Example(TypeVisitor):
            result = pa.nulls(0)

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.nulls(1)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array([True], type=pa.bool_())

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if base == st.IdBase.STRING:
                    self.Text(
                        encoding="",
                        possible_values=["1"],
                        properties={
                            TEXT_CHARSET: '["1"]',
                            TEXT_MAX_LENGTH: "1",
                        },
                    )
                elif base in (
                    st.IdBase.INT8,
                    st.IdBase.INT16,
                    st.IdBase.INT32,
                    st.IdBase.INT64,
                ):
                    int_base = {
                        st.IdBase.INT8: st.IntegerBase.INT8,
                        st.IdBase.INT16: st.IntegerBase.INT16,
                        st.IdBase.INT32: st.IntegerBase.INT32,
                        st.IdBase.INT64: st.IntegerBase.INT64,
                    }[base]
                    self.Integer(
                        min=1, max=1, base=int_base, possible_values=[1]
                    )
                else:
                    raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pa_type: pa.DataType = {
                    st.IntegerBase.INT8: pa.int8(),
                    st.IntegerBase.INT16: pa.int16(),
                    st.IntegerBase.INT32: pa.int32(),
                    st.IntegerBase.INT64: pa.int64(),
                }[base]
                possible_values = t.cast(list, possible_values)
                if len(possible_values) > 0:
                    self.result = pa.array([possible_values[0]], type=pa_type)
                else:
                    self.result = pa.array(
                        [int((min + max) / 2)], type=pa_type
                    )

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([name_values[0][0]], pa.large_string())

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pa_type: pa.DataType = {
                    st.FloatBase.FLOAT16: pa.float16(),
                    st.FloatBase.FLOAT32: pa.float32(),
                    st.FloatBase.FLOAT64: pa.float64(),
                }[base]

                possible_values = t.cast(list, possible_values)
                if len(possible_values) > 0:
                    x: t.Union[float, np.float16] = possible_values[0]
                else:
                    x = (min + max) / 2
                if base == st.FloatBase.FLOAT16:
                    out: t.Union[float, np.float16] = np.float16(x)
                else:
                    out = x
                self.result = pa.array([out], type=pa_type)

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                possible_values = t.cast(list, possible_values)
                if len(possible_values) > 0:
                    self.result = pa.array(
                        [possible_values[0]], pa.large_string()
                    )
                else:
                    try:
                        char_set = json.loads(self.properties[TEXT_CHARSET])
                    except json.JSONDecodeError:
                        self.result = pa.array(
                            ["Anonymyzed"], pa.large_string()
                        )
                    else:
                        max_length = int(self.properties[TEXT_MAX_LENGTH])
                        ex = (
                            np.array(char_set)
                            .astype(np.uint32)
                            .view("U" + str(len(char_set)))[0]
                        )
                        if len(ex) > max_length:
                            ex = ex[:max_length]
                        self.result = pa.array([ex], pa.large_string())

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array(
                    [bytes("1", "utf-8")], pa.binary(length=1)
                )

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                assert properties is not None
                if properties["kind"] == "text":
                    max_size = fields["input_ids"].protobuf().list.max_size
                    if max_size == np.iinfo(np.int64).max:
                        # there is no convention given
                        # on the max size so we take 1
                        pos_ids = pa.ListArray.from_arrays(
                            offsets=[0, 1],
                            values=pa.concat_arrays([pa.array([0])]),
                        )
                        attention_mask = pa.ListArray.from_arrays(
                            offsets=[0, 1],
                            values=pa.concat_arrays([pa.array([1])]),
                        )
                        input_ids = pa.ListArray.from_arrays(
                            offsets=[0, 1],
                            values=pa.concat_arrays([pa.array([0])]),
                        )
                    else:
                        pos_ids = pa.ListArray.from_arrays(
                            offsets=[0, max_size],
                            values=pa.array(range(0, max_size)),
                        )

                        attention_mask = pa.ListArray.from_arrays(
                            offsets=[0, max_size],
                            values=pa.array([1] * max_size),
                        )

                        input_ids = pa.ListArray.from_arrays(
                            offsets=[0, max_size],
                            values=pa.array([0] * max_size),
                        )

                    self.result = pa.StructArray.from_arrays(
                        arrays=[input_ids, attention_mask, pos_ids],
                        fields=[
                            pa.field(
                                name="input_ids",
                                type=input_ids.type,
                                nullable=False,
                            ),
                            pa.field(
                                name="attention_mask",
                                type=attention_mask.type,
                                nullable=False,
                            ),
                            pa.field(
                                name="position_ids",
                                type=pos_ids.type,
                                nullable=False,
                            ),
                        ],
                    )

                else:
                    arrays = [
                        field_type.example() for field_type in fields.values()
                    ]

                    self.result = pa.StructArray.from_arrays(
                        arrays=arrays,
                        fields=[
                            pa.field(
                                name=field_name,
                                nullable=field_type.protobuf().HasField(
                                    "optional"
                                )
                                or field_type.protobuf().HasField("unit"),
                                type=array.type,
                            )
                            for (field_name, field_type), array in zip(
                                fields.items(), arrays
                            )
                        ],
                    )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                n_fields = len(fields)
                arrays = []
                for j, field_type in enumerate(fields.values()):
                    middle_arr = field_type.example()
                    early_arr = pa.nulls(j, type=middle_arr.type)
                    late_arr = pa.nulls(n_fields - j - 1, type=middle_arr.type)
                    arrays.append(
                        pa.concat_arrays([early_arr, middle_arr, late_arr])
                    )
                names = list(fields.keys())
                arrays.append(pa.array(names, pa.large_string()))
                names.append("field_selected")
                self.result = pa.StructArray.from_arrays(
                    arrays=arrays,
                    names=names,
                )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = type.example()

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                sub_type = type.example()
                # build ListArray with one single repeated value
                if max_size == np.iinfo(np.int64).max:
                    # there is no convention given on the max size so we take 1
                    self.result = pa.ListArray.from_arrays(
                        offsets=[0, 1], values=pa.concat_arrays([sub_type])
                    )
                else:
                    self.result = pa.ListArray.from_arrays(
                        offsets=[0, max_size],
                        values=pa.concat_arrays(
                            [sub_type for _ in range(max_size)]
                        ),
                    )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                possible_values = t.cast(list, possible_values)
                if len(possible_values) > 0:
                    self.result = pa.array(
                        pd.to_datetime([possible_values[0]], format=format),
                        pa.timestamp("ns"),
                    )
                else:
                    self.result = pa.array(
                        pd.to_datetime([max], format=format),
                        pa.timestamp("ns"),
                    )

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                possible_values = t.cast(list, possible_values)
                if len(possible_values) > 0:
                    val = possible_values[0]
                else:
                    val = max
                if base == st.DateBase.INT32:
                    self.result = pa.array(
                        pd.to_datetime([val], format=format),
                        pa.date32(),
                    )
                else:
                    self.result = pa.array(
                        [val],
                        pa.large_string(),
                    )

        visitor = Example(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def numpy_example(self) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it returns a non missing value of the type.
        """
        return self.example().to_numpy(zero_copy_only=False)  # type:ignore

    def tensorflow_example(self) -> t.Any:
        """This methods returns a dictionary where the leaves are
        tf tensors. For optional types, we consider the case
        where the field is not missing.
        """

        class TensorflowExample(TypeVisitor):
            result = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant([np.NaN], dtype=tf.float64)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant([1], dtype=tf.int64)

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if base == st.IdBase.STRING:
                    self.result = tf.constant(["1"], tf.string)
                elif base == st.IdBase.INT64:
                    self.result = tf.constant([1], tf.int64)
                else:
                    raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([int((min + max) / 2)], tf.int64)

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([name_values[0][0]], tf.string)

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([(min + max) / 2], dtype=tf.float64)

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                try:
                    char_set = json.loads(self.properties[TEXT_CHARSET])
                except json.JSONDecodeError:
                    self.result = tf.constant([""], tf.string)
                else:
                    max_length = int(self.properties[TEXT_MAX_LENGTH])
                    ex = (
                        np.array(char_set)
                        .astype(np.uint32)
                        .view("U" + str(len(char_set)))[0]
                    )
                    if len(ex) > max_length:
                        ex = ex[:max_length]
                    self.result = tf.constant([ex], tf.string)

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant(["1"], tf.string)

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_example()
                    for field_name, field_type in fields.items()
                }

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_example()
                    for field_name, field_type in fields.items()
                }

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    "input_mask": tf.constant([1], dtype=tf.int64),
                    "values": type.tensorflow_example(),
                }

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([min], dtype=tf.string)

        visitor = TensorflowExample(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def default(self) -> pa.Array:
        """This methods returns a pyarrow scalar that matches the type.
        For an optional type, we consider the case where, the field
        is missing.
        """

        class Default(TypeVisitor):
            result = pa.nulls(0)

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.nulls(0)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array([True], type=pa.bool_())

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if base == st.IdBase.STRING:
                    self.result = pa.array(["1"], pa.large_string())
                elif base == st.IdBase.INT64:
                    self.result = pa.array([1], pa.int64())
                else:
                    raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([int((min + max) / 2)], type=pa.int64())

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([name_values[0][0]], pa.large_string())

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([(min + max) / 2], type=pa.float64())

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                try:
                    char_set = json.loads(self.properties[TEXT_CHARSET])
                except json.JSONDecodeError:
                    self.result = pa.array([""], pa.large_string())
                else:
                    max_length = int(self.properties[TEXT_MAX_LENGTH])
                    ex = "".join(char_set)
                    if len(ex) > max_length:
                        ex = ex[:max_length]
                    self.result = pa.array([ex], pa.large_string())

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array(
                    [bytes("1", "utf-8")], pa.binary(length=1)
                )

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.StructArray.from_arrays(
                    arrays=[
                        field_type.default() for field_type in fields.values()
                    ],
                    names=list(fields.keys()),
                )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                n_fields = len(fields)
                arrays = []
                for j, field_type in enumerate(fields.values()):
                    middle_arr = field_type.default()
                    early_arr = pa.nulls(j, type=middle_arr.type)
                    late_arr = pa.nulls(n_fields - j - 1, type=middle_arr.type)
                    arrays.append(
                        pa.concat_arrays([early_arr, middle_arr, late_arr])
                    )
                names = list(fields.keys())
                arrays.append(pa.array(names, pa.large_string()))
                names.append("field_selected")
                self.result = pa.StructArray.from_arrays(
                    arrays=arrays,
                    names=names,
                )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([None], type=type.default().type)

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array(
                    pd.to_datetime([max], format=format), pa.timestamp("ns")
                )

        visitor = Default(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def numpy_default(self) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it sets the default missing value
        """
        return self.default().to_numpy(zero_copy_only=False)  # type:ignore

    def tensorflow_default(self, is_optional: bool = False) -> t.Any:
        """This methods returns a dictionary with tensors as leaves
        that match the type.
        For an optional type, we consider the case where the field
        is missing, and set the default value for each missing type.
        """

        class ToTensorflow(TypeVisitor):
            result = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant([np.NaN], dtype=tf.float64)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                if is_optional:
                    self.result = tf.constant(
                        [np.iinfo(np.int64).max], dtype=tf.int64
                    )
                else:
                    self.result = tf.constant([1], dtype=tf.int64)

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if is_optional:
                    if base == st.IdBase.STRING:
                        self.result = tf.constant([""], dtype=tf.string)
                    elif base == st.IdBase.INT64:
                        self.result = tf.constant(
                            [np.iinfo(np.int64).max], pa.large_string()
                        )
                    else:
                        raise NotImplementedError
                else:
                    if base == st.IdBase.STRING:
                        self.result = tf.constant(["1"], tf.string)
                    elif base == st.IdBase.INT64:
                        self.result = tf.constant([1], tf.int64)
                    else:
                        raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant(
                        [np.iinfo(np.int64).min], dtype=tf.int64
                    )
                else:
                    self.result = tf.constant(
                        [int((min + max) / 2)], dtype=tf.int64
                    )

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([""], dtype=tf.string)
                else:
                    self.result = tf.constant([name_values[0][0]], tf.string)

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([np.NaN], dtype=tf.float64)
                else:
                    self.result = tf.constant(
                        [(min + max) / 2], dtype=tf.float64
                    )

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([""], dtype=tf.string)
                else:
                    try:
                        char_set = json.loads(self.properties[TEXT_CHARSET])
                    except json.JSONDecodeError:
                        self.result = tf.constant([""], tf.string)
                    else:
                        max_length = int(self.properties[TEXT_MAX_LENGTH])
                        ex = "".join(char_set)
                        if len(ex) > max_length:
                            ex = ex[:max_length]
                        self.result = tf.constant([ex], tf.string)

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                if is_optional:
                    self.result = tf.constant([""], dtype=tf.string)
                else:
                    self.result = tf.constant(["1"], tf.string)

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_default(
                        is_optional=is_optional
                    )
                    for field_name, field_type in fields.items()
                }

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_default(
                        is_optional=is_optional
                    )
                    for field_name, field_type in fields.items()
                }

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    "input_mask": tf.constant([0], dtype=tf.int64),
                    "values": type.tensorflow_default(is_optional=True),
                }

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([""], dtype=tf.string)
                else:
                    self.result = tf.constant([min], dtype=tf.string)

        visitor = ToTensorflow(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def path_leaves(self) -> t.Sequence[st.Path]:
        """Returns the list of each path to a leaf in the type. If the type
        is a leaf, it returns an empty list"""

        class PathLeaves(TypeVisitor):
            result = []

            def default(self) -> None:
                pass

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                for field_name, field_type in fields.items():
                    sub_paths = field_type.path_leaves()
                    if len(sub_paths) > 0:
                        self.result.extend(
                            [
                                path_builder(label=field_name, paths=[el])
                                for el in sub_paths
                            ]
                        )
                    else:
                        self.result.extend(
                            [path_builder(label=field_name, paths=[])]
                        )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                for field_name, field_type in fields.items():
                    sub_paths = field_type.path_leaves()
                    if len(sub_paths) > 0:
                        self.result.extend(
                            [
                                path_builder(label=field_name, paths=[el])
                                for el in sub_paths
                            ]
                        )
                    else:
                        self.result.extend(
                            [path_builder(label=field_name, paths=[])]
                        )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                sub_paths = type.path_leaves()
                if len(sub_paths) > 0:
                    self.result.extend(
                        [
                            path_builder(label=OPTIONAL_VALUE, paths=[el])
                            for el in sub_paths
                        ]
                    )
                else:
                    self.result.extend(
                        [path_builder(label=OPTIONAL_VALUE, paths=[])]
                    )

        visitor = PathLeaves()
        self.accept(visitor)
        return visitor.result


# A New Visitor base implementation
class TypeVisitor(st.TypeVisitor):
    """A base implementation for visitor class"""

    def default(self) -> None:
        raise NotImplementedError

    def Null(self, properties: t.Optional[t.Mapping[str, str]] = None) -> None:
        self.default()

    def Unit(self, properties: t.Optional[t.Mapping[str, str]] = None) -> None:
        self.default()

    def Boolean(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None:
        self.default()

    def Id(
        self,
        unique: bool,
        reference: t.Optional[st.Path] = None,
        base: t.Optional[st.IdBase] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Integer(
        self,
        min: int,
        max: int,
        base: st.IntegerBase,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Enum(
        self,
        name: str,
        name_values: t.Sequence[t.Tuple[str, int]],
        ordered: bool,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Float(
        self,
        min: float,
        max: float,
        base: st.FloatBase,
        possible_values: t.Iterable[float],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Text(
        self,
        encoding: str,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Bytes(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None:
        self.default()

    def Struct(
        self,
        fields: t.Mapping[str, st.Type],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Union(
        self,
        fields: t.Mapping[str, st.Type],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Optional(
        self,
        type: st.Type,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def List(
        self,
        type: st.Type,
        max_size: int,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Array(
        self,
        type: st.Type,
        shape: t.Tuple[int, ...],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Datetime(
        self,
        format: str,
        min: str,
        max: str,
        base: st.DatetimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Time(
        self,
        format: str,
        min: str,
        max: str,
        base: st.TimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Date(
        self,
        format: str,
        min: str,
        max: str,
        base: st.DateBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Duration(
        self,
        unit: str,
        min: int,
        max: int,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Constrained(
        self,
        type: st.Type,
        constraint: st.Predicate,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()

    def Hypothesis(
        self,
        *types: t.Tuple[st.Type, float],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        self.default()


# A New Visitor base implementation
class TypeVisitor_(st.TypeVisitor_[VisitedType]):
    """A base implementation for visitor class"""

    def default(self) -> VisitedType:
        """This is the minimal implementation to provide"""
        raise NotImplementedError

    def Null(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType:
        return self.default()

    def Unit(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType:
        return self.default()

    def Boolean(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType:
        return self.default()

    def Id(
        self,
        unique: bool,
        reference: t.Optional[st.Path] = None,
        base: t.Optional[st.IdBase] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Integer(
        self,
        min: int,
        max: int,
        base: st.IntegerBase,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Enum(
        self,
        name: str,
        name_values: t.Sequence[t.Tuple[str, int]],
        ordered: bool,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Float(
        self,
        min: float,
        max: float,
        base: st.FloatBase,
        possible_values: t.Iterable[float],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Text(
        self,
        encoding: str,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Bytes(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType:
        return self.default()

    def Struct(
        self,
        fields: t.Mapping[str, VisitedType],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Union(
        self,
        fields: t.Mapping[str, VisitedType],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Optional(
        self,
        type: VisitedType,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def List(
        self,
        type: VisitedType,
        max_size: int,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Array(
        self,
        type: VisitedType,
        shape: t.Tuple[int, ...],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Datetime(
        self,
        format: str,
        min: str,
        max: str,
        base: st.DatetimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Time(
        self,
        format: str,
        min: str,
        max: str,
        base: st.TimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Date(
        self,
        format: str,
        min: str,
        max: str,
        base: st.DateBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Duration(
        self,
        unit: str,
        min: int,
        max: int,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Constrained(
        self,
        type: VisitedType,
        constraint: st.Predicate,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()

    def Hypothesis(
        self,
        *types: t.Tuple[VisitedType, float],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType:
        return self.default()


# A few builders
def Null(
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(name="Null", null=sp.Type.Null(), properties=properties)
    )


def Unit(properties: t.Optional[t.Mapping[str, str]] = None) -> Type:
    return Type(
        sp.Type(name="Unit", unit=sp.Type.Unit(), properties=properties)
    )


def Id(
    unique: bool,
    base: t.Optional[st.IdBase] = None,
    reference: t.Optional[st.Path] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if base is None:
        base = st.IdBase.STRING
    if reference is None:
        return Type(
            sp.Type(
                name="Id",
                id=sp.Type.Id(
                    base=BASE_ID_TO_PROTO[base.value],
                    unique=unique,
                ),
                properties=properties,
            )
        )
    return Type(
        sp.Type(
            name="Id",
            id=sp.Type.Id(
                base=BASE_ID_TO_PROTO[base.value],
                unique=unique,
                reference=reference.protobuf(),
            ),
            properties=properties,
        )
    )


def Boolean(
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name="Boolean", boolean=sp.Type.Boolean(), properties=properties
        )
    )


def Integer(
    min: t.Optional[int] = None,
    max: t.Optional[int] = None,
    base: t.Optional[st.IntegerBase] = None,
    possible_values: t.Optional[t.Iterable[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if base is None:
        base = st.IntegerBase.INT64
    if min is None:
        if base == st.IntegerBase.INT64:
            min = np.iinfo(np.int64).min
        elif base == st.IntegerBase.INT32:
            min = np.iinfo(np.int32).min
        elif base == st.IntegerBase.INT16:
            min = np.iinfo(np.int16).min
        else:
            min = np.iinfo(np.int8).min
    if max is None:
        if base == st.IntegerBase.INT64:
            max = np.iinfo(np.int64).max
        elif base == st.IntegerBase.INT32:
            max = np.iinfo(np.int32).max
        elif base == st.IntegerBase.INT16:
            max = np.iinfo(np.int16).max
        else:
            max = np.iinfo(np.int8).max
    return Type(
        sp.Type(
            name="Integer",
            integer=sp.Type.Integer(
                base=BASE_INT_TO_PROTO[base.value],
                min=min,
                max=max,
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Enum(
    name: str,
    name_values: t.Union[
        t.Sequence[str], t.Sequence[int], t.Sequence[t.Tuple[str, int]]
    ],
    ordered: bool = False,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    enum_name_values: t.List[sp.Type.Enum.NameValue]
    if len(name_values) == 0:
        raise ValueError("No enum values")
    if isinstance(name_values[0], str):
        name_values = t.cast(t.Sequence[str], name_values)
        enum_name_values = [
            sp.Type.Enum.NameValue(name=n, value=v)
            for v, n in enumerate(sorted(name_values))
        ]
    elif isinstance(name_values[0], int):
        name_values = t.cast(t.Sequence[int], name_values)
        enum_name_values = [
            sp.Type.Enum.NameValue(name=str(v), value=v)
            for v in sorted(name_values)
        ]
    elif isinstance(name_values[0], tuple):
        name_values = t.cast(t.Sequence[t.Tuple[str, int]], name_values)
        enum_name_values = [
            sp.Type.Enum.NameValue(name=n, value=v)
            for n, v in sorted(name_values)
        ]
    return Type(
        sp.Type(
            name=name,
            enum=sp.Type.Enum(
                base=sp.Type.Enum.Base.INT64,
                ordered=ordered,
                name_values=enum_name_values,
            ),
            properties=properties,
        )
    )


def Float(
    min: t.Optional[float] = None,
    max: t.Optional[float] = None,
    base: t.Optional[st.FloatBase] = None,
    possible_values: t.Optional[t.Iterable[float]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if base is None:
        base = st.FloatBase.FLOAT64
    if min is None:
        if base == st.FloatBase.FLOAT64:
            min = np.finfo(np.float64).min  # type:ignore
        elif base == st.FloatBase.FLOAT32:
            min = np.finfo(np.float32).min  # type:ignore
        else:
            min = np.finfo(np.float16).min  # type:ignore
    if max is None:
        if base == st.FloatBase.FLOAT64:
            max = np.finfo(np.float64).max  # type:ignore
        elif base == st.FloatBase.FLOAT32:
            max = np.finfo(np.float32).max  # type:ignore
        else:
            max = np.finfo(np.float16).max  # type:ignore
    return Type(
        sp.Type(
            name="Float64",
            float=sp.Type.Float(
                base=BASE_FLOAT_TO_PROTO[base.value],
                min=min,  # type:ignore
                max=max,  # type:ignore
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Text(
    encoding: str = "UTF-8",
    possible_values: t.Optional[t.Iterable[str]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=f"Text {encoding}",
            text=sp.Type.Text(
                encoding="UTF-8", possible_values=possible_values
            ),
            properties=properties,
        )
    )


def Bytes() -> Type:
    return Type(sp.Type(name="Bytes", bytes=sp.Type.Bytes()))


def Struct(
    fields: t.Mapping[str, st.Type],
    name: str = "Struct",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            struct=sp.Type.Struct(
                fields=[
                    sp.Type.Struct.Field(name=name, type=type.protobuf())
                    for name, type in fields.items()
                ]
            ),
            properties=properties,
        )
    )


def Union(
    fields: t.Mapping[str, st.Type],
    name: str = "Union",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            union=sp.Type.Union(
                fields=[
                    sp.Type.Union.Field(
                        name=field_name, type=field_type.protobuf()
                    )
                    for field_name, field_type in fields.items()
                ]
            ),
            properties=properties,
        )
    )


def Optional(
    type: st.Type,
    name: str = "Optional",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            optional=sp.Type.Optional(type=type.protobuf()),
            properties=properties,
        )
    )


def List(
    type: st.Type,
    max_size: int = np.iinfo(np.int64).max,
    name: str = "List",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            list=sp.Type.List(type=type.protobuf(), max_size=max_size),
            properties=properties,
        )
    )


def Array(
    type: st.Type,
    shape: t.Sequence[int],
    name: str = "Array",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            array=sp.Type.Array(type=type.protobuf(), shape=shape),
            properties=properties,
        )
    )


def Datetime(
    format: t.Optional[str] = None,
    min: t.Optional[str] = None,
    max: t.Optional[str] = None,
    base: t.Optional[st.DatetimeBase] = None,
    possible_values: t.Optional[t.Iterable[str]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if format is None:
        format = "%Y-%m-%dT%H:%M:%S"
    if base is None:
        base = st.DatetimeBase.INT64_NS
    assert base == st.DatetimeBase.INT64_NS
    bounds = []
    iint64 = np.iinfo(np.int64)
    for i, bound in enumerate((min, max)):
        if bound is None:  # the bound is assumed to be sound otherwise
            # This starts with the true bounds for the type datetime64[ns]
            # However, storing dates as string implies an aliasing:
            # datetime.datetime cannot be more precise than µs.
            # So this would truncate the nanoseconds:
            # ```
            # min = (min + np.timedelta64(1, "us")).astype("datetime64[us]")
            # max = max.astype("datetime64[us]")
            # ```
            # More generally, the date format can only store a bound lower
            # than that bound, which is fine with the max but not for the
            # min, as it truncates some time units.
            if i == 0:
                int_bound = iint64.min + 1  # iint64.min maps to 'NaT'
                aliasing = np.timedelta64(0, "ns")
                # This looks for the lowest offset for the format:
                # see:
                # https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-and-timedelta-arithmetic
                for unit, np_unit in [
                    ("%Y", "Y"),
                    ("%m", "M"),
                    ("%d", "D"),
                    ("%H", "h"),
                    ("%M", "m"),
                    ("%S", "s"),
                    ("%f", "us"),
                ]:
                    if unit not in format:
                        break
                    elif unit in ["%m", "%Y"]:
                        # months and years have variable length
                        as_unit = np.datetime64(int_bound, np_unit)
                        aliasing = np.timedelta64(1, np_unit)
                        aliasing = as_unit + aliasing - as_unit
                        aliasing = aliasing.astype("timedelta64[ns]")
                    else:
                        aliasing = np.timedelta64(1, np_unit)
            elif i == 1:
                int_bound = iint64.max
                aliasing = np.timedelta64(0, "ns")
            bound = str(
                (np.datetime64(int_bound, "ns") + aliasing).astype(
                    "datetime64[us]"
                )
            )
            bound = datetime.datetime.strptime(
                bound, "%Y-%m-%dT%H:%M:%S.%f"
            ).strftime(format)
        bounds.append(bound)

    return Type(
        sp.Type(
            name="Datetime",
            datetime=sp.Type.Datetime(
                format=format,
                min=bounds[0],
                max=bounds[1],
                base=BASE_DATETIME_TO_PROTO[base.value],
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Date(
    format: t.Optional[str] = None,
    min: t.Optional[str] = None,
    max: t.Optional[str] = None,
    possible_values: t.Optional[t.Iterable[str]] = None,
    base: t.Optional[st.DateBase] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    """Inspired by pyarrow.date32() type. This is compatible with
    pyarrow-pandas integration:
    https://arrow.apache.org/docs/python/pandas.html#pandas-arrow-conversion

    pyarrow.date32() and not pyarrow.date64() because the later isndefined as:
    "milliseconds since UNIX epoch 1970-01-01"
    which is a bit bizarre since there are multiple integers representing
    a single date.

    Default ranges are defined by datetime.date lowest and highest year:
    0001-01-01 and 9999-12-31. Note that if the SQL database has a date outside
    of this range the table reflection would fail since also sql alchemy is
    using datetime.date as an underlying python type.
    """

    if format is None:
        format = "%Y-%m-%d"

    if base is None:
        base = st.DateBase.INT32

    if min is None:
        min = datetime.datetime.strptime(
            str(datetime.date(datetime.MINYEAR, 1, 1)), "%Y-%m-%d"
        ).strftime(format)
    if max is None:
        max = datetime.datetime.strptime(
            str(datetime.date(datetime.MAXYEAR, 12, 31)), "%Y-%m-%d"
        ).strftime(format)

    return Type(
        sp.Type(
            name="Date",
            date=sp.Type.Date(
                format=format,
                min=min,
                max=max,
                base=BASE_DATE_TO_PROTO[base.value],
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Time(
    format: t.Optional[str] = None,
    min: t.Optional[str] = None,
    max: t.Optional[str] = None,
    possible_values: t.Optional[t.Iterable[str]] = None,
    base: t.Optional[st.TimeBase] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    """Very similar to Datetime. The difference here is that the
    range is simpler.
    """
    if format is None:
        format = "%H:%M:%S.%f"
    if base is None:
        base = st.TimeBase.INT64_US
    if base == st.TimeBase.INT64_NS:
        raise NotImplementedError(
            "time with nanoseconds resolution not supported"
        )
    if min is None:
        min = datetime.time.min.strftime(
            format.replace("%f", "{__subseconds__}").format(
                __subseconds__=(
                    "000000" if base == st.TimeBase.INT64_US else "000"
                )
            )
        )
    if max is None:
        max = datetime.time.max.strftime(
            format.replace("%f", "{__subseconds__}").format(
                __subseconds__=(
                    "999999" if base == st.TimeBase.INT64_US else "999"
                )
            )
        )

    return Type(
        sp.Type(
            name="Time",
            time=sp.Type.Time(
                format=format,
                min=min,
                max=max,
                base=BASE_TIME_TO_PROTO[base.value],
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Duration(
    unit: t.Optional[str] = None,
    min: t.Optional[int] = None,
    max: t.Optional[int] = None,
    possible_values: t.Optional[t.Iterable[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    """Inspired by pythons datetime.timedelta,
    It stores duration as int64 with microseconds resolution.
    If unit is provided the range is adjusted accodingly.
    Compatible with pyarrow.duration(unit). All pyarrow units are valid:
    https://arrow.apache.org/docs/python/generated/pyarrow.duration.html
    except for 'ns' because it is incompatible with SQLAlchemy types
    (backed by python's datetime.timedelta which has up to 'us' resolution)
    and it would cause problems when pushing to sql (also SQL duration
    types have up to 'us' resolution).

    It raises an error if the unit provided is not among:
    ('us','ms', 's'). Default value 'us'
    """
    if unit is None:
        unit = "us"

    default_bounds = DURATION_UNITS_TO_RANGE.get(unit)
    if default_bounds is None:
        raise ValueError(
            f"Duration unit {unit} not recongnized"
            f"Only values in {DURATION_UNITS_TO_RANGE.keys()} are allowed"
        )

    bounds = [
        default_bounds[0] if min is None else min,
        default_bounds[1] if max is None else max,
    ]

    return Type(
        sp.Type(
            name="Duration",
            duration=sp.Type.Duration(
                unit=unit,
                min=bounds[0],
                max=bounds[1],
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Constrained(
    type: st.Type,
    constraint: Predicate,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name="Constrained",
            constrained=sp.Type.Constrained(
                type=type.protobuf(), constraint=constraint._protobuf
            ),
            properties=properties,
        )
    )


def Hypothesis(
    *types: t.Tuple[st.Type, float],
    name: str = "Hypothesis",
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            hypothesis=sp.Type.Hypothesis(
                types=(
                    sp.Type.Hypothesis.Scored(type=v.protobuf(), score=s)
                    for v, s in types
                )
            ),
            properties=properties,
        )
    )


def extract_filter_from_types(
    initial_type: st.Type, goal_type: st.Type
) -> st.Type:
    class FilterVisitor(TypeVisitor):
        """Visitor that select type for filtering, it only takes
        the Union types of the goal type and the rest is taken from
        the initial type
        """

        filter_type = initial_type

        def default(self) -> None:
            pass

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the goal type
            self.filter_type = Union(
                fields={
                    field_name: extract_filter_from_types(
                        initial_type=initial_type.children()[field_name],
                        goal_type=field_type,
                    )
                    for field_name, field_type in fields.items()
                }
            )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the initial type
            self.filter_type = Struct(
                fields={
                    field_name: (
                        extract_filter_from_types(
                            initial_type=field_type,
                            goal_type=fields[field_name],
                        )
                        if fields.get(field_name) is not None
                        else field_type
                    )
                    for field_name, field_type in initial_type.children().items()  # noqa: E501
                }
            )

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here it does not change
            self.filter_type = Optional(
                type=extract_filter_from_types(
                    initial_type=initial_type.children()[OPTIONAL_VALUE],
                    goal_type=type,
                )
            )

    visitor = FilterVisitor()
    goal_type.accept(visitor)
    return visitor.filter_type


def extract_project_from_types(
    initial_type: st.Type, goal_type: st.Type
) -> st.Type:
    class ProjectVisitor(TypeVisitor):
        """Visitor that select type for projecting, it only takes
        the Project types of the goal type and the rest is taken from
        the initial type
        """

        project_type = initial_type

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the initial type
            self.project_type = Union(
                fields={
                    field_name: (
                        extract_filter_from_types(
                            initial_type=field_type,
                            goal_type=fields[field_name],
                        )
                        if fields.get(field_name) is not None
                        else field_type
                    )
                    for field_name, field_type in initial_type.children().items()  # noqa: E501
                }
            )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the goal type
            self.project_type = Struct(
                fields={
                    field_name: extract_project_from_types(
                        initial_type=initial_type.children()[field_name],
                        goal_type=field_type,
                    )
                    for field_name, field_type in fields.items()
                }
            )

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here it does not change
            self.project_type = Optional(
                type=extract_filter_from_types(
                    initial_type=initial_type.children()[OPTIONAL_VALUE],
                    goal_type=type,
                )
            )

    visitor = ProjectVisitor()
    goal_type.accept(visitor)
    return visitor.project_type


def protected_type(input_type: st.Type) -> st.Type:
    """Convert a data Type to a protected Type."""
    protection_fields = {
        PUBLIC: Boolean(),
        PU_COLUMN: Optional(type=Id(base=st.IdBase.STRING, unique=False)),
        WEIGHTS: Float(min=0.0, max=np.finfo(np.float64).max),  # type: ignore
    }
    if input_type.has_privacy_unit_tracking():
        # Already protected
        return input_type
    elif input_type.has_admin_columns():
        # Add protection to existing admin columns
        fields = {
            **input_type.children(),
            **protection_fields,
        }
        return Struct(fields=fields)
    else:
        # Add admin columns
        fields = {
            DATA: input_type,
            **protection_fields,
        }
        return Struct(fields=fields)


def to_numeric_string(
    sds_type: st.Type,
) -> t.Literal[
    "int64", "int32", "int16", "int8", "float32", "float64", "boolean"
]:
    class ToNumericString(st.TypeVisitor):
        """Visitor that converts sarus type to a string"""

        str_type: t.Literal[
            "int64", "int32", "int16", "int8", "float32", "float64", "boolean"
        ]

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if base == st.IntegerBase.INT32:
                self.str_type = "int32"
            elif base == st.IntegerBase.INT64:
                self.str_type = "int64"
            elif base == st.IntegerBase.INT8:
                self.str_type = "int8"
            elif base == st.IntegerBase.INT16:
                self.str_type = "int16"
            else:
                raise NotImplementedError

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if base == st.FloatBase.FLOAT32:
                self.str_type = "float32"
            elif base == st.FloatBase.FLOAT64:
                self.str_type = "float64"

            else:
                raise NotImplementedError

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.str_type = "boolean"

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

    visitor = ToNumericString()
    sds_type.accept(visitor)
    return visitor.str_type


if t.TYPE_CHECKING:
    test_type: st.Type = Type(sp.Type())
