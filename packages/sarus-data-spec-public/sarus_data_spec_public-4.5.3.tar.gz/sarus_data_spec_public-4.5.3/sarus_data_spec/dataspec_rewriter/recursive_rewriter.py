from time import time_ns
from typing import Any, Collection, Dict, List, Optional, Tuple, cast
import logging
import hashlib
from sarus_data_spec.context import global_context
from sarus_data_spec.dataset import transformed
from sarus_data_spec.dataspec_rewriter.base import BaseDataspecRewriter
from sarus_data_spec.dataspec_rewriter.graph_query_builder_utils import (
    GraphBuilder,
    build_and_fit_graph_builder,
    extract_privacy_limit,
)
from sarus_data_spec.dataspec_rewriter.simple_rules import (
    attach_variant,
    rewrite_mock,
    rewrite_synthetic,
)
from sarus_data_spec.dataspec_rewriter.utils import (
    find_dataspec_from_constraint,
)
from sarus_data_spec.dataspec_validator.privacy_limit import DeltaEpsilonLimit
from sarus_data_spec.dataspec_validator.recursive_validator import (
    RecursiveDataspecValidator,
)
from sarus_data_spec.manager.ops.processor import routing
from sarus_data_spec.scalar import privacy_budget
from sarus_data_spec.storage.typing import Storage
from sarus_data_spec.variant_constraint import dp_constraint
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.sarus_query_builder.builders.composed_builder import (
        ComposedBuilder,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus" not in str(e_pandas_dp):
        raise
    ComposedBuilder = Any  # type: ignore
    OptimizableQueryBuilder = Any

logger = logging.getLogger(__name__)


class RecursiveDataspecRewriter(BaseDataspecRewriter):
    def __init__(self, storage: Storage):
        self._storage = storage
        self._dataspec_validator = RecursiveDataspecValidator(storage=storage)
        self._rewriter_dict: Dict[
            Tuple[str, str], str
        ] = {}  # help to rewrite, avoid rewriting multipletime the same dataspec

    def rewriter_dict(self) -> Dict[Tuple[str, str], str]:
        return self._rewriter_dict

    def rewrite_uuid(
        self,
        dataspec_uuid: str,
        privacy_limit: Optional[st.PrivacyLimit] = None,
    ) -> str:
        rewrite_uuid = dataspec_uuid + str(time_ns())
        return rewrite_uuid

    def get_transform_for_dp_rewriting(
        self, dataspec: st.DataSpec
    ) -> st.Transform:
        """Returns the appropriate transform for rewriting
        a dataspec in the context of DP rewriting."""
        if not dataspec.is_transformed():
            raise ValueError(
                """A not transformed dataspec does not
                have transform for rewriting"""
            )

        if dataspec.is_dp_writable():
            _, StaticChecker = routing.get_op(dataspec)
            transform_to_use = StaticChecker(dataspec).dp_transform()
            if transform_to_use is None:
                raise ValueError(
                    "A DP applicable dataspec should have a dp transform"
                )
        else:
            transform_to_use = dataspec.transform()
        return transform_to_use

    def get_transform_for_pup_rewriting(
        self, dataspec: st.DataSpec
    ) -> st.Transform:
        """Returns the appropriate transform for rewriting
        a dataspec in the context of PUP rewriting."""
        if not dataspec.is_transformed():
            raise ValueError(
                """A not transformed dataspec does not
                have transform for rewriting"""
            )

        if dataspec.is_pup_writable():
            dataset = cast(st.Dataset, dataspec)
            _, StaticChecker = routing.get_op(dataspec)
            transform_to_use = StaticChecker(dataset).pup_transform()
            if transform_to_use is None:
                raise ValueError(
                    "A PUP applicable dataspec should have a pup transform"
                )
        else:
            transform_to_use = dataspec.transform()
        return transform_to_use

    def variant(
        self,
        dataspec: st.DataSpec,
        kind: st.ConstraintKind,
        public_context: Collection[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[st.DataSpec]:
        return self.rewrite(
            dataspec,
            kind,
            public_context,
            privacy_limit,
        )

    def rewrite(
        self,
        dataspec: st.DataSpec,
        target_kind: st.ConstraintKind,
        public_context: Collection[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[st.DataSpec]:
        """Returns a compliant dataspec or None."""

        if target_kind == st.ConstraintKind.SYNTHETIC:
            variant, _ = rewrite_synthetic(
                self.dataspec_validator(),
                dataspec,
                public_context,
            )
            return variant

        elif target_kind == st.ConstraintKind.MOCK:
            mock_variant, _ = rewrite_mock(
                self.dataspec_validator(),
                dataspec,
                public_context,
            )
            return mock_variant

        if privacy_limit is None:
            raise ValueError(
                "Privacy limit must be defined for PUP or DP rewriting"
            )

        rewrite_uuid = self.rewrite_uuid(
            dataspec.uuid(), privacy_limit=privacy_limit
        )

        if target_kind == st.ConstraintKind.DP:
            if not dataspec.is_publishable():
                return rewrite_synthetic(
                    self.dataspec_validator(), dataspec, public_context
                )[0]
            # a dp rewriting require some minimum budget
            delta_epsilon_dict = privacy_limit.delta_epsilon_dict()
            _, epsilon = next(iter(delta_epsilon_dict.items()))
            if epsilon == 0:
                return rewrite_synthetic(
                    self.dataspec_validator(), dataspec, public_context
                )[0]
            graph_query_builder = build_and_fit_graph_builder(
                dataspec, privacy_limit
            )

            variant, _ = self.rewrite_dp(
                dataspec,
                public_context=public_context,
                graph_query_builder=graph_query_builder,
                rewrite_uuid=rewrite_uuid,
            )
            return variant

        elif target_kind == st.ConstraintKind.PUP:
            if not dataspec.is_pup_writable():
                return rewrite_synthetic(
                    self.dataspec_validator(), dataspec, public_context
                )[0]
            graph_query_builder = build_and_fit_graph_builder(
                dataspec, privacy_limit
            )
            variant, _ = self.rewrite_pup(
                dataspec,
                public_context=public_context,
                graph_query_builder=graph_query_builder,
                rewrite_uuid=rewrite_uuid,
            )
            return variant
        else:
            raise ValueError(
                f"Privacy policy {target_kind} rewriting not implemented yet"
            )

    def find_variant_from_rewriter(
        self, uuid: str, rewrite_uuid: Optional[str] = None
    ) -> Optional[st.DataSpec]:
        """Returna an already computed variant of a dataspec from the
        current rewriting defined by the rewrite uuid.

        Args:
            uuid (str): The uuid of the dataspec to be rewritten.
            rewrite_uuid (Optional[str], optional): The rewrite uuid to keep
            track of the already rewritten dataspec. Defaults to None.

        Returns:
            Optional[st.DataSpec]: The already computed variant or None.
        """
        if rewrite_uuid is None:
            return None
        # find already computed variant during the rewriting
        if (uuid, rewrite_uuid) in self.rewriter_dict():
            variant_uuid = self.rewriter_dict()[(uuid, rewrite_uuid)]
            variant = self.storage().referrable(variant_uuid)
            assert variant is not None
            dataspec = cast(st.DataSpec, variant)
            return dataspec
        else:
            return None

    def _rewrite_arg(
        self,
        arg: st.DataSpec,
        public_context: Collection[str],
        graph_query_builder: GraphBuilder,
        rewrite_uuid: Optional[str] = None,
    ) -> st.DataSpec:
        """
        Rewrites the dataspec 'arg' to the appropriate variant based on its
        properties.

        Currently, the function assumes that there is only one DP/PUP variant
        for any dataspec (excluding synthetic variants).
        This assumption may change in the future, and the function should be
        updated accordingly.

        Args:
            arg (st.DataSpec): The dataspec to be rewritten.
            public_context (Collection[str]): The public context for the
            rewriting process.
            graph_query_builder (GraphBuilder): The graph query builder for
            the dataspec being rewritten.
            rewrite_uuid (Optional[str], optional): An optional UUID string
            for tracking the rewrite process. Defaults to None.

        Raises:
            ValueError: If the dataspec is not rewritable.

        Returns:
            st.DataSpec: The rewritten dataspec variant.
        """
        if isinstance(arg, st.DataSpec):
            # TODO decide what to do when a dataset is both
            # is_dp_writable and is_pup_writable. For select_sql with
            # qrlew now a dataset can be both.
            # In this case, for the moment, the innermost
            # dp_writable and pup_writable select sql will be rewritten in dp.
            if arg.is_publishable():
                rewritten_arg = self.rewrite_dp(
                    arg,
                    public_context,
                    graph_query_builder=graph_query_builder,
                    rewrite_uuid=rewrite_uuid,
                )[0]
            elif arg.is_pup_writable():
                rewritten_arg = self.rewrite_pup(
                    arg,
                    public_context,
                    graph_query_builder=graph_query_builder,
                    rewrite_uuid=rewrite_uuid,
                )[0]
            elif arg.is_public():
                rewritten_arg = arg
            else:
                raise ValueError(
                    f"""No rewriting possible for
                    the dataspec: {arg.uuid()}. """
                )
        else:
            rewritten_arg = arg
        return rewritten_arg

    def _rewrite_parents(
        self,
        dataspec: st.DataSpec,
        public_context: Collection[str],
        graph_query_builder: GraphBuilder,
        rewrite_uuid: Optional[str] = None,
    ) -> Tuple[List[st.DataSpec[Any]], Dict[str, st.DataSpec[Any]]]:
        """Rewrites all the parents of the dataspec to the appropriate variant
        based on its
        properties.

        Args:
            dataspec (st.DataSpec): The dataspec to be rewritten.
            public_context (Collection[str]): The public context for the
            rewriting process.
            graph_query_builder (GraphBuilder): The graph query builder for
            the dataspec being rewritten.
            rewrite_uuid (Optional[str], optional): An optional UUID string
            for tracking the rewrite process. Defaults to None.

        Returns:
            Tuple[List[st.DataSpec[Any]], Dict[str, st.DataSpec[Any]]]:
            rewrited parents
        """
        args, kwargs = dataspec.parents()
        rewritten_args = []
        for arg in args:
            assert isinstance(arg, st.DataSpec)
            rewritten_arg = self._rewrite_arg(
                arg,
                public_context,
                graph_query_builder,
                rewrite_uuid,
            )
            rewritten_args.append(rewritten_arg)

        rewritten_kwargs = {}
        for name, arg in kwargs.items():
            assert isinstance(arg, st.DataSpec)
            rewritten_arg = self._rewrite_arg(
                arg,
                public_context,
                graph_query_builder,
                rewrite_uuid,
            )
            rewritten_kwargs[name] = rewritten_arg
        return rewritten_args, rewritten_kwargs

    def rewrite_dp(
        self,
        dataspec: st.DataSpec,
        public_context: Collection[str],
        graph_query_builder: GraphBuilder,
        deterministic_seed: bool = True,
        rewrite_uuid: Optional[str] = None,
    ) -> Tuple[st.DataSpec, Collection[str]]:
        """
        Return an "is_publishable" dataspec into an "is_published" variant.

        Args:
            dataspec (st.DataSpec): The dataspec to be rewritten.
            public_context (Collection[str]): Not used yet.
            graph_query_builder (GraphBuilder): The graph query builder of the
            dataspec we are rewriting.
            rewrite_uuid (Optional[str]): A UUID string for tracking the
            rewrite process. Default is None.

        Returns:
            Tuple[st.DataSpec, Collection[str]]: A tuple containing the
            "is_published" dataspec and an updated collection of public
            context information.

        Note:
            The dataspec provided must be "is_publishable" for the
            rewriting to proceed. Ensure that the dataspec
            meets this criterion before invoking this function.
        """

        if not dataspec.is_publishable():
            raise ValueError(
                "Try to rewrite with dp a non publishable dataspec"
            )

        if dataspec.is_published():
            return dataspec, public_context

        if graph_query_builder is None:
            raise ValueError(
                """A Dataspec dp publishable but not published should have a
                graph query builder to be published. """
            )

        # find already computed variant during the rewriting
        existing_variant = self.find_variant_from_rewriter(
            dataspec.uuid(), rewrite_uuid
        )
        if existing_variant is not None:
            return existing_variant, public_context

        # find already computed variant from constraint
        privacy_limit = extract_privacy_limit(dataspec, graph_query_builder)

        kind = st.ConstraintKind.DP
        if privacy_limit is not None:
            existing_variant = find_dataspec_from_constraint(
                dataspec_validator=self.dataspec_validator(),
                dataspec=dataspec,
                kind=kind,
                public_context=public_context,
                privacy_limit=privacy_limit,
            )
            if existing_variant is not None:
                return existing_variant, public_context

        # rewrite parents
        rewritten_args, rewritten_kwargs = self._rewrite_parents(
            dataspec=dataspec,
            public_context=public_context,
            graph_query_builder=graph_query_builder,
            rewrite_uuid=rewrite_uuid,
        )

        # create dataspec
        transform_to_use = self.get_transform_for_dp_rewriting(
            dataspec=dataspec
        )
        if dataspec.is_dp_writable():
            dict_builder = (
                graph_query_builder.split_graph_builder_in_dict_of_builders()
            )
            if dataspec.uuid() not in dict_builder:
                raise ValueError(
                    "A is_dp_writable dataspec should have a builder"
                )
            builder = dict_builder[dataspec.uuid()]
            dataspec_epsilon_deltas_budget = builder.epsilon_deltas_budget
            if dataspec_epsilon_deltas_budget is None:
                raise ValueError(
                    """The graph_query_builder is not fitted, thus no budget
                 is defined for the dp rewriting"""
                )
            epsilon, delta = list(dataspec_epsilon_deltas_budget)[0]
            dataspec_privacy_limit = DeltaEpsilonLimit({delta: epsilon})

            budget = privacy_budget(dataspec_privacy_limit)

            if deterministic_seed:
                ## feed all informations needed for the transform
                salt = salt_from_dataspec_info(
                    dataspec,
                    budget,
                    transform_to_use,
                    *rewritten_args,
                    kwargs=rewritten_kwargs,
                )
            else:
                salt = time_ns()

            seed = global_context().generate_seed(salt=salt)

            dp_variant = cast(
                st.DataSpec,
                transformed(
                    transform_to_use,
                    *rewritten_args,
                    dataspec_type=sp.type_name(dataspec.prototype()),
                    dataspec_name=None,
                    budget=budget,
                    seed=seed,
                    **rewritten_kwargs,
                ),
            )
        else:
            dp_variant = cast(
                st.DataSpec,
                transformed(
                    transform_to_use,
                    *rewritten_args,
                    dataspec_type=sp.type_name(dataspec.prototype()),
                    dataspec_name=None,
                    **rewritten_kwargs,
                ),
            )
        # cache result in rewriter
        if rewrite_uuid is not None:
            self.rewriter_dict()[(dataspec.uuid(), rewrite_uuid)] = (
                dp_variant.uuid()
            )

        # attach constraints
        if privacy_limit is not None:
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

        # We also attach the dataspec's synthetic/mock variant
        # to be the DP dataspec's synthetic variant. This is to
        # avoid to have DP computations in the MOCK.
        syn_variant = dataspec.variant(st.ConstraintKind.SYNTHETIC)
        if syn_variant is None:
            raise ValueError("Could not find a synthetic variant.")
        attach_variant(
            original=dp_variant,
            variant=syn_variant,
            kind=st.ConstraintKind.SYNTHETIC,
        )

        mock_variant = dataspec.variant(st.ConstraintKind.MOCK)
        if mock_variant is None:
            raise ValueError("Could not find a mock variant.")
        attach_variant(
            original=dp_variant,
            variant=mock_variant,
            kind=st.ConstraintKind.MOCK,
        )

        assert dp_variant.is_published()
        return dp_variant, public_context

    def rewrite_pup(
        self,
        dataspec: st.DataSpec,
        public_context: Collection[str],
        graph_query_builder: GraphBuilder,
        rewrite_uuid: Optional[str] = None,
    ) -> Tuple[st.DataSpec, Collection[str]]:
        """
        Return an "is_pup_writable" dataspec into an pup variant.

        Args:
            dataspec (st.DataSpec): The dataspec to be rewritten.
            public_context (Collection[str]): Not used yet.
            graph_query_builder (GraphBuilder): The graph query builder of the
            dataspec we are rewriting
            rewrite_uuid (Optional[str]): A UUID string for tracking the
            rewrite process. Default is None.

        Returns:
            Tuple[st.DataSpec, Collection[str]]: A tuple containing the
            "is_pup" dataspec and an updated collection of public
            context information.

        Note:
            The dataspec provided must be "is_pup_writable" for the
            rewriting to proceed. Ensure that the dataspec
            meets this criterion before invoking this function.
        """
        if not dataspec.is_pup_writable():
            raise ValueError(
                "Try to rewrite in pup a non pup appicable dataspec"
            )

        if dataspec.is_pup():
            return dataspec, public_context

        # find already computed variant during the rewriting
        existing_variant = self.find_variant_from_rewriter(
            dataspec.uuid(), rewrite_uuid
        )
        if existing_variant is not None:
            return existing_variant, public_context

        if graph_query_builder is not None:
            privacy_limit = extract_privacy_limit(
                dataspec, graph_query_builder
            )

        # find already computed variant from constraint
        kind = st.ConstraintKind.PUP
        if privacy_limit is not None:
            existing_variant = find_dataspec_from_constraint(
                dataspec_validator=self.dataspec_validator(),
                dataspec=dataspec,
                kind=kind,
                public_context=public_context,
                privacy_limit=privacy_limit,
            )
            if existing_variant is not None:
                return existing_variant, public_context

        # rewrite parents
        rewritten_args, rewritten_kwargs = self._rewrite_parents(
            dataspec=dataspec,
            public_context=public_context,
            graph_query_builder=graph_query_builder,
            rewrite_uuid=rewrite_uuid,
        )

        # create dataspec
        transform_to_use = self.get_transform_for_pup_rewriting(
            dataspec=dataspec
        )
        pup_variant = cast(
            st.DataSpec,
            transformed(
                transform_to_use,
                *rewritten_args,
                dataspec_type=sp.type_name(dataspec.prototype()),
                dataspec_name=None,
                **rewritten_kwargs,
            ),
        )

        # cache result in rewriter
        if rewrite_uuid is not None:
            self.rewriter_dict()[(dataspec.uuid(), rewrite_uuid)] = (
                pup_variant.uuid()
            )

        # We also attach the dataspec's synthetic/mock variant
        # to be the DP dataspec's synthetic variant. This is to
        # avoid to have DP computations in the MOCK.
        syn_variant = dataspec.variant(st.ConstraintKind.SYNTHETIC)
        if syn_variant is None:
            raise ValueError("Could not find a synthetic variant.")
        attach_variant(
            original=pup_variant,
            variant=syn_variant,
            kind=st.ConstraintKind.SYNTHETIC,
        )

        mock_variant = dataspec.variant(st.ConstraintKind.MOCK)
        if mock_variant is None:
            raise ValueError("Could not find a mock variant.")
        attach_variant(
            original=pup_variant,
            variant=mock_variant,
            kind=st.ConstraintKind.MOCK,
        )

        # assert pup_variant.pup_token() is not None
        assert pup_variant.is_pup()
        return pup_variant, public_context


def salt_from_dataspec_info(
    *args: st.Referrable, kwargs: Dict[str, st.DataSpec[Any]]
) -> int:
    """Returns a hash of the arguments and keyword arguments. Such hash
    should not depend on the order of the arguments, nor the kwargs.
    The alogorithm is as follows:
    - hash args, and hash the tuple (keyword,value) of kwargs
    - sort all of the hashes
    - hash the sorted list
    """

    hashes = [arg.uuid().encode() for arg in args]
    for name, item in kwargs.items():
        item_uuid = item.uuid()
        hashmd5 = hashlib.md5(usedforsecurity=False)
        hashmd5.update(name.encode())
        hashmd5.update(item_uuid.encode())
        hashes.append(hashmd5.digest())
    hashes = sorted(hashes)
    hashmd5 = hashlib.md5(usedforsecurity=False)
    for el in sorted(hashes):
        hashmd5.update(el)
    return hash(hashmd5.hexdigest())
