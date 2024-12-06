from __future__ import annotations

from typing import (
    Collection,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)
import datetime
import typing as t

from sarus_data_spec.base import Referring
from sarus_data_spec.transform import Transform
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from enum import Enum


class Scalar(Referring[sp.Scalar]):
    """A python class to describe scalars"""

    def __init__(self, protobuf: sp.Scalar, store: bool = True) -> None:
        if protobuf.spec.HasField("transformed"):
            transformed = protobuf.spec.transformed
            self._referred = {
                transformed.transform,
                *transformed.arguments,
                *list(transformed.named_arguments.values()),
            }

        super().__init__(protobuf=protobuf, store=store)

    def prototype(self) -> Type[sp.Scalar]:
        """Return the type of the underlying protobuf."""
        return sp.Scalar

    def name(self) -> str:
        return self._protobuf.name

    def doc(self) -> str:
        return self._protobuf.doc

    def spec(self) -> str:
        return str(self._protobuf.spec.WhichOneof("spec"))

    def is_transformed(self) -> bool:
        """Is the scalar composed."""
        return self._protobuf.spec.HasField("transformed")

    def is_remote(self) -> bool:
        """Is the dataspec a remotely defined dataset."""
        return self.manager().is_remote(self)

    def is_source(self) -> bool:
        """Is the scalar not composed."""
        return not self.is_transformed()

    def is_pretrained_model(self) -> bool:
        if not self._protobuf.spec.HasField("model"):
            return False
        return (
            self._protobuf.spec.model.WhichOneof("type") == "pretrained_model"
        )

    def is_fitted_model(self) -> bool:
        if not self.is_transformed():
            return False
        transform = self.transform()
        return transform.protobuf().spec.WhichOneof("spec") in [
            "fit_model",
            "fit_model_dp",
        ]

    def is_privacy_params(self) -> bool:
        """Is the scalar privacy parameters."""
        return self._protobuf.spec.HasField("privacy_params")

    def is_random_seed(self) -> bool:
        """Is the scalar a random seed."""
        if self._protobuf.spec.HasField("random_seed"):
            return True
        if self.is_transformed():
            transform = self.transform()
            if transform.protobuf().spec.HasField("derive_seed"):
                return True
        return False

    def is_synthetic_model(self) -> bool:
        """Is the scalar composed."""
        return self._protobuf.spec.HasField("synthetic_model")

    def is_pup(self) -> bool:
        """Is the scalar PUP."""
        return False

    def pup_token(self) -> Optional[str]:
        """Returns the scalar PUP token."""
        return None

    def rewritten_pup_token(self) -> Optional[str]:
        return None

    def is_synthetic(self) -> bool:
        """Is the scalar synthetic."""
        return self.manager().dataspec_validator().is_synthetic(self)

    def is_dp(self) -> bool:
        """Is the dataspec the result of a DP transform"""
        return self.manager().dataspec_validator().is_dp(self)

    def is_public(self) -> bool:
        """Is the scalar public."""
        return self.manager().dataspec_validator().is_public(self)

    def is_dp_writable(self) -> bool:
        """Check if it exists a variant of this dataspec
        that utilizes the dp equivalent, and this variant is is_dp."""
        return self.manager().dataspec_validator().is_dp_writable(self)

    def is_pup_writable(self) -> bool:
        """Check if it exists a variant of this dataspec that is is_pup."""
        return False

    def is_publishable(self) -> bool:
        """Check if it exists a variant of this dataspec that is published"""
        return self.manager().dataspec_validator().is_publishable(self)

    def is_published(self) -> bool:
        """Check if the dataspec is the result of a DP transform or another
        published dataspec.
        There is at least one parent that is DP.
        Such a dataspec has at least one private query in its computation
        graph."""
        return self.manager().dataspec_validator().is_published(self)

    def is_big_data_computable(self) -> bool:
        return self.manager().dataspec_validator().is_big_data_computable(self)

    def status(self, task_names: t.Optional[List[str]]) -> Optional[st.Status]:
        """This method return a status that contains all the
        last updates for the task_names required. It returns None if
        all the tasks are missing."""

        if task_names is None:
            task_names = []
        if type(task_names) not in [list, set, tuple]:
            raise TypeError(
                f"Invalid task_names passed to dataset.status {task_names}"
            )
        last_status = self.manager().status(self)
        if last_status is None:
            return last_status
        if all([last_status.task(task) is None for task in task_names]):
            return None
        return last_status

    def transform(self) -> st.Transform:
        return cast(
            st.Transform,
            self.storage().referrable(
                self.protobuf().spec.transformed.transform
            ),
        )

    def parents(
        self,
    ) -> Tuple[
        List[Union[st.DataSpec, st.Transform]],
        Dict[str, Union[st.DataSpec, st.Transform]],
    ]:
        if not self.is_transformed():
            return list(), dict()

        args_id = self._protobuf.spec.transformed.arguments
        kwargs_id = self._protobuf.spec.transformed.named_arguments

        args_parents = [
            cast(
                Union[st.DataSpec, st.Transform],
                self.storage().referrable(uuid),
            )
            for uuid in args_id
        ]
        kwargs_parents = {
            name: cast(
                Union[st.DataSpec, st.Transform],
                self.storage().referrable(uuid),
            )
            for name, uuid in kwargs_id.items()
        }

        return args_parents, kwargs_parents

    def parents_list(
        self,
    ) -> t.List[st.DataSpec]:
        parents_args, parents_kwargs = self.parents()
        parents_args.extend(parents_kwargs.values())

        return [
            dataspec_parent
            for dataspec_parent in parents_args
            if isinstance(dataspec_parent, st.DataSpec)
        ]

    def sources(
        self, type_name: t.Optional[str] = sp.type_name(sp.Dataset)
    ) -> Set[st.DataSpec]:
        """Returns the set of non-transformed datasets that are parents
        of the current dataset"""
        sources = self.storage().sources(self, type_name=type_name)
        return sources

    def variant(
        self,
        kind: st.ConstraintKind,
        public_context: Collection[str] = (),
        privacy_limit: Optional[st.PrivacyLimit] = None,
    ) -> Optional[st.DataSpec]:
        return (
            self.manager()
            .dataspec_rewriter()
            .variant(self, kind, public_context, privacy_limit)
        )

    def variants(self) -> Collection[st.DataSpec]:
        return self.manager().dataspec_rewriter().variants(self)

    def private_queries(self) -> List[st.PrivateQuery]:
        """Return the list of PrivateQueries used in a Dataspec's transform.

        It represents the privacy loss associated with the current computation.

        It can be used by Sarus when a user (Access object) reads a DP dataspec
        to update its accountant. Note that Private Query objects are generated
        with a random uuid so that even if they are submitted multiple times to
        an account, they are only accounted once (ask @cgastaud for more on
        accounting)."""
        return self.manager().dataspec_validator().private_queries(self)

    def value(self) -> st.DataSpecValue:
        return self.manager().value(self)

    async def async_value(self) -> st.DataSpecValue:
        return await self.manager().async_value(self)

    # A Visitor acceptor
    def accept(self, visitor: st.Visitor) -> None:
        visitor.all(self)
        if self.is_transformed():
            visitor.transformed(
                self,
                cast(
                    Transform,
                    self.storage().referrable(
                        self._protobuf.spec.transformed.transform
                    ),
                ),
                *(
                    cast(Scalar, self.storage().referrable(arg))
                    for arg in self._protobuf.spec.transformed.arguments
                ),
                **{
                    name: cast(Scalar, self.storage().referrable(arg))
                    for name, arg in self._protobuf.spec.transformed.named_arguments.items()  # noqa: E501
                },
            )
        else:
            visitor.other(self)

    def dot(self) -> str:
        """return a graphviz representation of the scalar"""

        class Dot(st.Visitor):
            visited: Set[st.DataSpec] = set()
            nodes: Dict[str, Tuple[str, str]] = {}
            edges: Dict[Tuple[str, str], str] = {}

            def transformed(
                self,
                visited: st.DataSpec,
                transform: st.Transform,
                *arguments: st.DataSpec,
                **named_arguments: st.DataSpec,
            ) -> None:
                if visited not in self.visited:
                    if visited.prototype() == sp.Dataset:
                        self.nodes[visited.uuid()] = (
                            visited.name(),
                            "Dataset",
                        )
                    else:
                        self.nodes[visited.uuid()] = (visited.name(), "Scalar")

                    if not visited.is_remote():
                        for argument in arguments:
                            self.edges[(argument.uuid(), visited.uuid())] = (
                                transform.name()
                            )
                            argument.accept(self)
                        for _, argument in named_arguments.items():
                            self.edges[(argument.uuid(), visited.uuid())] = (
                                transform.name()
                            )
                            argument.accept(self)
                    self.visited.add(visited)

            def other(self, visited: st.DataSpec) -> None:
                if visited.prototype() == sp.Dataset:
                    self.nodes[visited.uuid()] = (
                        visited.name(),
                        "Dataset",
                    )
                else:
                    self.nodes[visited.uuid()] = (visited.name(), "Scalar")

            def all(self, visited: st.DataSpec) -> None:
                pass

        visitor = Dot()
        self.accept(visitor)
        result = "digraph {"
        for uuid, (label, node_type) in visitor.nodes.items():
            shape = "polygon" if node_type == "Scalar" else "ellipse"
            result += (
                f'\n"{uuid}" [label="{label} ({uuid[:2]})", shape={shape}];'
            )
        for (u1, u2), label in visitor.edges.items():
            result += f'\n"{u1}" -> "{u2}" [label="{label} ({uuid[:2]})"];'
        result += "}"
        return result

    def attribute(self, name: str) -> Optional[st.Attribute]:
        return self.manager().attribute(name=name, dataspec=self)

    def attributes(self, name: str) -> List[st.Attribute]:
        return self.manager().attributes(name=name, dataspec=self)


