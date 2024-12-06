from __future__ import annotations

from typing import Collection, Optional, cast
import logging

from sarus_data_spec.constants import VARIANT_UUID
from sarus_data_spec.dataspec_validator.base import BaseDataspecValidator
from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.dataspec_rewriter.simple_rules as rewriting_rules
import sarus_data_spec.dataspec_validator.typing as sdvt
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class BaseDataspecRewriter:
    def __init__(self, storage: Storage):
        self._storage = storage
        self._dataspec_validator = BaseDataspecValidator(storage=storage)

    def dataspec_validator(self) -> sdvt.DataspecValidator:
        return self._dataspec_validator

    def storage(self) -> Storage:
        return self._storage

    def variant(
        self,
        dataspec: st.DataSpec,
        kind: st.ConstraintKind,
        public_context: Collection[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[st.DataSpec]:
        return rewriting_rules.rewrite(
            self.dataspec_validator(),
            dataspec,
            kind,
            public_context,
            privacy_limit,
        )

    def variants(self, dataspec: st.DataSpec) -> Collection[st.DataSpec]:
        """Return all variants attached to a Dataspec."""
        variants_attributes = {
            variant_kind: dataspec.attributes(name=variant_kind.name)
            for variant_kind in st.ConstraintKind
        }
        variants_dict = {
            variant_kind: [
                self.storage().referrable(att[VARIANT_UUID]) for att in atts
            ]
            for variant_kind, atts in variants_attributes.items()
        }
        # raise warning if some variants are not found in the storage
        for variant_kind, variants in variants_dict.items():
            if any([variant is None for variant in variants]):
                logger.warning(
                    "Found None "
                    f"variant {variant_kind.name} for dataspec {dataspec}"
                )
        variants = list(
            filter(lambda x: x is not None, sum(variants_dict.values(), []))
        )
        return cast(Collection[st.DataSpec], variants)
