from __future__ import annotations

from typing import Dict, Optional, Type

from sarus_data_spec.base import Referring
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Attribute(Referring[sp.Attribute]):
    """A python class to describe attributes"""

    def __init__(self, protobuf: sp.Attribute, store: bool = True) -> None:
        self._referred = {protobuf.object}
        # This has to be defined before it is initialized
        super().__init__(protobuf=protobuf, store=store)

    def prototype(self) -> Type[sp.Attribute]:
        """Return the type of the underlying protobuf."""
        return sp.Attribute

    def name(self) -> str:
        return self.protobuf().name


def attach_properties(
    dataspec: st.DataSpec,
    name: str = "",
    properties: Optional[Dict[str, str]] = None,
) -> Attribute:
    if properties is None:
        properties = {}
    return Attribute(
        sp.Attribute(object=dataspec.uuid(), properties=properties, name=name)
    )
