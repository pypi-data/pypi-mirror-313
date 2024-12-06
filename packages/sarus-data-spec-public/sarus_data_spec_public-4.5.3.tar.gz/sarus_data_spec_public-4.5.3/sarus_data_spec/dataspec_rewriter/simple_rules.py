from time import time_ns
from typing import Collection, Dict, List, Optional, Tuple, Union, cast
import logging

from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.constants import VARIANT_UUID
from sarus_data_spec.context import global_context
from sarus_data_spec.dataset import transformed
from sarus_data_spec.dataspec_validator.typing import DataspecValidator
from sarus_data_spec.manager.ops.processor import routing
from sarus_data_spec.scalar import privacy_budget
from sarus_data_spec.variant_constraint import (
    dp_constraint,
    mock_constraint,
    syn_constraint,
)
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


def attach_variant(
    original: st.DataSpec,
    variant: st.DataSpec,
    kind: st.ConstraintKind,
) -> None:
    attach_properties(
        original,
        properties={
            # TODO deprecated in SDS >= 2.0.0 -> use only VARIANT_UUID
            kind.name: variant.uuid(),
            VARIANT_UUID: variant.uuid(),
        },
        name=kind.name,
    )


def rewrite(
    dataspec_validator: DataspecValidator,
    dataspec: st.DataSpec,
    kind: st.ConstraintKind,
    public_context: Collection[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> Optional[st.DataSpec]:
    """Returns a compliant Node or None."""

    if kind == st.ConstraintKind.SYNTHETIC:
        variant, _ = rewrite_synthetic(
            dataspec_validator,
            dataspec,
            public_context,
        )
        return variant

    elif kind == st.ConstraintKind.MOCK:
        mock_variant, _ = rewrite_mock(
            dataspec_validator,
            dataspec,
            public_context,
        )
        return mock_variant

    if privacy_limit is None:
        raise ValueError(
            "Privacy limit must be defined for PUP or DP rewriting"
        )

    if kind == st.ConstraintKind.DP:
        variant, _ = rewrite_dp(
            dataspec_validator,
            dataspec,
            public_context=public_context,
            privacy_limit=privacy_limit,
        )
        return variant

    elif kind == st.ConstraintKind.PUP:
        raise NotImplementedError("PUP rewriting")

    else:
        raise ValueError(
            f"Privacy policy {kind} rewriting not implemented yet"
        )


def rewrite_synthetic(
    dataspec_validator: DataspecValidator,
    dataspec: st.DataSpec,
    public_context: Collection[str],
) -> Tuple[st.DataSpec, Collection[str]]:
    # Current dataspec verifies the constraint?
    for constraint in dataspec_validator.verified_constraints(dataspec):
        if dataspec_validator.verifies(
            constraint,
            st.ConstraintKind.SYNTHETIC,
            public_context,
            privacy_limit=None,
        ):
            return dataspec, public_context

    # Current dataspec has a variant that verifies the constraint?
    for variant in dataspec.variants():
        if variant is None:
            logger.info(f"Found a None variant for dataspec {dataspec.uuid()}")
            continue
        for constraint in dataspec_validator.verified_constraints(variant):
            if dataspec_validator.verifies(
                constraint,
                st.ConstraintKind.SYNTHETIC,
                public_context,
                privacy_limit=None,
            ):
                return variant, public_context

    # Derive the SD from the parents SD
    if dataspec.is_transformed():
        transform = dataspec.transform()
        args, kwargs = dataspec.parents()

        syn_args: List[Union[st.DataSpec, st.Transform]] = [
            rewrite_synthetic(dataspec_validator, arg, public_context)[0]
            if isinstance(arg, st.DataSpec)
            else arg
            for arg in args
        ]
        syn_kwargs: Dict[str, Union[st.DataSpec, st.Transform]] = {
            name: rewrite_synthetic(dataspec_validator, arg, public_context)[0]
            if isinstance(arg, st.DataSpec)
            else arg
            for name, arg in kwargs.items()
        }

        syn_variant = cast(
            st.DataSpec,
            transformed(
                transform,
                *syn_args,
                dataspec_type=sp.type_name(dataspec.prototype()),
                dataspec_name=None,
                **syn_kwargs,
            ),
        )
        syn_constraint(
            dataspec=syn_variant, required_context=list(public_context)
        )
        attach_variant(dataspec, syn_variant, kind=st.ConstraintKind.SYNTHETIC)
        return syn_variant, public_context

    elif dataspec.is_public():
        return dataspec, public_context
    else:
        raise TypeError(
            "Non public source Datasets cannot"
            "be rewritten to Synthetic, a synthetic variant"
            "should have been created downstream in the graph."
        )


def rewrite_mock(
    dataspec_validator: DataspecValidator,
    dataspec: st.DataSpec,
    public_context: Collection[str],
) -> Tuple[Optional[st.DataSpec], Collection[str]]:
    """rewrite the MOCK variant of a DataSpec.

    Note that the MOCK rewriting only makes sense for internally transformed
    dataspecs. For externally transformed dataspecs, the MOCK is computed
    before the dataspec, so we can only fetch it.
    """
    for constraint in dataspec_validator.verified_constraints(dataspec):
        if dataspec_validator.verifies(
            constraint,
            st.ConstraintKind.MOCK,
            public_context,
            privacy_limit=None,
        ):
            return dataspec, public_context

    # Current dataspec has a variant that verifies the constraint?
    for variant in dataspec.variants():
        if variant is None:
            logger.info(f"Found a None variant for dataspec {dataspec.uuid()}")
            continue
        for constraint in dataspec_validator.verified_constraints(variant):
            if dataspec_validator.verifies(
                constraint,
                st.ConstraintKind.MOCK,
                public_context,
                privacy_limit=None,
            ):
                return variant, public_context

    if not dataspec.is_transformed():
        if not dataspec.is_public():
            raise ValueError(
                "Cannot rewrite the MOCK of a non public source DataSpec. "
                "A MOCK should be set manually downstream in the "
                "computation graph."
            )
        else:
            return dataspec, public_context

    # The DataSpec is the result of an internal transform
    transform = dataspec.transform()
    args, kwargs = dataspec.parents()
    mock_args = [
        arg.variant(st.ConstraintKind.MOCK)
        if isinstance(arg, st.DataSpec)
        else arg
        for arg in args
    ]
    named_mock_args = {
        name: arg.variant(st.ConstraintKind.MOCK)
        if isinstance(arg, st.DataSpec)
        else arg
        for name, arg in kwargs.items()
    }
    if any([m is None for m in mock_args]) or any(
        [m is None for m in named_mock_args.values()]
    ):
        raise ValueError(
            f"Cannot derive a mock for {dataspec} "
            "because of of the parent has a None MOCK."
        )

    typed_mock_args = [cast(st.DataSpec, ds) for ds in mock_args]
    typed_named_mock_args = {
        name: cast(st.DataSpec, ds) for name, ds in named_mock_args.items()
    }

    mock: st.DataSpec = transformed(
        transform,
        *typed_mock_args,
        dataspec_type=sp.type_name(dataspec.prototype()),
        dataspec_name=None,
        **typed_named_mock_args,
    )
    mock_constraint(mock)
    attach_variant(dataspec, mock, st.ConstraintKind.MOCK)

    return mock, public_context


def rewrite_dp(
    dataspec_validator: DataspecValidator,
    dataspec: st.DataSpec,
    public_context: Collection[str],
    privacy_limit: st.PrivacyLimit,
) -> Tuple[st.DataSpec, Collection[str]]:
    """Simple DP rewriting.

    Only check the dataspec's parents, do not go further up in the graph.
    """
    # Current dataspec verifies the constraint?
    for constraint in dataspec_validator.verified_constraints(dataspec):
        if dataspec_validator.verifies(
            variant_constraint=constraint,
            kind=st.ConstraintKind.DP,
            public_context=public_context,
            privacy_limit=privacy_limit,
        ):
            return dataspec, public_context

    # Current dataspec has a variant that verifies the constraint?
    for variant in dataspec.variants():
        for constraint in dataspec_validator.verified_constraints(variant):
            if dataspec_validator.verifies(
                variant_constraint=constraint,
                kind=st.ConstraintKind.DP,
                public_context=public_context,
                privacy_limit=privacy_limit,
            ):
                return variant, public_context

    if not dataspec.is_transformed():
        return rewrite_synthetic(dataspec_validator, dataspec, public_context)

    # Check that there is a positive epsilon
    delta_epsilon_dict = privacy_limit.delta_epsilon_dict()
    if len(delta_epsilon_dict) == 1:
        epsilon = list(delta_epsilon_dict.values()).pop()
        if epsilon == 0:
            return rewrite_synthetic(
                dataspec_validator, dataspec, public_context
            )

    transform = dataspec.transform()
    if dataspec.prototype() == sp.Dataset:
        dataset = cast(st.Dataset, dataspec)
        _, DatasetStaticChecker = routing.get_dataset_op(transform)
        is_dp_writable = DatasetStaticChecker(dataset).is_dp_writable(
            public_context
        )
        dp_transform = DatasetStaticChecker(dataset).dp_transform()
    else:
        scalar = cast(st.Scalar, dataspec)
        _, ScalarStaticChecker = routing.get_scalar_op(transform)
        is_dp_writable = ScalarStaticChecker(scalar).is_dp_writable(
            public_context
        )
        dp_transform = ScalarStaticChecker(scalar).dp_transform()

    if not is_dp_writable:
        return rewrite_synthetic(dataspec_validator, dataspec, public_context)

    # Create the DP variant
    assert dp_transform is not None
    budget = privacy_budget(privacy_limit)
    seed = global_context().generate_seed(salt=time_ns())

    args, kwargs = dataspec.parents()
    dp_variant = cast(
        st.DataSpec,
        transformed(
            dp_transform,
            *args,
            dataspec_type=sp.type_name(dataspec.prototype()),
            dataspec_name=None,
            budget=budget,
            seed=seed,
            **kwargs,
        ),
    )
    dp_constraint(
        dataspec=dp_variant,
        required_context=list(public_context),
        privacy_limit=privacy_limit,
    )
    attach_variant(
        original=dataspec,
        variant=dp_variant,
        kind=st.ConstraintKind.DP,
    )

    # We also attach the dataspec's synthetic variant to be the DP dataspec's
    # synthetic variant. This is to avoid to have DP computations in the MOCK.
    syn_variant = dataspec.variant(st.ConstraintKind.SYNTHETIC)
    if syn_variant is None:
        raise ValueError("Could not find a synthetic variant.")
    attach_variant(
        original=dp_variant,
        variant=syn_variant,
        kind=st.ConstraintKind.SYNTHETIC,
    )

    return dp_variant, public_context
