from types import TracebackType
import typing as t

from sarus_data_spec.context.state import (
    pop_global_context,
    push_global_context,
)
from sarus_data_spec.context.typing import Context
from sarus_data_spec.manager.typing import Manager
from sarus_data_spec.scalar import random_seed
from sarus_data_spec.storage.typing import Storage
from sarus_data_spec.transform import derive_seed
import sarus_data_spec.typing as st


class Public(Context):
    """A public context base"""

    def __init__(self, seed: int = 1234) -> None:
        self.master_seed = seed

    def generate_seed(self, salt: int = 0) -> st.Scalar:
        """Generate a new seed from the master seed."""
        return t.cast(
            st.Scalar, derive_seed(salt)(random_seed(self.master_seed))
        )

    def factory(self) -> st.Factory:
        raise NotImplementedError

    def storage(self) -> Storage:
        raise NotImplementedError()

    def manager(self) -> Manager:
        raise NotImplementedError()

    def __enter__(self) -> Context:
        push_global_context(self)
        return self

    def __exit__(
        self,
        type: t.Optional[t.Type[BaseException]],
        value: t.Optional[BaseException],
        traceback: t.Optional[TracebackType],
    ) -> None:
        pop_global_context()
        return None
