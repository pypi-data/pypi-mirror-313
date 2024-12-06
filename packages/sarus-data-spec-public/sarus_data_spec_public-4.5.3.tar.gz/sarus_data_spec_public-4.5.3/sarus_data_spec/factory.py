from typing import Callable, MutableMapping, TypeVar, Union, cast
import inspect

from sarus_data_spec.protobuf import type_name
from sarus_data_spec.protobuf.typing import Protobuf
import sarus_data_spec.typing as st

ReferrableBuilder = Callable[[Protobuf, bool], st.HasProtobuf]
BaseBuilder = Callable[[Protobuf], st.HasProtobuf]

Builder = Union[ReferrableBuilder, BaseBuilder]


class Factory(st.Factory):
    """Can produce objects from protobuf messages"""

    def __init__(self) -> None:
        self.type_name_create: MutableMapping[str, Builder] = {}

    def register(self, name: str, create: Builder) -> None:
        self.type_name_create[name] = create

    M = TypeVar("M", bound=Protobuf)

    def create(self, message: M, store: bool = True) -> st.HasProtobuf[M]:
        """Instantiate a wrapping class from a protobuf message.

        Factory functions (builders) may optionally take a `store` parameter.
        We check dynamically if the registered builder accepts the `store`
        parameter and pass it the `store` parameter accordingly.
        """
        builder = self.type_name_create[type_name(message)]
        args = list(inspect.signature(builder).parameters.keys())
        if len(args) == 2 and "store" in args:
            referrable_builder = cast(ReferrableBuilder, builder)
            return referrable_builder(message, store)
        elif len(args) == 1:
            base_builder = cast(BaseBuilder, builder)
            return base_builder(message)
        else:
            raise ValueError(f"Unknown factory function signature {args}")
