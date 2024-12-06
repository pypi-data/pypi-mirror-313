from __future__ import annotations

from typing import Collection, List, Optional, cast
import json
import logging

from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.constants import (
    IS_VALID,
    NO_TOKEN,
    PRIVATE_QUERY,
    PUBLIC,
    PUP_TOKEN,
    IS_DP,
    IS_PUBLIC,
    IS_SYNTHETIC,
    IS_BIG_DATA_COMPUTABLE,
)
from sarus_data_spec.dataspec_validator.privacy_limit import DeltaEpsilonLimit
from sarus_data_spec.manager.async_utils import sync
from sarus_data_spec.manager.ops.processor import routing
from sarus_data_spec.manager.ops.processor.external.external_op import (
    external_implementation,
)
from sarus_data_spec.protobuf.utilities import dejson
from sarus_data_spec.protobuf.utilities import json as proto_to_json
from sarus_data_spec.storage.typing import Storage
from sarus_data_spec.transform import handle_big_data
from sarus_data_spec.variant_constraint import (
    public_constraint,
    pup_constraint,
    syn_constraint,
)
import sarus_data_spec.dataspec_validator.simple_rules as verification_rules
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.dataspec_validator.caching_utils import (
    check_existence_in_attribute_or_cache_after,
)

try:
    from sarus_differential_privacy.protobuf.private_query_pb2 import (
        PrivateQuery as ProtoPrivateQuery,
    )
    from sarus_differential_privacy.query import BasePrivateQuery

except ImportError:
    # Warning raised in typing.py
    pass

logger = logging.getLogger(__name__)


