from typing import cast
import json
import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec import Transform
from sarus_data_spec.path import Path, path
from sarus_data_spec.protobuf.typing import Protobuf
from sarus_data_spec.protobuf.utilities import from_base64, to_base64
from sarus_data_spec.transform import filter, project
import sarus_data_spec.protobuf as sp
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st


def select_rows(
    _type: st.Type, array: pa.Array, is_optional: bool = False
) -> t.Tuple[pa.Array, pa.Array]:
    """Visitor selecting columns based on the type.
    The idea is that at each level,
    the filter for the array is computed, and for the union,
    we remove the fields that we want to filter among
    the columns
    TODO: implement missing types
    """

    class RowsSelector(st.TypeVisitor):
        batch_array: pa.Array = array
        filter_indices: pa.Array

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.filter_indices = pa.array(
                np.ones(len(self.batch_array.to_pylist())).astype("bool")
            )

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.filter_indices = pa.array(
                np.ones(len(self.batch_array.to_pylist())).astype("bool")
            )

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
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
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
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
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
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
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            if is_optional:
                self.filter_indices = pa.array(
                    np.ones(len(self.batch_array.to_pylist())).astype("bool")
                )
            else:
                self.filter_indices = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # no projection, we keep all existing children
            assert len(fields) == self.batch_array.type.num_fields
            pa_fields = list(self.batch_array.type)

            arrays_indices = [
                select_rows(
                    fields[field_name],
                    self.batch_array.flatten()[
                        self.batch_array.type.get_field_index(field_name)
                    ],
                )
                for field_name in fields.keys()
            ]

            final_index = np.logical_and.reduce(
                [array_index[1] for array_index in arrays_indices]
            )
            if is_optional:
                self.filter_indices = pa.array(final_index)
            else:
                index_nulls = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )
                self.filter_indices = pa.compute.and_(
                    pa.array(final_index), index_nulls
                )
            self.batch_array = pa.StructArray.from_arrays(
                [element[0] for element in arrays_indices],
                fields=pa_fields,
            )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
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
            new_array, filter_indices = select_rows(
                type, self.batch_array, is_optional=True
            )
            self.batch_array = new_array
            self.filter_indices = filter_indices

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # build filter array for this level
            initial_field_selected = self.batch_array.field(
                "field_selected"
            ).to_numpy(zero_copy_only=False)

            indices = [
                initial_field_selected == field_name
                for field_name in fields.keys()
            ]
            index = np.logical_or.reduce(indices)
            union_level_filter = pa.array(index)

            # now get sub-levels filter_indices
            arrays = [
                self.batch_array.flatten()[
                    self.batch_array.type.get_field_index(field_name)
                ]
                for i, (field_name, field_type) in enumerate(fields.items())
            ]
            arrays_indices = [
                select_rows(typ, arr)
                for typ, arr in zip(fields.values(), arrays)
            ]
            low_level_indices = [
                array_index[1] for array_index in arrays_indices
            ]
            low_level_filter = np.logical_or.reduce(low_level_indices)

            final_filter = pa.compute.and_(
                low_level_filter, union_level_filter
            )
            if is_optional:
                self.filter_indices = final_filter
            else:
                index_nulls = pa.compute.invert(
                    self.batch_array.is_null(nan_is_null=True)
                )
                self.filter_indices = pa.compute.and_(
                    final_filter, index_nulls
                )

            fields_name = list(fields.keys())
            # here we need to take arrays modified from low level
            selected_arrays = [
                array_index[0] for array_index in arrays_indices
            ]
            struct_fields = [
                pa.field(name=field_name, type=arr.type)
                for arr, field_name in zip(selected_arrays, fields_name)
            ]
            struct_fields.append(
                pa.field(
                    name="field_selected",
                    type=pa.large_string(),
                    nullable=False,
                )
            )
            selected_arrays.append(self.batch_array.field("field_selected"))
            self.batch_array = pa.StructArray.from_arrays(
                selected_arrays,
                fields=struct_fields,
            )

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

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = RowsSelector()
    _type.accept(visitor)
    return visitor.batch_array, visitor.filter_indices


