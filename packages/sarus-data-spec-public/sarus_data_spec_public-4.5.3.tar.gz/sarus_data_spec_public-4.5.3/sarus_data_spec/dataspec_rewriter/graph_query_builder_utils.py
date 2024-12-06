from typing import Any, Dict, List, Optional, Sequence, Set, Union

from sarus_data_spec.dataspec_validator.privacy_limit import DeltaEpsilonLimit
from sarus_data_spec.manager.async_utils import sync
from sarus_data_spec.manager.ops.processor import routing
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.sarus_query_builder.builders.composed_builder import (
        ComposedBuilder,
    )
    from sarus_data_spec.sarus_query_builder.core.core import (
        OptimizableQueryBuilder,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus" not in str(e_pandas_dp):
        raise

    # Placeholder classes
    class ComposedBuilder:  # type: ignore
        pass

    class OptimizableQueryBuilder:  # type: ignore
        pass


class GraphBuilder(ComposedBuilder):
    """Graph builder"""

    def __init__(
        self,
        dataspec: st.DataSpec,
        builders: Sequence[OptimizableQueryBuilder],
        dp_applicable_dataspecs: Sequence[st.DataSpec],
        weights: Sequence[float],
    ):
        assert len(builders) == len(weights)
        assert len(builders) == len(dp_applicable_dataspecs)
        self._dataset = dataspec  # type: ignore
        self._builders = builders
        self._weights = weights
        self._dp_applicable_dataspecs = dp_applicable_dataspecs

    def dataspec(self) -> st.DataSpec:
        return self._dataset

    def split_graph_builder_in_dict_of_builders(
        self,
    ) -> Dict[str, Any]:
        dict_builder = {}
        for builder, dataspec in zip(
            self._builders, self._dp_applicable_dataspecs
        ):
            dict_builder[dataspec.uuid()] = builder
        return dict_builder


def simple_graph_builder(
    dataspec: st.DataSpec,
    builders: Sequence[OptimizableQueryBuilder],
    dp_applicable_dataspecs: Sequence[st.DataSpec],
) -> GraphBuilder:
    return GraphBuilder(
        dataspec, builders, dp_applicable_dataspecs, [1] * len(builders)
    )


def build_and_fit_graph_builder(
    dataspec: st.DataSpec, privacy_limit: st.PrivacyLimit
) -> GraphBuilder:
    delta_epsilon_dict = privacy_limit.delta_epsilon_dict()
    delta, epsilon = next(iter(delta_epsilon_dict.items()))
    # build query builder for the computation graph
    graph_query_builder = build_graph_query_builder(dataspec)
    if graph_query_builder is not None and epsilon > 0:
        graph_query_builder.fit([(epsilon, delta)], (0, epsilon))
    return graph_query_builder


def extract_privacy_limit(
    dataspec: st.DataSpec,
    graph_query_buidler: GraphBuilder,
) -> Optional[st.PrivacyLimit]:
    """Return the privacy limit of the dataspec given the graph query builder"""
    if not graph_query_buidler.is_fitted():
        raise ValueError(
            """The graph_query_builder is not fitted, thus no privacy
                limit is defined for the dataspec"""
        )
    elif dataspec.uuid() == graph_query_buidler.dataspec().uuid():
        epsilon_deltas_budget = graph_query_buidler.epsilon_deltas_budget
        assert epsilon_deltas_budget is not None
        epsilon, delta = list(epsilon_deltas_budget)[0]
        return DeltaEpsilonLimit({delta: epsilon})
    else:
        return None


def build_graph_query_builder(dataspec: st.DataSpec) -> GraphBuilder:
    """Return all the private queries from a dataspec to the sources."""

    class BuilderVisitor(st.Visitor, st.TransformVisitor):
        visited: Set[Union[st.DataSpec, st.Transform]] = set()
        builders: List[ComposedBuilder] = list()
        dp_applicable_dataspecs: List[st.DataSpec] = list()

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
                if visited.is_dp_writable():
                    _, StaticChecker = routing.get_op(visited)
                    builder = sync(StaticChecker(visited).query_builder())
                    self.builders.append(builder)
                    self.dp_applicable_dataspecs.append(visited)

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

    visitor = BuilderVisitor()
    dataspec.accept(visitor)
    builders = visitor.builders
    dp_applicable_dataspecs = visitor.dp_applicable_dataspecs
    return simple_graph_builder(dataspec, builders, dp_applicable_dataspecs)
