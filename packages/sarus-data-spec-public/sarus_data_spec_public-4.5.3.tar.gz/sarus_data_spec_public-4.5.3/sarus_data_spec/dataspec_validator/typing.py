from __future__ import annotations

from enum import Enum
from typing import Collection, List, Optional, Protocol
import logging

from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class DataspecPrivacyPolicy(Enum):
    WHITE_LISTED = "Whitelisted"
    DP = "Differentially-private evaluation"
    SYNTHETIC = "Evaluated from synthetic data only"
    PUBLIC = "Public"


class PUPKind(Enum):
    NOT_PUP = 0
    PUP = 1
    TOKEN_PRESERVING = 2
    ROW = 3


class DataspecValidator(Protocol):
    def storage(self) -> Storage: ...

    def verifies(
        self,
        variant_constraint: st.VariantConstraint,
        kind: st.ConstraintKind,
        public_context: Collection[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[bool]:
        """Check if the constraint attached to a Dataspec meets requirements.

        This function is useful because comparisons are not straightforwards.
        For instance, a Dataspec might have the variant constraint SYNTHETIC
        attached to it. This synthetic dataspec also verifies the DP constraint
        and the PUBLIC constraint.

        Args:
            variant_constraint: VariantConstraint attached to the Dataspec
            kind: constraint kind to verify compliance with
            public_context: actual current public context
            epsilon: current privacy consumed
        """
        ...

    def verified_constraints(
        self, dataspec: st.DataSpec
    ) -> List[st.VariantConstraint]:
        """Return the list of VariantConstraints attached to a DataSpec.

        A VariantConstraint attached to a DataSpec means that the DataSpec
        verifies the constraint.
        """
        ...

    def pup_token(self, dataspec: st.DataSpec) -> Optional[str]:
        """Return a token if the dataspec is PUP, otherwise return None.

        DataSpec.pup_token() returns a PUP token if the dataset is PUP and None
        otherwise. The PUP token is stored in the properties of the
        VariantConstraint. It is a hash initialized with a value when the
        Dataset is protected.

        If a transform does not preserve the PUI then the token is set to None
        If a transform preserves the PUI assignment but changes the rows (e.g.
        sample, shuffle, filter,...) then the token's value is changed If a
        transform does not change the rows (e.g. selecting a column, adding a
        scalar,...) then the token is passed without change

        A Dataspec is PUP if its PUP token is not None. Two PUP Dataspecs are
        aligned (i.e. they have the same number of rows and all their rows have
        the same PUI) if their tokens are equal.
        """
        ...

    def is_public(self, dataspec: st.DataSpec) -> bool:
        """Return True if the dataspec is public.

        Some DataSpecs are intrinsically Public, this is the case if they are
        freely available externally, they can be tagged so and will never be
        considered otherwise.

        This function returns True in the following cases:
        - The dataspec is an ML model
        - The dataspec is transformed but all its inputs are public

        This functions creates a VariantConstraint on the DataSpec to cache the
        PUBLIC constraint.
        """
        ...

    def is_dp(self, dataspec: st.DataSpec) -> bool:
        """Return True if the dataspec is the result of a DP transform.

        This is a simple implementation. This function checks if the
        dataspec's transform has a privacy budget and a random seed as an
        argument.
        """
        ...

    def is_synthetic(self, dataspec: st.DataSpec) -> bool:
        """Return True if the dataspec is synthetic.

        This functions creates a VariantConstraint on the DataSpec to cache
        the SYNTHETIC constraint.
        """

    def private_queries(self, dataspec: st.DataSpec) -> List[st.PrivateQuery]:
        """Return the list of PrivateQueries used in a Dataspec's transform.

        It represents the privacy loss associated with the current computation.

        It can be used by Sarus when a user (Access object) reads a DP dataspec
        to update its accountant. Note that Private Query objects are generated
        with a random uuid so that even if they are submitted multiple times to
        an account, they are only accounted once (ask @cgastaud for more on
        accounting)."""
        ...

    def is_dp_writable(self, dataspec: st.DataSpec) -> bool: ...

    def is_pup_writable(self, dataspec: st.DataSpec) -> bool: ...

    def is_publishable(self, dataspec: st.DataSpec) -> bool: ...

    def is_published(self, dataspec: st.DataSpec) -> bool: ...

    def rewritten_pup_token(self, dataspec: st.DataSpec) -> Optional[str]:
        """Returns the PUP token for the DP variant of this dataspec
        during DP rewriting.

        Currently, the implementation assumes a single DP/PUP variant per
        dataspec, resulting in one possible value for
        "rewritten_pup_token."
        Future changes could introduce multiple variants, necessitating
        the implementation of priority rules.
        """
        ...

    def is_big_data_computable(self, dataspec: st.DataSpec) -> bool: ...
