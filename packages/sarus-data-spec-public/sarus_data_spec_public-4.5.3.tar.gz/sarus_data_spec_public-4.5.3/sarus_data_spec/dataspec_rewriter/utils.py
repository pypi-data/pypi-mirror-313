from typing import Collection, List, Optional, Set, Union
import logging
import typing as t

try:
    from sarus_differential_privacy.query import PrivateQuery
except ModuleNotFoundError as e_groupby_dp:
    if "sarus_differential_privacy" not in str(e_groupby_dp):
        raise
    PrivateQuery = t.Any  # type: ignore

from sarus_data_spec.dataspec_validator.typing import DataspecValidator
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


def find_dataspec_from_constraint(
    dataspec_validator: DataspecValidator,
    dataspec: st.DataSpec,
    kind: st.ConstraintKind,
    public_context: Collection[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> Optional[st.DataSpec]:
    # Current dataspec verifies the constraint?
    for constraint in dataspec_validator.verified_constraints(dataspec):
        if dataspec_validator.verifies(
            variant_constraint=constraint,
            kind=kind,
            public_context=public_context,
            privacy_limit=privacy_limit,
        ):
            return dataspec

    # Current dataspec has a variant that verifies the constraint?
    for variant in dataspec.variants():
        for constraint in dataspec_validator.verified_constraints(variant):
            if dataspec_validator.verifies(
                variant_constraint=constraint,
                kind=kind,
                public_context=public_context,
                privacy_limit=privacy_limit,
            ):
                return variant

    return None


def graph_private_queries(dataspec: st.DataSpec) -> List[PrivateQuery]:
    """Return all the private queries from a dataspec to the sources."""

    class PrivateQueriesVisitor(st.Visitor, st.TransformVisitor):
        visited: Set[Union[st.DataSpec, st.Transform]] = set()
        private_queries: List[PrivateQuery] = list()

        def all(self, visited: Union[st.DataSpec, st.Transform]) -> None:
            pass

        def transformed(
            self,
            visited: st.DataSpec,
            transform: st.Transform,
            *arguments: st.DataSpec,
            **named_arguments: st.DataSpec,
        ) -> None:
            if visited not in self.visited:
                self.private_queries.extend(visited.private_queries())

                for argument in arguments:
                    argument.accept(self)
                for _, argument in named_arguments.items():
                    argument.accept(self)
                self.visited.add(visited)

        def other(self, visited: Union[st.DataSpec, st.Transform]) -> None:
            if visited not in self.visited:
                self.visited.add(visited)

        def composed(
            self,
            visited: st.Transform,
            transform: st.Transform,
            *arguments: st.Transform,
            **named_arguments: st.Transform,
        ) -> None:
            for argument in arguments:
                argument.accept(self)
            for _, argument in named_arguments.items():
                argument.accept(self)

        def variable(
            self,
            visited: st.Transform,
            name: str,
            position: int,
        ) -> None:
            pass

    visitor = PrivateQueriesVisitor()
    dataspec.accept(visitor)
    private_queries = visitor.private_queries
    return private_queries
