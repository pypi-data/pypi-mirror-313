from __future__ import annotations

import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.schema import to_arrow
from sarus_data_spec.base import Referring
from sarus_data_spec.constants import DATA, DATASET_SLUGNAME, PUBLIC
from sarus_data_spec.path import Path, path
from sarus_data_spec.type import Type
import sarus_data_spec.dataset as sd
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Schema(Referring[sp.Schema]):
    """A python class to describe schemas"""

    def __init__(self, protobuf: sp.Schema, store: bool = True) -> None:
        self._referred = {
            protobuf.dataset
        }  # This has to be defined before it is initialized
        super().__init__(protobuf, store=store)
        self._type = Type(self._protobuf.type)

    def prototype(self) -> t.Type[sp.Schema]:
        """Return the type of the underlying protobuf."""
        return sp.Schema

    def name(self) -> str:
        return self._protobuf.name

    def dataset(self) -> sd.Dataset:
        return t.cast(
            sd.Dataset, self.storage().referrable(self._protobuf.dataset)
        )

    def to_arrow(self) -> pa.Schema:
        return to_arrow(self.protobuf())

    def type(self) -> Type:
        """Returns the first type level of the schema"""
        return self._type

    def data_type(self) -> Type:
        """Returns the first type level containing the data,
        hence skips the privacy_unit struct if there is one"""
        return self.type().data_type()

    def has_admin_columns(self) -> bool:
        return self.type().has_admin_columns()

    def is_privacy_unit_tracking(self) -> bool:
        return self.type().has_privacy_unit_tracking()

    def privacy_unit_tracking_paths(self) -> Path:
        """Returns the path to the privacy unit"""
        return Path(self.protobuf().privacy_unit)

    # TODO: Add to_parquet, to_tensorflow, to_sql... here?
    # The Schema has a manager, it would provide the implementation

    def tables(self) -> t.List[st.Path]:
        struct_paths = self.data_type().structs()
        if struct_paths is None:  # there is no struct
            return []
        if len(struct_paths) == 0:  # struct is the first level
            return [path(label=DATA)]
        return [
            path(label=DATA, paths=[t.cast(Path, element)])
            for element in struct_paths
        ]

    def private_tables(self) -> t.List[st.Path]:
        return [
            table
            for table in self.tables()
            if self.data_type().sub_types(table)[0].properties()[PUBLIC]
            != str(True)
        ]

    def public_tables(self) -> t.List[st.Path]:
        return [
            table
            for table in self.tables()
            if self.data_type().sub_types(table)[0].properties()[PUBLIC]
            == str(True)
        ]


# Builder
def schema(
    dataset: st.Dataset,
    fields: t.Optional[t.Mapping[str, st.Type]] = None,
    schema_type: t.Optional[st.Type] = None,
    privacy_unit_tracking_paths: t.Optional[sp.Path] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
    name: t.Optional[str] = None,
) -> Schema:
    """A builder to ease the construction of a schema"""
    if name is None:
        name = dataset.properties().get(
            DATASET_SLUGNAME, f"{dataset.name()}_schema"
        )
    assert name is not None

    if fields is not None:
        return Schema(
            sp.Schema(
                dataset=dataset.uuid(),
                name=name,
                type=sp.Type(
                    struct=sp.Type.Struct(
                        fields=[
                            sp.Type.Struct.Field(
                                name=name, type=type.protobuf()
                            )
                            for name, type in fields.items()
                        ]
                    )
                ),
                privacy_unit=privacy_unit_tracking_paths,
                properties=properties,
            )
        )
    if schema_type is not None:
        return Schema(
            sp.Schema(
                dataset=dataset.uuid(),
                name=name,
                type=schema_type.protobuf(),
                privacy_unit=privacy_unit_tracking_paths,
                properties=properties,
            )
        )
    # If none of fields or type is defined, set type to Null
    return Schema(
        sp.Schema(
            dataset=dataset.uuid(),
            name=name,
            type=sp.Type(name="Null", null=sp.Type.Null()),
            privacy_unit=privacy_unit_tracking_paths,
            properties=properties,
        )
    )


if t.TYPE_CHECKING:
    test_schema: st.Schema = schema(sd.sql(uri="sqlite:///:memory:"))
