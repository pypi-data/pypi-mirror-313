from typing import Collection, List, Optional, Tuple, cast
import logging

from sarus_data_spec.constants import (
    IS_PUBLIC,
    IS_SYNTHETIC,
    NO_TOKEN,
    PUP_TOKEN,
)
import sarus_data_spec.typing as st

ArgStruct = Tuple[List[int], List[str]]
logger = logging.getLogger(__name__)


def verifies(
    variant_constraint: st.VariantConstraint,
    kind: st.ConstraintKind,
    public_context: Collection[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> Optional[bool]:
    if kind == st.ConstraintKind.PUBLIC:
        return verifies_public(variant_constraint=variant_constraint)

    elif kind == st.ConstraintKind.SYNTHETIC:
        return verifies_synthetic(variant_constraint=variant_constraint)

    elif kind == st.ConstraintKind.MOCK:
        return verifies_mock(variant_constraint=variant_constraint)

    elif kind == st.ConstraintKind.DP:
        return verifies_dp(
            variant_constraint=variant_constraint,
            privacy_limit=privacy_limit,
        )
    elif kind == st.ConstraintKind.PUP:
        return verifies_pup(variant_constraint=variant_constraint)
    else:  # kind == st.ConstraintKind.PUP_FOR_REWRITING:
        return verifies_pup_for_rewriting(
            variant_constraint=variant_constraint
        )


def verifies_public(
    variant_constraint: st.VariantConstraint,
) -> Optional[bool]:
    kind = variant_constraint.constraint_kind()
    if kind == st.ConstraintKind.PUBLIC:
        return variant_constraint.properties()[IS_PUBLIC] == str(True)
    else:
        return None


def verifies_synthetic(
    variant_constraint: st.VariantConstraint,
) -> Optional[bool]:
    kind = variant_constraint.constraint_kind()
    if kind == st.ConstraintKind.SYNTHETIC:
        return variant_constraint.properties()[IS_SYNTHETIC] == str(True)
    elif kind == st.ConstraintKind.PUBLIC:
        if variant_constraint.properties()[IS_PUBLIC] == str(True):
            return True
        else:
            return None
    else:
        return None


def verifies_mock(variant_constraint: st.VariantConstraint) -> Optional[bool]:
    kind = variant_constraint.constraint_kind()
    if kind == st.ConstraintKind.MOCK:
        return True
    else:
        return None


def verifies_pup(
    variant_constraint: st.VariantConstraint,
) -> Optional[bool]:
    """If we attached a PUP constraint to a dataspec then it is PUP.

    NB: for now we don't check the context nor the privacy limit
    """
    kind = variant_constraint.constraint_kind()
    if kind == st.ConstraintKind.PUP:
        stored_token = variant_constraint.properties()[PUP_TOKEN]
        return False if stored_token == NO_TOKEN else True
    else:
        return None


def verifies_pup_for_rewriting(
    variant_constraint: st.VariantConstraint,
) -> Optional[bool]:
    kind = variant_constraint.constraint_kind()
    if kind == st.ConstraintKind.PUP_FOR_REWRITING:
        stored_token = variant_constraint.properties()[PUP_TOKEN]
        return False if stored_token == NO_TOKEN else True
    else:
        return None


def verifies_dp(
    variant_constraint: st.VariantConstraint,
    privacy_limit: Optional[st.PrivacyLimit],
) -> Optional[bool]:
    """Check if a variant constraint satisfies a DP profile.

    For now, return True only for strict equality.
    """
    if privacy_limit is None:
        raise ValueError(
            "Input privacy limit required when checking against DP."
        )

    kind = variant_constraint.constraint_kind()
    if kind != st.ConstraintKind.DP:
        return None

    constraint_privacy_limit = variant_constraint.privacy_limit()
    if constraint_privacy_limit is None:
        raise ValueError(
            "Found a DP constraint without a privacy limit "
            "when checking against DP."
        )
    return cast(
        bool,
        privacy_limit.delta_epsilon_dict()
        == constraint_privacy_limit.delta_epsilon_dict(),
    )
