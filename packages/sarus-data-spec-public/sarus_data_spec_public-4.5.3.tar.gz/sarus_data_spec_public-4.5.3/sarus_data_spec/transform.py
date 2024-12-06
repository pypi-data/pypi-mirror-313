from __future__ import annotations

import datetime
import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.base import Referrable
from sarus_data_spec.constants import (
    BIG_DATA_TASK,
    SAMPLE_SIZE_N_LINES,
    SARUS_DEFAULT_OUTPUT,
)

from sarus_data_spec.context import global_context
from sarus_data_spec.json_serialisation import (
    SarusJSONDecoder,
    SarusJSONEncoder,
)
from sarus_data_spec.path import straight_path
import sarus_data_spec.dataset as sd
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class Transform(Referrable[sp.Transform]):
    """A python class to describe transforms"""

    def prototype(self) -> t.Type[sp.Transform]:
        """Return the type of the underlying protobuf."""
        return sp.Transform

    def name(self) -> str:
        return self._protobuf.name

    def doc(self) -> str:
        return self._protobuf.doc

    def is_composed(self) -> bool:
        """Is the transform composed."""
        return self._protobuf.spec.HasField("composed")

    def is_variable(self) -> bool:
        """Is the transform a variable."""
        return self._protobuf.spec.HasField("variable")

    def spec(self) -> str:
        return t.cast(str, self._protobuf.spec.WhichOneof("spec"))

    def is_external(self) -> bool:
        """Is the transform an external operation."""
        return self._protobuf.spec.HasField("external")

    def infer_dataset_or_scalar(
        self,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> t.Tuple[str, t.Callable[[st.DataSpec], None]]:
        """Guess if the external transform output is a Dataset or a Scalar.

        Registers schema if it is a Dataset and returns the value type.
        """
        return self.manager().infer_dataset_or_scalar(
            self, *arguments, **named_arguments
        )

    def transforms(self) -> t.Set[st.Transform]:
        """return all transforms (and avoid infinite recursions/loops)"""

        class Transforms(st.TransformVisitor):
            visited: t.Set[st.Transform] = set()

            def all(self, visited: st.Transform) -> None:
                self.visited.add(visited)

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                self.visited.add(transform)
                if transform not in self.visited:
                    transform.accept(self)
                for arg in arguments:
                    if arg not in self.visited:
                        arg.accept(self)
                for arg in named_arguments.values():
                    if arg not in self.visited:
                        arg.accept(self)

            def other(self, visited: st.Transform) -> None:
                raise ValueError(
                    "A composed transform can only have Variables "
                    "or Composed ancestors."
                )

            def variable(
                self,
                visited: st.Transform,
                name: str,
                position: int,
            ) -> None:
                return

        visitor = Transforms()
        self.accept(visitor)
        return visitor.visited

    def variables(self) -> t.Set[st.Transform]:
        """Return all the variables from a composed transform"""
        return {
            transform
            for transform in self.transforms()
            if transform.is_variable()
        }

    def compose(
        self,
        *compose_arguments: st.Transform,
        **compose_named_arguments: st.Transform,
    ) -> st.Transform:
        class Compose(st.TransformVisitor):
            visited: t.Set[st.Transform] = set()
            result: st.Transform

            def variable(
                self,
                visited: st.Transform,
                name: str,
                position: int,
            ) -> None:
                self.result = visited
                self.result = compose_named_arguments[name]

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                if visited not in self.visited:
                    self.result = composed(
                        transform,
                        *(
                            arg.compose(
                                *compose_arguments, **compose_named_arguments
                            )
                            for arg in arguments
                        ),
                        **{
                            name: arg.compose(
                                *compose_arguments, **compose_named_arguments
                            )
                            for name, arg in named_arguments.items()
                        },
                    )
                    self.visited.add(visited)
                else:
                    self.result = visited

            def other(self, visited: st.Transform) -> None:
                self.result = composed(
                    visited, *compose_arguments, **compose_named_arguments
                )

            def all(self, visited: st.Transform) -> None:
                pass

        visitor = Compose()
        self.accept(visitor)
        return visitor.result

    def apply(
        self,
        *apply_arguments: st.DataSpec,
        **apply_named_arguments: st.DataSpec,
    ) -> st.DataSpec:
        class Apply(st.TransformVisitor):
            visited: t.Dict[st.Transform, st.DataSpec] = {}
            result: st.DataSpec

            def variable(
                self,
                visited: st.Transform,
                name: str,
                position: int,
            ) -> None:
                self.result = apply_named_arguments[name]
                if self.result is None:
                    raise ValueError("Cannot substitute all variables")

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                if visited not in self.visited:
                    self.result = t.cast(
                        sd.Dataset,
                        sd.transformed(
                            transform,
                            *(
                                arg.apply(
                                    *apply_arguments, **apply_named_arguments
                                )
                                for arg in arguments
                            ),
                            dataspec_type=None,
                            dataspec_name=None,
                            **{
                                name: arg.apply(
                                    *apply_arguments, **apply_named_arguments
                                )
                                for name, arg in named_arguments.items()
                            },
                        ),
                    )
                    self.visited[visited] = self.result

            def other(self, visited: st.Transform) -> None:
                self.result = sd.transformed(
                    visited,
                    *apply_arguments,
                    dataspec_type=None,
                    dataspec_name=None,
                    **apply_named_arguments,
                )

            def all(self, visited: st.Transform) -> None:
                pass

        visitor = Apply()
        self.accept(visitor)
        return visitor.result

    def abstract(
        self,
        *arguments: str,
        **named_arguments: str,
    ) -> st.Transform:
        return composed(
            self,
            *(variable(name=arg) for arg in arguments),
            **{
                name: variable(name=arg)
                for name, arg in named_arguments.items()
            },
        )

    def __call__(
        self,
        *arguments: t.Union[st.Transform, st.DataSpec, int, str],
        **named_arguments: t.Union[st.Transform, st.DataSpec, int, str],
    ) -> t.Union[st.Transform, st.DataSpec]:
        """Applies the transform to another element"""
        n_transforms = 0
        n_datasets = 0
        n_variables = 0
        for arg in arguments:
            n_transforms += int(isinstance(arg, Transform))
            n_datasets += int(isinstance(arg, st.DataSpec))
            n_variables += int(isinstance(arg, int) or isinstance(arg, str))
        for arg in named_arguments.values():
            n_transforms += int(isinstance(arg, Transform))
            n_datasets += int(isinstance(arg, st.DataSpec))
            n_variables += int(isinstance(arg, int) or isinstance(arg, str))

        total = len(arguments) + len(named_arguments)
        if total == 0:
            # If no argument is passed, we consider that we should apply
            return self.apply(
                *t.cast(t.Sequence[st.DataSpec], arguments),
                **t.cast(t.Mapping[str, st.DataSpec], named_arguments),
            )
        elif n_transforms == total:
            return self.compose(
                *t.cast(t.Sequence[Transform], arguments),
                **t.cast(t.Mapping[str, Transform], named_arguments),
            )
        elif n_variables == total:
            return self.abstract(
                *t.cast(t.Sequence[str], arguments),
                **t.cast(t.Mapping[str, str], named_arguments),
            )
        elif n_transforms + n_datasets == total:
            return self.apply(
                *t.cast(t.Sequence[st.DataSpec], arguments),
                **t.cast(t.Mapping[str, st.DataSpec], named_arguments),
            )

        return self

    def __mul__(self, argument: st.Transform) -> st.Transform:
        return self.compose(argument)

    # A Visitor acceptor
    def accept(self, visitor: st.TransformVisitor) -> None:
        visitor.all(self)
        if self.is_composed():
            visitor.composed(
                self,
                t.cast(
                    Transform,
                    self.storage().referrable(
                        self._protobuf.spec.composed.transform
                    ),
                ),
                *(
                    t.cast(Transform, self.storage().referrable(transform))
                    for transform in self._protobuf.spec.composed.arguments
                ),
                **{
                    name: t.cast(
                        Transform, self.storage().referrable(transform)
                    )
                    for name, transform in self._protobuf.spec.composed.named_arguments.items()  # noqa: E501
                },
            )
        elif self.is_variable():
            var = self._protobuf.spec.variable
            visitor.variable(self, name=var.name, position=var.position)
        else:
            visitor.other(self)

    def dot(self) -> str:
        """return a graphviz representation of the transform"""

        class Dot(st.TransformVisitor):
            visited: t.Set[st.Transform] = set()
            nodes: t.Dict[str, str] = {}
            edges: t.Set[t.Tuple[str, str]] = set()

            def variable(
                self,
                visited: st.Transform,
                name: str,
                position: int,
            ) -> None:
                self.nodes[visited.uuid()] = f"{name} ({position})"

            def composed(
                self,
                visited: st.Transform,
                transform: st.Transform,
                *arguments: st.Transform,
                **named_arguments: st.Transform,
            ) -> None:
                if visited not in self.visited:
                    transform.accept(self)
                    self.nodes[visited.uuid()] = transform.name()
                    for argument in arguments:
                        self.edges.add((argument.uuid(), visited.uuid()))
                        argument.accept(self)
                    for _, argument in named_arguments.items():
                        self.edges.add((argument.uuid(), visited.uuid()))
                        argument.accept(self)
                    self.visited.add(visited)

            def other(self, visited: st.Transform) -> None:
                raise NotImplementedError

            def all(self, visited: st.Transform) -> None:
                pass

        visitor = Dot()
        self.accept(visitor)
        result = "digraph {"
        for uuid, label in visitor.nodes.items():
            result += f'\n"{uuid}" [label="{label} ({uuid[:2]})"];'
        for u1, u2 in visitor.edges:
            result += f'\n"{u1}" -> "{u2}";'
        result += "}"
        return result

    def transform_to_apply(self) -> st.Transform:
        """Return the transform of a composed transform."""
        assert self.is_composed()
        uuid = self.protobuf().spec.composed.transform
        return t.cast(st.Transform, self.storage().referrable(uuid))

    def composed_parents(
        self,
    ) -> t.Tuple[t.List[st.Transform], t.Dict[str, st.Transform]]:
        """Return the parents of a composed transform."""
        assert self.is_composed()

        args_id = self._protobuf.spec.composed.arguments
        kwargs_id = self._protobuf.spec.composed.named_arguments

        args_parents = [
            t.cast(st.Transform, self.storage().referrable(uuid))
            for uuid in args_id
        ]
        kwargs_parents = {
            name: t.cast(st.Transform, self.storage().referrable(uuid))
            for name, uuid in kwargs_id.items()
        }
        return args_parents, kwargs_parents

    def composed_callable(self) -> t.Callable[..., t.Any]:
        """Return the composed transform's equivalent callable.

        The function takes an undefined number of named arguments.
        """
        return self.manager().composed_callable(self)

    def output_type(
        self,
    ) -> t.Optional[
        t.Literal["sarus_data_spec.Dataset", "sarus_data_spec.Scalar"]
    ]:
        """Returns the Dataspec type created by the transform. If the type
        cannot be known because it depends on the input arguments, None
        is returned"""

        if self.spec() in [
            "privacy_unit_tracking_paths",
            "automatic_user_settings",
            "public_paths",
            "automatic_budget",
            "attribute_budget",
            "sd_budget",
            "sampling_ratios",
            "derive_seed",
            "relationship_spec",
            "validated_user_type",
            "error_estimation",
            "fit_model",
            "fit_model_dp",
        ]:
            return "sarus_data_spec.Scalar"

            # Other internal transforms return a Dataset
        if not self.is_external():
            return "sarus_data_spec.Dataset"

        return None


# Builders
def identity() -> Transform:
    return Transform(
        sp.Transform(
            name="Identity",
            spec=sp.Transform.Spec(identity=sp.Transform.Identity()),
            inversible=True,
            schema_preserving=True,
        )
    )


def variable(name: str, position: int = 0) -> Transform:
    return Transform(
        sp.Transform(
            name="Variable",
            spec=sp.Transform.Spec(
                variable=sp.Transform.Variable(
                    name=name,
                    position=position,
                )
            ),
            inversible=True,
            schema_preserving=True,
        )
    )


def composed(
    transform: st.Transform,
    *arguments: st.Transform,
    **named_arguments: st.Transform,
) -> st.Transform:
    if transform.is_composed():
        # We want to compose simple transforms only
        return transform.compose(*arguments, **named_arguments)
    return Transform(
        sp.Transform(
            name="Composed",
            spec=sp.Transform.Spec(
                composed=sp.Transform.Composed(
                    transform=transform.uuid(),
                    arguments=(a.uuid() for a in arguments),
                    named_arguments={
                        n: a.uuid() for n, a in named_arguments.items()
                    },
                )
            ),
        )
    )


def op_identifier_from_id(id: str) -> sp.Transform.External.OpIdentifier:
    """Build an OpIdentifier protobuf message from a string identifier.

    Args:
        identifier (str): id in the form library.name (e.g. sklearn.PD_MEAN)
    """
    parts = id.split(".")
    if len(parts) != 2:
        raise ValueError(
            f"Transform ID {id} should have the format library.name"
        )
    library, name = parts

    mapping = {
        "std": sp.Transform.External.Std,
        "sklearn": sp.Transform.External.Sklearn,
        "pandas": sp.Transform.External.Pandas,
        "pandas_profiling": sp.Transform.External.PandasProfiling,
        "numpy": sp.Transform.External.Numpy,
        "tensorflow": sp.Transform.External.Tensorflow,
        "xgboost": sp.Transform.External.XGBoost,
        "skopt": sp.Transform.External.Skopt,
        "imblearn": sp.Transform.External.Imblearn,
        "shap": sp.Transform.External.Shap,
        "scipy": sp.Transform.External.Scipy,
        "optbinning": sp.Transform.External.OptBinning,
    }

    if library not in mapping.keys():
        raise ValueError(f"Unsupported library {library}")

    MsgClass = mapping[library]
    msg = sp.Transform.External.OpIdentifier()
    getattr(msg, library).CopyFrom(MsgClass(name=name))
    return msg


def transform_id(transform: st.Transform) -> str:
    """Return the transform id."""
    spec = transform.protobuf().spec
    spec_type = transform.spec()
    if spec_type == "external":
        library = str(spec.external.op_identifier.WhichOneof("op"))
        op_name = getattr(spec.external.op_identifier, library).name
        return f"{library}.{op_name}"
    else:
        return spec_type


def external(
    id: str,
    py_args: t.Optional[t.Dict[int, t.Any]] = None,
    py_kwargs: t.Optional[t.Dict[str, t.Any]] = None,
    ds_args_pos: t.Optional[t.List[int]] = None,
    ds_types: t.Optional[t.Dict[t.Union[int, str], str]] = None,
    sarus_default_output: t.Optional[t.Union[pa.Table, pd.DataFrame]] = None,
) -> st.Transform:
    """Create an external library transform.

    Args:
        id (str): id in the form library.name (e.g. sklearn.PD_MEAN)
        py_args (Dict[int, Any]):
            the Python objects passed as arguments to the transform.
        py_kwargs (Dict[int, Any]):
            the Python objects passed as keyword arguments to the transform.
        ds_args_pos (List[int]):
            the positions of Dataspecs passed in args.
        ds_types (Dict[int | str, str]):
            the types of the Dataspecs passed as arguments.
    """
    if py_args is None:
        py_args = {}
    if py_kwargs is None:
        py_kwargs = {}
    if ds_args_pos is None:
        ds_args_pos = []
    if ds_types is None:
        ds_types = {}
    external = sp.Transform.External(
        arguments=SarusJSONEncoder.encode_bytes([]),
        named_arguments=SarusJSONEncoder.encode_bytes(
            {
                "py_args": py_args,
                "py_kwargs": py_kwargs,
                "ds_args_pos": ds_args_pos,
                "ds_types": ds_types,
            }
        ),
        op_identifier=op_identifier_from_id(id),
    )

    transform = Transform(
        sp.Transform(
            name=id,
            spec=sp.Transform.Spec(
                external=external,
            ),
        )
    )

    return (
        transform
        if sarus_default_output is None
        else add_sarus_default_output(transform, sarus_default_output)
    )


def project(projection: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name="Project",
            spec=sp.Transform.Spec(
                project=sp.Transform.Project(projection=projection.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def filter(filter: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name="Filter",
            spec=sp.Transform.Spec(
                filter=sp.Transform.Filter(filter=filter.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def get_item(path: st.Path) -> st.Transform:
    return Transform(
        sp.Transform(
            name="get_item",
            spec=sp.Transform.Spec(
                get_item=sp.Transform.GetItem(path=path.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def select_table(path: st.Path) -> Transform:
    return Transform(
        sp.Transform(
            name="select_table",
            spec=sp.Transform.Spec(
                select_table=sp.Transform.SelectTable(path=path.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def shuffle() -> Transform:
    return Transform(
        sp.Transform(
            name="Shuffle",
            spec=sp.Transform.Spec(shuffle=sp.Transform.Shuffle()),
            inversible=False,
            schema_preserving=True,
        )
    )


def join(on: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name="Join",
            spec=sp.Transform.Spec(join=sp.Transform.Join(on=on.protobuf())),
            inversible=False,
            schema_preserving=False,
        )
    )


def cast(type: st.Type) -> Transform:
    return Transform(
        sp.Transform(
            name="Cast",
            spec=sp.Transform.Spec(
                cast=sp.Transform.Cast(type=type.protobuf())
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def sample(fraction_size: t.Union[float, int], seed: st.Scalar) -> Transform:
    """Transform to sample from a dataspec
    - the dataset that needs to be protected as the first arg
    - a kwarg seed"""
    return Transform(
        sp.Transform(
            name="Sample",
            spec=sp.Transform.Spec(
                sample=sp.Transform.Sample(
                    size=fraction_size,
                    seed=seed.protobuf(),
                )
                if isinstance(fraction_size, int)
                else sp.Transform.Sample(
                    fraction=fraction_size, seed=seed.protobuf()
                )
            ),
            inversible=False,
            schema_preserving=False,
        )
    )


def user_settings() -> Transform:
    """Transform to create a dataspec from
    a protected one with a new schema. It should
    be called on:
    - the dataset that needs to be protected as the first arg
    - a kwarg user_type: scalar output of automatic_user_setttings"""
    return Transform(
        sp.Transform(
            name="User Settings",
            spec=sp.Transform.Spec(user_settings=sp.Transform.UserSettings()),
            inversible=False,
            schema_preserving=False,
        )
    )


def automatic_user_settings(
    max_categories: int = 200,
    batch_size_sample: int = 10000,
    max_table_size_sample: int = 200000,
    sampling_ratio: float = 0.9,
) -> Transform:
    """Transform to be called on a protected dataset
    we want to change the schema. It creates a scalar
    whose value explicits the new type of the schema.
    For big data we batch_size_sample max_table_size_sample
    and sampling_ratio are used to compue charset on a sample
    """
    return Transform(
        sp.Transform(
            name="automatic_user_settings",
            spec=sp.Transform.Spec(
                automatic_user_settings=sp.Transform.AutomaticUserSettings(
                    max_categories=max_categories,
                    batch_size_sample=batch_size_sample,
                    max_table_size_sample=max_table_size_sample,
                    sampling_ratio=sampling_ratio,
                )
            ),
            inversible=False,
            schema_preserving=False,
            properties={"creation_time": str(datetime.datetime.now())},
        )
    )


def synthetic() -> Transform:
    """Synthetic transform. This transform should be
    called on a dataset with the additional following kwargs:
    -synthetic_model: a scalar of type synthetic_model
    """
    return Transform(
        sp.Transform(
            name="Synthetic data",
            spec=sp.Transform.Spec(
                synthetic=sp.Transform.Synthetic(),
            ),
            inversible=False,
            schema_preserving=True,
        )
    )


def privacy_unit_tracking() -> Transform:
    """Transform used for PUT should be called on:
    - the dataset that needs to be PUT as the first arg
    - a kwarg privacy_unit_tracking_paths: scalar specifying the paths
     to the entities to PUT
    - a kwarg public_paths: scalar specifying the paths to
    the public tables"""
    return Transform(
        sp.Transform(
            name="Protect",
            spec=sp.Transform.Spec(
                privacy_unit_tracking=sp.Transform.PrivacyUnitTracking()
            ),
            inversible=True,
            schema_preserving=False,
        )
    )


def transcode(model_properties: t.Dict[str, t.Any]) -> st.Transform:
    raise NotImplementedError("This transform has been removed")


def inverse_transcode() -> st.Transform:
    raise NotImplementedError("This transform has been removed")


def automatic_privacy_unit_tracking_paths() -> st.Transform:
    """Transform that should be called on the dataset
    that needs to be protected, it creates a scalar whose
    value will explicit the paths to protect"""
    return Transform(
        sp.Transform(
            name="automatic_privacy_unit_tracking_paths",
            spec=sp.Transform.Spec(
                privacy_unit_tracking_paths=sp.Transform.PrivacyUnitTrackingPaths()  # noqa: E501
            ),
            properties={"creation_time": str(datetime.datetime.now())},
        )
    )


def automatic_public_paths() -> st.Transform:
    """Transform that should be called on the dataset
    that needs to be protected, it creates a scalar whose
    value will explicit the paths to public entities"""
    return Transform(
        sp.Transform(
            name="automatic_public_paths",
            spec=sp.Transform.Spec(public_paths=sp.Transform.PublicPaths()),
            properties={"creation_time": str(datetime.datetime.now())},
        )
    )


def assign_budget() -> st.Transform:
    """Transform to assign a given privacy budget to a dataset.
    It is used to specify the budget to compute the attributes
    size, bounds, marginals"""

    return Transform(
        sp.Transform(
            name="budget_assignment",
            spec=sp.Transform.Spec(assign_budget=sp.Transform.AssignBudget()),
        )
    )


def automatic_budget() -> st.Transform:
    """Transform to create a scalar specifying a budget
    automatically from the dataset it is called on.
    The rule to fix the budget is set in the corresponding
    op.
    """

    return Transform(
        sp.Transform(
            name="automatic_budget",
            spec=sp.Transform.Spec(
                automatic_budget=sp.Transform.AutomaticBudget()
            ),
        )
    )


def attributes_budget() -> st.Transform:
    """Transform to create a scalar specifying an
     epsilon,delta budget for the DP attributes of a
    dataset. It is called on a scalar specifying a
    global budget for attributes+sd."""

    return Transform(
        sp.Transform(
            name="attributes_budget",
            spec=sp.Transform.Spec(
                attribute_budget=sp.Transform.AttributesBudget()
            ),
        )
    )


def sd_budget() -> st.Transform:
    """Transform to create a scalar specifying an
     epsilon,delta budget for a synthetic dataset.
    It should be called on another scalar that specifies
    a global budget (SD+DP attributes)"""

    return Transform(
        sp.Transform(
            name="sd_budget",
            spec=sp.Transform.Spec(sd_budget=sp.Transform.SDBudget()),
        )
    )


def derive_seed(random_int: int) -> st.Transform:
    """Transform to derive a seed from a master seed"""
    return Transform(
        sp.Transform(
            name="derive_seed",
            spec=sp.Transform.Spec(
                derive_seed=sp.Transform.DeriveSeed(random_integer=random_int)
            ),
        )
    )


def group_by_pe() -> st.Transform:
    """Transform that allows to group fields
    by protected entity value. This implies that
    the dataset on which the transform is
    applied should be PUP"""
    return Transform(
        sp.Transform(
            name="group_by",
            spec=sp.Transform.Spec(group_by_pe=sp.Transform.GroupByPE()),
        )
    )


def differentiated_sample(  # type: ignore[no-untyped-def]
    fraction_size: t.Union[float, int], seed=st.Scalar
) -> Transform:
    return Transform(
        sp.Transform(
            name="DifferentiatedSample",
            spec=sp.Transform.Spec(
                differentiated_sample=sp.Transform.DifferentiatedSample(
                    size=fraction_size, seed=seed.protobuf()
                )
                if isinstance(fraction_size, int)
                else sp.Transform.DifferentiatedSample(
                    fraction=fraction_size, seed=seed.protobuf()
                )
            ),
        )
    )


def to_small_data(
    size: int, random_sampling: bool, seed: st.Scalar
) -> Transform:
    return Transform(
        sp.Transform(
            name="ToSmallData",
            spec=sp.Transform.Spec(
                to_small_data=sp.Transform.ToSmallData(
                    size=size,
                    random_sampling=random_sampling,
                    seed=seed.protobuf(),
                )
            ),
            inversible=False,
            schema_preserving=True,
        )
    )


def push_sql(
    dataconnection_name: str, schema_name: str, table_name: str, uri: str
) -> Transform:
    return Transform(
        sp.Transform(
            name="push_sql",
            spec=sp.Transform.Spec(
                push_sql=sp.Transform.PushSQL(
                    dataconnection_name=dataconnection_name,
                    schema_name=schema_name,
                    table_name=table_name,
                    uri=uri,
                )
            ),
            inversible=True,
            schema_preserving=True,
        )
    )


def handle_big_data_from_name(code_name: str) -> bool:
    """
    Check if the transform with name codename can handle bigdata in SQL.
    """
    if code_name in [
        "assign_budget",
        "differentiated_sample",
        "select_sql",
        "extract",
        "sample",
        "privacy_unit_tracking",
        "user_settings",
        "automatic_user_settings",
        "ToSmallData",
    ]:
        return True
    return False


def handle_big_data(transform: st.Transform) -> bool:
    """
    Check if the transform with name codename can handle bigdata in SQL.
    """
    return handle_big_data_from_name(transform.name())


def transform_to_small_data(
    dataspec: st.DataSpec, code_name: t.Optional[str], random_sampling: bool
) -> st.DataSpec:
    """
    Transform dataspec into small data if the following transform cannot
    handle bigdata.
    The following transform name is code_name.
    """
    manager = dataspec.manager()

    if manager.is_big_data(dataspec) and (
        code_name is None or not handle_big_data_from_name(code_name)
    ):
        status = manager.status(dataspec, task_name=BIG_DATA_TASK)
        assert status
        # This could be improved by taking the threshold in bytes,
        # measuring the size of one row and
        # guessing the numbers of rows we can fetch.
        big_data_threshold_lines = int(
            status.task(BIG_DATA_TASK).properties()[SAMPLE_SIZE_N_LINES]  # type:ignore
        )
        seed = global_context().generate_seed()
        small_dataspec = t.cast(
            st.DataSpec,
            to_small_data(
                size=big_data_threshold_lines,
                random_sampling=random_sampling,
                seed=seed,
            )(dataspec),
        )
    else:
        small_dataspec = dataspec
    return small_dataspec


def select_sql(
    query: t.Union[str, t.Dict[t.Union[str, t.Tuple[str, ...]], str]],
    dialect: t.Optional[st.SQLDialect] = None,
    op_id: st.SqlOpId = st.SqlOpId.NONE,
    sarus_default_output: t.Optional[t.Union[pa.Table, pd.DataFrame]] = None,
) -> st.Transform:
    """Transform that applies a query or a batch of aliased queries to
    a dataset.Calling .schema() or .to_arrow() on a select_sql transformed
    dataset the .sql method will be invoked and the query will be executed.
    """
    sql_dialect = (
        sp.Transform.SQLDialect.POSTGRES
        if not dialect
        else sp.Transform.SQLDialect.Value(dialect.name)
    )
    op_identifier = sp.Transform.SelectSql.OpIdentifier(
        sql_op=sp.Transform.SelectSql.OpIdentifier.SqlOp.Value(op_id.name)
    )

    if isinstance(query, str):
        select_sql = sp.Transform.SelectSql(
            query=query, sql_dialect=sql_dialect, op_identifier=op_identifier
        )
    elif len(query) == 0:
        raise ValueError(
            """Transform `SelecltSQL` must be used with
            at least one query"""
        )
    else:
        queries = {
            straight_path(
                list(
                    name
                    if isinstance(name, t.Tuple)  # type: ignore
                    else (name,)
                )
            ): qry
            for (name, qry) in query.items()
        }
        select_sql = sp.Transform.SelectSql(
            aliased_queries=sp.Transform.AliasedQueries(
                aliased_query=(
                    sp.Transform.AliasedQuery(
                        path=_path.protobuf(),
                        query=qry,
                    )
                    for (_path, qry) in queries.items()
                ),
            ),
            sql_dialect=sql_dialect,
            op_identifier=op_identifier,
        )
    transform = Transform(
        sp.Transform(
            name="select_sql",
            spec=sp.Transform.Spec(select_sql=select_sql),
            inversible=False,
            schema_preserving=False,
        )
    )
    return (
        transform
        if sarus_default_output is None
        else add_sarus_default_output(transform, sarus_default_output)
    )


def extract(
    size: int,
) -> st.Transform:
    """Transform that should be called on a dataset from which we want to
    extract some rows from according to the size parameter and a kwargs
    random_seed, a scalar that is a seed. For now, seed and size are
    ignored and iterating on the extract transformed dataset will be as
    iterating over the parent dataset.
    """
    return Transform(
        sp.Transform(
            name="extract",
            spec=sp.Transform.Spec(extract=sp.Transform.Extract(size=size)),
            inversible=False,
            schema_preserving=True,
        )
    )


def relationship_spec() -> st.Transform:
    """Transform that allows to redefine the primary and foreign keys
    of a dataset."""
    return Transform(
        sp.Transform(
            name="relationship_spec",
            spec=sp.Transform.Spec(
                relationship_spec=sp.Transform.RelationshipSpec()
            ),
        )
    )


def validated_user_type() -> st.Transform:
    """Transform that allows to set whether the user has validated
    the schema or if some types have to be changed"""
    return Transform(
        sp.Transform(
            name="validated_user_type",
            spec=sp.Transform.Spec(
                validated_user_type=sp.Transform.ValidatedUserType()
            ),
        )
    )


def error_estimation() -> st.Transform:
    """Transform that computes 95th percentile from true value"""
    return Transform(
        sp.Transform(
            name="error_estimation",
            spec=sp.Transform.Spec(
                error_estimation=sp.Transform.ErrorEstimation()
            ),
        )
    )


LORA_ATTN_MODULES = t.Literal["q_proj", "k_proj", "v_proj", "output_proj"]


def fit_model(
    batch_size: int,
    epochs: int = 1,
    text_field: t.Optional[str] = None,
    question_field: t.Optional[str] = None,
    answer_field: t.Optional[str] = None,
    quantize: bool = True,
    use_lora: bool = True,
    learning_rate: float = 1e-5,
    lora_attn_modules: t.Optional[t.List[LORA_ATTN_MODULES]] = None,
    apply_lora_to_mlp: bool = False,
    apply_lora_to_output: bool = False,
    lora_rank: int = 128,
    lora_alpha: int = 256,
) -> st.Transform:
    if quantize:
        assert (
            use_lora
        ), "Quantized models can only be finetuned with Low Rank Adaptation"

    if lora_attn_modules is None:
        lora_attn_modules = ["q_proj", "v_proj"]

    is_text_field = text_field is not None
    is_chat = question_field is not None and answer_field is not None

    if is_chat and is_text_field:
        raise ValueError(
            "Wrong arguments: you must either fill text_field or "
            "both answer_field and question_field"
        )
    if is_chat:
        question_field = t.cast(str, question_field)
        answer_field = t.cast(str, answer_field)
        return Transform(
            sp.Transform(
                name="fit_model",
                spec=sp.Transform.Spec(
                    fit_model=sp.Transform.FitModel(
                        batch_size=batch_size,
                        epochs=epochs,
                        text_kind=sp.Transform.TextKind(
                            chat=sp.Transform.Chat(
                                question_field=question_field,
                                answer_field=answer_field,
                            )
                        ),
                        use_lora=use_lora,
                        quantize=quantize,
                        learning_rate=learning_rate,
                        lora_attn_modules=lora_attn_modules,
                        apply_lora_to_mlp=apply_lora_to_mlp,
                        apply_lora_to_output=apply_lora_to_output,
                        lora_rank=lora_rank,
                        lora_alpha=lora_alpha,
                    ),
                ),
            )
        )
    if is_text_field:
        text_field = t.cast(str, text_field)
        return Transform(
            sp.Transform(
                name="fit_model",
                spec=sp.Transform.Spec(
                    fit_model=sp.Transform.FitModel(
                        batch_size=batch_size,
                        epochs=epochs,
                        text_kind=sp.Transform.TextKind(text_field=text_field),
                        use_lora=use_lora,
                        quantize=quantize,
                        learning_rate=learning_rate,
                        lora_attn_modules=lora_attn_modules,
                        apply_lora_to_mlp=apply_lora_to_mlp,
                        apply_lora_to_output=apply_lora_to_output,
                        lora_rank=lora_rank,
                        lora_alpha=lora_alpha,
                    ),
                ),
            )
        )

    raise ValueError(
        "Wrong arguments: you must either fill text_field "
        "or both answer_field and question_field"
    )


def fit_model_dp(
    batch_size: int,
    epochs: int = 1,
    l2_norm_clip: float = 1e-2,
    text_field: t.Optional[str] = None,
    question_field: t.Optional[str] = None,
    answer_field: t.Optional[str] = None,
    quantize: bool = True,
    use_lora: bool = True,
    learning_rate: float = 1e-5,
    lora_attn_modules: t.Optional[LORA_ATTN_MODULES] = None,
    apply_lora_to_mlp: bool = False,
    apply_lora_to_output: bool = False,
    lora_rank: int = 128,
    lora_alpha: int = 256,
) -> st.Transform:
    if quantize:
        assert (
            use_lora
        ), "Quantized models can only be finetuned with Low Rank Adaptation"
    if lora_attn_modules is None:
        lora_attn_modules = ["q_proj", "v_proj"]  # type:ignore

    is_text_field = text_field is not None
    is_chat = question_field is not None and answer_field is not None

    if is_chat and is_text_field:
        raise ValueError(
            "Wrong arguments: you must either fill text_field"
            " or both answer_field and question_field"
        )
    if is_chat:
        question_field = t.cast(str, question_field)
        answer_field = t.cast(str, answer_field)

        return Transform(
            sp.Transform(
                name="fit_model_dp",
                spec=sp.Transform.Spec(
                    fit_model_dp=sp.Transform.FitModelDP(
                        batch_size=batch_size,
                        l2_norm_clip=l2_norm_clip,
                        epochs=epochs,
                        text_kind=sp.Transform.TextKind(
                            chat=sp.Transform.Chat(
                                question_field=question_field,
                                answer_field=answer_field,
                            )
                        ),
                        use_lora=use_lora,
                        quantize=quantize,
                        learning_rate=learning_rate,
                        lora_attn_modules=lora_attn_modules,
                        apply_lora_to_mlp=apply_lora_to_mlp,
                        apply_lora_to_output=apply_lora_to_output,
                        lora_rank=lora_rank,
                        lora_alpha=lora_alpha,
                    ),
                ),
            )
        )
    if is_text_field:
        text_field = t.cast(str, text_field)
        return Transform(
            sp.Transform(
                name="fit_model_dp",
                spec=sp.Transform.Spec(
                    fit_model_dp=sp.Transform.FitModelDP(
                        batch_size=batch_size,
                        l2_norm_clip=l2_norm_clip,
                        epochs=epochs,
                        text_kind=sp.Transform.TextKind(text_field=text_field),
                        use_lora=use_lora,
                        quantize=quantize,
                        learning_rate=learning_rate,
                        lora_attn_modules=lora_attn_modules,
                        apply_lora_to_mlp=apply_lora_to_mlp,
                        apply_lora_to_output=apply_lora_to_output,
                        lora_rank=lora_rank,
                        lora_alpha=lora_alpha,
                    ),
                ),
            )
        )
    raise ValueError(
        "Wrong arguments: you must either fill text_field "
        "or both answer_field and question_field"
    )


def generate_from_model(
    max_new_tokens: int = 20, temperature: float = 1.0
) -> st.Transform:
    return Transform(
        sp.Transform(
            name="generate_from_model",
            spec=sp.Transform.Spec(
                generate_from_model=sp.Transform.GenerateFromModel(
                    temperature=temperature,
                    max_new_tokens=max_new_tokens,
                )
            ),
        )
    )


if t.TYPE_CHECKING:
    test_transform: st.Transform = Transform(sp.Transform())


def has_sarus_default_output(transform: st.Transform) -> bool:
    transform_proto = transform.protobuf()
    encoded_sarus_default_output = transform_proto.properties.get(
        SARUS_DEFAULT_OUTPUT, None
    )
    if encoded_sarus_default_output is not None:
        return True
    else:
        return False


def extract_sarus_default_output(transform: st.Transform) -> pa.Table:
    transform_proto = transform.protobuf()
    encoded_sarus_default_output = transform_proto.properties.get(
        SARUS_DEFAULT_OUTPUT, None
    )
    if encoded_sarus_default_output is not None:
        default_output = SarusJSONDecoder().decode(
            encoded_sarus_default_output
        )
        if isinstance(default_output, pa.Table):
            return default_output
        elif isinstance(default_output, pd.DataFrame):
            default_table = pa.Table.from_pandas(
                default_output, preserve_index=False
            )
            return default_table
        else:
            raise NotImplementedError(
                f"Type {default_output} for the default output is not supported."
            )
    else:
        raise ValueError(
            f"No sarus default output for this transform: {transform.uuid()}"
        )


def add_sarus_default_output(
    transform: st.Transform, default_output: t.Union[pa.Table, pd.DataFrame]
) -> st.Transform:
    transform_proto = transform.protobuf()
    encoded_sarus_default_output = SarusJSONEncoder().encode(default_output)
    transform_proto.properties.update(
        {SARUS_DEFAULT_OUTPUT: encoded_sarus_default_output}
    )
    return Transform(transform_proto)
