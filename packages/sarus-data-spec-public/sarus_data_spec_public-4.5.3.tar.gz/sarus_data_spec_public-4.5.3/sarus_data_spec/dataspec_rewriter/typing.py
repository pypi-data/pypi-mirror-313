from __future__ import annotations

from typing import Collection, Optional, Protocol
import logging

from sarus_data_spec.dataspec_validator.typing import DataspecValidator
from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class DataspecRewriter(Protocol):
    def storage(self) -> Storage: ...

    def dataspec_validator(self) -> DataspecValidator: ...

    def variant(
        self,
        dataspec: st.DataSpec,
        kind: st.ConstraintKind,
        public_context: Collection[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[st.DataSpec]: ...

    def variants(self, dataspec: st.DataSpec) -> Collection[st.DataSpec]:
        """Return all variants attached to a Dataspec."""
        ...