class BaseDataspecValidator:
    def __init__(self, storage: Storage):
        self._storage = storage

    def storage(self) -> Storage:
        return self._storage

    def verified_constraints(
        self, dataspec: st.DataSpec
    ) -> List[st.VariantConstraint]:
        """Return the list of VariantConstraints attached to a DataSpec.

        A VariantConstraint attached to a DataSpec means that the DataSpec
        verifies the constraint.
        """
        constraints = self.storage().referring(
            dataspec, type_name=sp.type_name(sp.VariantConstraint)
        )
        return cast(List[st.VariantConstraint], list(constraints))

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
        return verification_rules.verifies(
            variant_constraint=variant_constraint,
            kind=kind,
            public_context=public_context,
            privacy_limit=privacy_limit,
        )

    @check_existence_in_attribute_or_cache_after(attribute_name=IS_DP)
    def is_dp(self, dataspec: st.DataSpec) -> bool:
        """Return True if the dataspec is the result of a DP transform.

        This is a simple implementation. This function checks if the
        dataspec's transform has a privacy budget and a random seed as an
        argument.
        """
        if not dataspec.is_transformed():
            return False
        parents, kwparents = dataspec.parents()
        parents = list(parents) + list(kwparents.values())
        scalars = [
            cast(st.Scalar, parent)
            for parent in parents
            if parent.prototype() == sp.Scalar
        ]
        has_budget = (
            len([scalar for scalar in scalars if scalar.is_privacy_params()])
            == 1
        )
        has_seed = (
            len([scalar for scalar in scalars if scalar.is_random_seed()]) == 1
        )
        return has_budget and has_seed

    @check_existence_in_attribute_or_cache_after(attribute_name=IS_SYNTHETIC)
    def is_synthetic(self, dataspec: st.DataSpec) -> bool:
        """Return True if the dataspec is synthetic.

        This functions creates a VariantConstraint on the DataSpec to cache
        the SYNTHETIC constraint.
        """
        # TODO fetch real context and epsilon
        public_context: Collection[str] = []
        privacy_limit = None
        kind = st.ConstraintKind.SYNTHETIC

        self.is_public(dataspec)

        for constraint in self.verified_constraints(dataspec):
            check_constraint = self.verifies(
                constraint, kind, public_context, privacy_limit
            )
            if check_constraint is not None:
                return check_constraint

        # Determine is the Dataspec is synthetic
        if dataspec.is_transformed():
            transform = dataspec.transform()
            if transform.protobuf().spec.HasField("synthetic"):
                is_synthetic = True
            else:
                # Returns true if the DataSpec derives only from synthetic
                args_parents, kwargs_parents = dataspec.parents()
                is_synthetic = all(
                    [
                        self.is_synthetic(ds)
                        for ds in args_parents
                        if isinstance(ds, st.DataSpec)
                    ]
                    + [
                        self.is_synthetic(ds)
                        for ds in kwargs_parents.values()
                        if isinstance(ds, st.DataSpec)
                    ]
                )
        else:
            is_synthetic = False

        # save variant constraint
        syn_constraint(dataspec, is_synthetic=is_synthetic)

        return is_synthetic

    @check_existence_in_attribute_or_cache_after(attribute_name=IS_PUBLIC)
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
        # TODO fetch real context and epsilon
        public_context: Collection[str] = []
        privacy_limit = DeltaEpsilonLimit({0.0: 0.0})
        kind = st.ConstraintKind.PUBLIC

        for constraint in self.verified_constraints(dataspec):
            check_constraint = self.verifies(
                constraint, kind, public_context, privacy_limit
            )
            if check_constraint is not None:
                return check_constraint

        # Determine is the Dataspec is public
        if dataspec.is_transformed():
            # Returns true if the DataSpec derives only from public
            if (
                dataspec.transform().is_external()
                or dataspec.prototype() == sp.Scalar
            ):
                args_parents, kwargs_parents = dataspec.parents()
                is_public = all(
                    [
                        self.is_public(ds)
                        for ds in args_parents
                        if isinstance(ds, st.DataSpec)
                    ]
                    + [
                        self.is_public(ds)
                        for ds in kwargs_parents.values()
                        if isinstance(ds, st.DataSpec)
                    ]
                )
            else:
                assert dataspec.prototype() == sp.Dataset
                # For a standard transform, all tables must be
                # public in the schema to have a public dataset
                dataset = cast(st.Dataset, dataspec)
                schema = dataset.schema()
                is_public = schema.data_type().properties()[PUBLIC] == str(
                    True
                )

        elif dataspec.prototype() == sp.Scalar:
            scalar = cast(st.Scalar, dataspec)
            assert (
                scalar.is_random_seed()
                or scalar.is_privacy_params()
                or scalar.is_synthetic_model()
                or scalar.is_pretrained_model()
            )
            is_public = True
        else:
            is_public = False

        # save variant constraint
        public_constraint(dataspec, is_public)

        return is_public

    def pup_token(self, dataspec: st.DataSpec) -> Optional[str]:
        """Return a token if the dataspec is PUP, otherwise return None.

        DataSpec.pup_token() returns a PUP token if the dataset is PUP and None
        otherwise. The PUP token is stored in the properties of the
        VariantConstraint. It is a hash initialized with a value when the
        Dataset is protected.

        If a transform does not preserve the PEID then the token is set to None
        If a transform preserves the PEID assignment but changes the rows (e.g.
        sample, shuffle, filter,...) then the token's value is changed If a
        transform does not change the rows (e.g. selecting a column, adding a
        scalar,...) then the token is passed without change

        A Dataspec is PUP if its PUP token is not None. Two PUP Dataspecs are
        aligned (i.e. they have the same number of rows and all their rows have
        the same PEID) if their tokens are equal.
        """
        if dataspec.prototype() == sp.Scalar:
            return None

        dataset = cast(st.Dataset, dataspec)

        # TODO fetch real context and budget
        public_context: Collection[str] = []
        privacy_limit = DeltaEpsilonLimit({0.0: 0.0})
        kind = st.ConstraintKind.PUP

        for constraint in self.verified_constraints(dataspec):
            check_constraint = self.verifies(
                constraint, kind, public_context, privacy_limit
            )
            if check_constraint is not None:
                if check_constraint:
                    return constraint.properties()[PUP_TOKEN]
                else:
                    return None

        # Compute the PUP token
        if not dataset.is_transformed():
            return None

        transform = dataset.transform()
        _, StaticChecker = routing.get_dataset_op(transform)
        pup_token = StaticChecker(dataset).pup_token(public_context)
        if pup_token is None:
            pup_token = NO_TOKEN

        pup_constraint(
            dataspec=dataset,
            token=pup_token,
            required_context=[],
            privacy_limit=privacy_limit,
        )

        return None if pup_token == NO_TOKEN else pup_token

    def private_queries(self, dataspec: st.DataSpec) -> List[st.PrivateQuery]:
        """Return the list of PrivateQueries used in a Dataspec's transform.

        It represents the privacy loss associated with the current computation.

        It can be used by Sarus when a user (Access object) reads a DP dataspec
        to update its accountant. Note that Private Query objects are generated
        with a random uuid so that even if they are submitted multiple times to
        an account, they are only accounted once (ask @cgastaud for more on
        accounting).
        """
        attribute = dataspec.attribute(name=PRIVATE_QUERY)
        # Already computed
        if attribute is not None:
            private_query_str = attribute[PRIVATE_QUERY]
            protos = [
                cast(ProtoPrivateQuery, dejson(q))
                for q in json.loads(private_query_str)
            ]
            return cast(
                List[st.PrivateQuery],
                BasePrivateQuery.from_protobuf(protos),
            )

        # Compute private queries
        if not dataspec.is_transformed():
            private_queries = []
        else:
            if dataspec.prototype() == sp.Dataset:
                dataset = cast(st.Dataset, dataspec)
                private_queries = sync(
                    routing.TransformedDataset(dataset).private_queries()
                )
            else:
                scalar = cast(st.Scalar, dataspec)
                private_queries = sync(
                    routing.TransformedScalar(scalar).private_queries()
                )

        # Cache in an attribute
        subqueries = [
            proto_to_json(query.protobuf()) for query in private_queries
        ]
        attach_properties(
            dataspec,
            properties={PRIVATE_QUERY: json.dumps(subqueries)},
            name=PRIVATE_QUERY,
        )

        return private_queries

    def has_valid_transform(self, dataspec: st.DataSpec) -> bool:
        """Check that the transform of a dataspec is valid with the input
        parameters.
        """
        if not dataspec.is_transformed():
            return True

        transform = dataspec.transform()
        # TODO: remove condition is_external when standard
        # transforms has signature
        if transform.is_external():
            implementation = external_implementation(transform)
            try:
                bound_signature = implementation.signature().bind_dataspec(
                    dataspec
                )
                bound_signature.static_validation()
                return True
            except (ValueError, TypeError):
                return False
        else:
            return True

    @check_existence_in_attribute_or_cache_after(IS_VALID)
    def is_valid(self, dataspec: st.DataSpec) -> bool:
        """
        Check that the dataspec is validating certain conditions: valid
        transforms, valid parents, valid sources.

        This function creates an attributes on the DataSpec to cache the
        validity of the dataspecs.
        The source dataspec are validated during the onboarding process.
        """
        if not dataspec.is_transformed():
            if dataspec.is_public():
                is_valid = True
            else:
                is_valid = False
        else:
            # Valid transform
            if self.has_valid_transform(dataspec):
                # Valid parents:
                parents, kwparents = dataspec.parents()
                parents = list(parents) + list(kwparents.values())
                is_valid = all(
                    self.is_valid(parent)
                    for parent in parents
                    if isinstance(parent, st.DataSpec)
                )
            else:
                is_valid = False

        # Only one non-public source max.
        sources_ds = dataspec.sources(sp.type_name(sp.Dataset))
        admin_sources = [
            source for source in sources_ds if not source.is_public()
        ]
        if len(admin_sources) > 1:
            is_valid = False
        return is_valid

    def is_dp_writable(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def is_pup_writable(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def is_publishable(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def is_published(self, dataspec: st.DataSpec) -> bool:
        raise NotImplementedError

    def rewritten_pup_token(self, dataspec: st.DataSpec) -> Optional[str]:
        raise NotImplementedError

    @check_existence_in_attribute_or_cache_after(IS_BIG_DATA_COMPUTABLE)
    def is_big_data_computable(self, dataspec: st.DataSpec) -> bool:
        """
        Check if the dataspec can be computed if the source is bigdata.
        Certain transformations are designed to handle big data datasets,
        meaning that the transformation can be converted into an SQL
        query executable by an SQL engine. Some transformations do not
        support big data and, as such, require computation in Python,
        potentially leading to out-of-memory errors.
        """
        manager = dataspec.manager()

        if not dataspec.is_transformed():
            return True

        sources = dataspec.sources(sp.type_name(sp.Dataset))
        if len(sources) == 0:
            return True

        source_ds = sources.pop()
        if not manager.is_big_data(source_ds):
            return True

        # TODO: to remove when it actually works without this
        if dataspec.is_transformed() and dataspec.transform().name() in [
            "budget_assignment",
            "attributes_budget",
            "Protect",
            "automatic_budget",
        ]:
            return True

        parents = dataspec.parents_list()
        if not handle_big_data(dataspec.transform()):
            if any(
                [
                    manager.is_big_data(dataspec_parent)
                    for dataspec_parent in parents
                ]
            ):
                return False
        return all(
            [
                self.is_big_data_computable(dataspec_parent)
                for dataspec_parent in parents
            ]
        )