def select_columns(_type: st.Type, array: pa.Array) -> pa.Array:
    """Visitor selecting columns based on the type.
    The idea is that at each level,
    the filter for the array is computed, and for the union,
    we remove the fields that we want to filter among
    the columns. Currently, it is not possible
    to filter Optional values.
    TODO: implement missing types
    """

    class ColumnsSelector(st.TypeVisitor):
        batch_array: pa.Array = array

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            flattened = self.batch_array.flatten()
            pa_type = self.batch_array.type
            arrays = [
                select_columns(
                    field_type,
                    flattened[pa_type.get_field_index(field_name)],
                )
                for field_name, field_type in fields.items()
            ]
            pa_fields = [
                pa_type.field(field_name).with_type(arrays[i].type)
                for i, field_name in enumerate(fields.keys())
            ]
            self.batch_array = pa.StructArray.from_arrays(
                arrays,
                fields=pa_fields,
            )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
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
            self.batch_array = select_columns(type, self.batch_array)

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert len(fields) == self.batch_array.type.num_fields - 1
            # -1 because field_selected is not in the fields
            pa_fields = list(self.batch_array.type)
            arrays = [
                select_columns(
                    field_type,
                    self.batch_array.flatten()[
                        self.batch_array.type.get_field_index(field_name)
                    ].filter(
                        pa.array(
                            self.batch_array.field("field_selected").to_numpy(
                                zero_copy_only=False
                            )
                            == field_name
                        )
                    ),
                )
                for field_name, field_type in fields.items()
            ]
            sizes = [len(array) for array in arrays]
            structs = []
            for i, array in enumerate(arrays):
                structs.append(
                    pa.concat_arrays(
                        [
                            # TODO: slices of same array
                            pa.array([None] * sum(sizes[:i]), type=array.type),
                            array,
                            pa.array(
                                sum(sizes[i + 1 :]) * [None], type=array.type
                            ),
                        ]
                    )
                )

            structs.append(self.batch_array.field("field_selected"))
            pa_fields = [
                field.with_type(array.type)
                for field, array in zip(self.batch_array.type, structs)
            ]
            self.batch_array = pa.StructArray.from_arrays(
                structs,
                fields=pa_fields,
            )

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
            pass

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

    visitor = ColumnsSelector()
    _type.accept(visitor)
    return visitor.batch_array


def filter_project_from_types(
    initial_type: st.Type, goal_type: st.Type
) -> t.Tuple[Transform, Transform]:
    """Creates the filtering and projection to be executed
    in that order to obtain the goal type from the initial type"""

    filter_type = sdt.extract_filter_from_types(initial_type, goal_type)
    return filter(filter=filter_type), project(projection=goal_type)


def filter_primary_keys(old_pks: str, new_type: st.Type) -> str:
    """Keeps only primary keys path that appear in new type"""
    filtered_pks = []
    primary_keys = [
        Path(cast(sp.Path, from_base64(proto, cast(Protobuf, sp.Path))))
        for proto in json.loads(old_pks)
    ]
    for primary_key in primary_keys:
        try:
            new_type.get(primary_key)
        except KeyError:
            pass

        else:
            filtered_pks.append(to_base64(primary_key.protobuf()))
    return json.dumps(filtered_pks)


def update_fks(curr_type: st.Type, original_type: st.Type) -> st.Type:
    """TODO: implement missing types"""

    class Select(st.TypeVisitor):
        result = curr_type

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            new_fields = {}
            for fieldname, fieldtype in fields.items():
                new_fields[fieldname] = update_fks(
                    curr_type=fieldtype, original_type=original_type
                )

            self.result = sdt.Struct(
                fields=new_fields,
                name=name if name is not None else "Struct",
                properties=properties,
            )
            # otherwise struct is empty and it is a terminal node

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            new_fields = {}
            for fieldname, fieldtype in fields.items():
                new_fields[fieldname] = update_fks(
                    curr_type=fieldtype, original_type=original_type
                )

            self.result = sdt.Union(
                fields=new_fields,
                name=name if name is not None else "Union",
                properties=properties,
            )

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.result = sdt.Optional(
                type=update_fks(curr_type=type, original_type=original_type),
                name=name if name is not None else "Optional",
                properties=properties,
            )

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.result = sdt.List(
                type=update_fks(curr_type=type, original_type=original_type),
                max_size=max_size,
                name=name if name is not None else "Optional",
                properties=properties,
            )

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.result = sdt.Array(
                type=update_fks(curr_type=type, original_type=original_type),
                shape=shape,
                name=name if name is not None else "Optional",
                properties=properties,
            )

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if reference is not None:
                try:
                    original_type.get(path(paths=[reference]))
                except KeyError:
                    self.result = sdt.Id(unique=unique, base=base)

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

    visitor = Select()
    curr_type.accept(visitor)
    return visitor.result
