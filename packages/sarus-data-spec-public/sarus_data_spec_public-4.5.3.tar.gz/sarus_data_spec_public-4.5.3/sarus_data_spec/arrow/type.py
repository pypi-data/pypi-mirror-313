import typing as t

import pyarrow as pa

import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st

INTBASE_TO_ARROW = {
    st.IntegerBase.INT64: pa.int64(),
    st.IntegerBase.INT32: pa.int32(),
    st.IntegerBase.INT16: pa.int16(),
    st.IntegerBase.INT8: pa.int8(),
    st.IntegerBase.UINT64: pa.uint64(),
    st.IntegerBase.UINT32: pa.uint32(),
    st.IntegerBase.UINT16: pa.uint16(),
    st.IntegerBase.UINT8: pa.uint8(),
}

IDBASE_TO_ARROW = {
    st.IdBase.INT64: pa.int64(),
    st.IdBase.INT32: pa.int32(),
    st.IdBase.INT16: pa.int16(),
    st.IdBase.INT8: pa.int8(),
    st.IdBase.STRING: pa.large_string(),
    st.IdBase.BYTES: pa.binary(),
}

FLOATBASE_TO_ARROW = {
    st.FloatBase.FLOAT64: pa.float64(),
    st.FloatBase.FLOAT32: pa.float32(),
    st.FloatBase.FLOAT16: pa.float16(),
}

DATETIMEBASE_TO_ARROW = {
    st.DatetimeBase.INT64_NS: pa.timestamp("ns"),
    st.DatetimeBase.INT64_MS: pa.timestamp("ms"),
    st.DatetimeBase.STRING: pa.large_string(),
}

DATEBASE_TO_ARROW = {
    st.DateBase.INT32: pa.date32(),
    st.DateBase.STRING: pa.large_string(),
}

TIMEBASE_TO_ARROW = {
    st.TimeBase.INT64_US: pa.time64("us"),
    st.TimeBase.INT32_MS: pa.time32("ms"),
    st.TimeBase.STRING: pa.large_string(),
}


def to_arrow(
    _type: st.Type,
    nullable: bool = True,
) -> pa.DataType:
    """Visitor that maps sarus types to pa types
    See https://arrow.apache.org/docs/python/api/datatypes.html
    """

    class ToArrow(st.TypeVisitor):
        pa_type: pa.DataType

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.pa_type = pa.null()

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.pa_type = pa.null()

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.pa_type = pa.bool_()

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if base is not None:
                self.pa_type = IDBASE_TO_ARROW[base]

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = INTBASE_TO_ARROW[base]

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = pa.large_string()

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = FLOATBASE_TO_ARROW[base]

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = pa.large_string()

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.pa_type = pa.binary()

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = pa.struct(
                [
                    pa.field(
                        name=name,
                        type=to_arrow(field),
                        nullable=field.protobuf().HasField("optional")
                        or field.protobuf().HasField("unit"),
                    )
                    for name, field in fields.items()
                ]
            )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = pa.struct(
                [
                    pa.field(
                        name=name,
                        type=to_arrow(field),
                        nullable=True,
                    )
                    for name, field in fields.items()
                ]
                + [
                    pa.field(
                        name="field_selected",
                        type=pa.large_string(),
                        nullable=False,
                    )
                ]
            )

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = to_arrow(type, nullable=True)

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = pa.list_(
                to_arrow(type), -1
            )  # return variable length list

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
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
            self.pa_type = DATETIMEBASE_TO_ARROW[base]

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = TIMEBASE_TO_ARROW[base]

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = DATEBASE_TO_ARROW[base]

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.pa_type = pa.duration(unit)

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
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

    visitor = ToArrow()
    _type.accept(visitor)
    return visitor.pa_type


def from_arrow(type: pa.DataType) -> sdt.Type:
    # Integers
    if pa.types.is_int8(type):
        return sdt.Integer(base=st.IntegerBase.INT8)
    if pa.types.is_int16(type):
        return sdt.Integer(base=st.IntegerBase.INT16)
    if pa.types.is_int32(type):
        return sdt.Integer(base=st.IntegerBase.INT32)
    if pa.types.is_int64(type):
        return sdt.Integer(base=st.IntegerBase.INT64)
    if pa.types.is_uint8(type):
        return sdt.Integer(base=st.IntegerBase.UINT8)
    if pa.types.is_uint16(type):
        return sdt.Integer(base=st.IntegerBase.UINT16)
    if pa.types.is_uint32(type):
        return sdt.Integer(base=st.IntegerBase.UINT32)
    if pa.types.is_uint64(type):
        return sdt.Integer(base=st.IntegerBase.UINT64)

    # Floats
    if pa.types.is_float16(type):
        return sdt.Float(base=st.FloatBase.FLOAT16)
    if pa.types.is_float32(type):
        return sdt.Float(base=st.FloatBase.FLOAT32)
    if pa.types.is_float64(type):
        return sdt.Float(base=st.FloatBase.FLOAT64)
    if pa.types.is_string(type):
        return sdt.Text()
    if pa.types.is_large_string(type):
        return sdt.Text()
    if pa.types.is_boolean(type):
        return sdt.Boolean()

    # Temporal
    if pa.types.is_temporal(type):
        # Return True if value is an instance of date, time,
        # timestamp or duration.
        if pa.types.is_timestamp(type):
            return sdt.Datetime(base=st.DatetimeBase.INT64_NS)
            # TODO: when we will support different bases for datetime
            # we need to remove the asserts in the Datetime builder and
            # the error rise in the check_visitor in user_settings
        if pa.types.is_time(type):
            if type.unit in ["ns", "us"]:
                return sdt.Time(base=st.TimeBase.INT64_US)
            else:
                return sdt.Time(base=st.TimeBase.INT32_MS)

        if pa.types.is_date(type):
            return sdt.Date()
        else:
            # It is a duration
            if type.unit in ["s", "ms", "us"]:
                return sdt.Duration(unit=type.unit)
            else:
                raise ValueError(
                    "Duration type with nanosecond resolution not supported"
                )
    if pa.types.is_null(type):
        return sdt.Unit()
    if pa.types.is_struct(type):
        struct_type = t.cast(pa.StructType, type)
        return sdt.Struct(
            {
                struct_type.field(i).name: type_from_arrow(
                    struct_type.field(i).type, nullable=False
                )
                for i in range(struct_type.num_fields)
            }
        )
    if pa.types.is_list(type):
        list_type = t.cast(pa.ListType, type)
        return sdt.List(
            type=type_from_arrow(list_type.value_type, nullable=False)
        )
    raise NotImplementedError(f"Type {type} not implemented")


def type_from_arrow(
    arrow_type: pa.DataType,
    nullable: bool,
) -> st.Type:
    if nullable and not (pa.types.is_null(arrow_type)):
        return sdt.Optional(type=from_arrow(arrow_type))
    return from_arrow(arrow_type)
