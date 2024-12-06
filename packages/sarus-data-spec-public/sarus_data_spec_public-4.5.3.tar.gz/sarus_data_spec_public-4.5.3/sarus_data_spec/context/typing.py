from typing import Protocol, runtime_checkable

from sarus_data_spec.manager.typing import Manager
from sarus_data_spec.storage.typing import Storage
from sarus_data_spec.typing import Factory
import sarus_data_spec.typing as st


@runtime_checkable
class Context(Protocol):
    """Provide the shared services."""

    def factory(self) -> Factory:
        """Provide a factory to create python objects from their protobuf
        counterparts."""
        ...

    def storage(self) -> Storage:
        """Provide the storage device for object persistence."""
        ...

    def manager(self) -> Manager:
        """Provide the manager to implement object behaviors."""
        ...

    def generate_seed(self, salt: int = 0) -> st.Scalar:
        """Generate a new seed from the master seed."""
        ...


@runtime_checkable
class HasContext(Protocol):
    """Has a context."""

    def context(self) -> Context:
        """Return a context (usually a singleton)."""
        ...