def privacy_budget(privacy_limit: st.PrivacyLimit) -> Scalar:
    delta_epsilon_dict = privacy_limit.delta_epsilon_dict()
    return Scalar(
        sp.Scalar(
            name="privacy_budget",
            spec=sp.Scalar.Spec(
                privacy_params=sp.Scalar.PrivacyParameters(
                    points=[
                        sp.Scalar.PrivacyParameters.Point(
                            epsilon=epsilon, delta=delta
                        )
                        for delta, epsilon in delta_epsilon_dict.items()
                    ]
                )
            ),
        )
    )


def random_seed(value: int) -> Scalar:
    return Scalar(
        sp.Scalar(
            name="seed",
            spec=sp.Scalar.Spec(random_seed=sp.Scalar.RandomSeed(value=value)),
        )
    )


class SampleType(str, Enum):
    PRETRAIN = "pretrain"
    INSTRUCT = "instruct"


def pretrained_model(
    foundation_model_name: str,
    sample_type: SampleType,
    checkpoint_path: t.Optional[str] = None,
) -> Scalar:
    return Scalar(
        sp.Scalar(
            name="Pretrained Model",
            spec=sp.Scalar.Spec(
                model=sp.Scalar.Model(
                    pretrained_model=sp.Scalar.Model.PretrainedModel(
                        foundation_model_name=foundation_model_name,
                        checkpoint_path=checkpoint_path
                        if checkpoint_path is not None
                        else "",
                        sample_type=sample_type.value,
                    )
                ),
            ),
        )
    )


def synthetic_model() -> Scalar:
    return Scalar(
        sp.Scalar(
            name="synthetic_model",
            spec=sp.Scalar.Spec(synthetic_model=sp.Scalar.SyntheticModel()),
            properties={"creation_time": str(datetime.datetime.now())},
        )
    )


class Visitor:
    """A visitor class for Scalar"""

    def all(self, visited: Scalar) -> None:
        return

    def transformed(
        self,
        visited: Scalar,
        transform: Transform,
        *arguments: Scalar,
        **named_arguments: Scalar,
    ) -> None:
        return

    def other(self, visited: Scalar) -> None:
        return
