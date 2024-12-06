from __future__ import annotations

import typing as t

from sarus_data_spec.dataspec_validator.signature import SarusBoundSignature
from sarus_data_spec.dataspec_validator.typing import PUPKind
import sarus_data_spec.typing as st

NO_TRANSFORM_ID = "no_transform_id"

try:
    from sarus_data_spec.sarus_query_builder.core.core import (
        OptimizableQueryBuilder,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus" not in str(e_pandas_dp):
        raise


@t.runtime_checkable
class ExternalOpImplementation(t.Protocol):
    """External Op implementation class.

    The `allowed_pup_args` is a list of combinations of arguments' names which
    are managed by the Op. The result of the Op will be PUP only if the set of
    PUP arguments passed to the Op are in this list.

    For instance, if we have an op that takes 3 arguments `a`, `b` and `c` and
    the `allowed_pup_args` are [{'a'}, {'b'}, {'a','b'}] then the following
    combinations will yield a PUP output:
        - `a` is a PUP dataspec, `b` and `c` are either not dataspecs or public
          dataspecs
        - `b` is a PUP dataspec, `a` and `c` are either not dataspecs or public
          dataspecs
        - `a` and `b` are PUP dataspecs, `c` is either not a dataspec or a
          public dataspec
    """

    def transform_id(self) -> str: ...

    def dp_equivalent_id(self) -> t.Optional[str]: ...

    def dp_equivalent(self) -> t.Optional[ExternalOpImplementation]: ...

    async def call(self, bound_signature: SarusBoundSignature) -> t.Any:
        """Compute the external op output value.

        DP implementation take additional arguments:
            - `seed` an integer used to parametrize rangom number generators
            - `budget` the privacy budget that can be spend in the op
            - `pe` the protected entity information of each row
        """

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """Return the PUP properties of the transform.

        It takes the transform arguments as input because it can depend on some
        transform parameters. For instance, it is not PUP if we are aggregating
        the rows (axis=0) and it is PUP if we are aggregating the columns
        (axis=1).
        """

    def is_dp(self, bound_signature: SarusBoundSignature) -> bool:
        """Return True if the DP transform is compatible with the arguments.

        It takes the transform arguments as input because it can depend on some
        transform parameters. For instance, if we are aggregating the rows
        (axis=0), then there might be an equivalent DP transform but if we are
        aggregating the columns there might not (axis=1).
        """

    async def private_queries(
        self, signature: SarusBoundSignature
    ) -> t.List[st.PrivateQuery]:
        """Return the PrivateQueries summarizing DP characteristics."""

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder: ...

    def py_output_hint(
        self,
        transform: st.Transform,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> t.Optional[str]:
        """May return a hint on the output's Python type.

        It returns an empty string if it cannot be inferred from the
        descriptions of the computation."""
