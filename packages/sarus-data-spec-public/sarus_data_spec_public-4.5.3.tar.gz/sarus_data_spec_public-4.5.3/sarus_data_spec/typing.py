"""Protocols describing common object behaviors."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum, IntEnum
import datetime as dt
import logging
import typing as t
import warnings

import numpy as np
import pandas as pd
import pyarrow as pa

from sarus_data_spec.protobuf.typing import Protobuf, ProtobufWithUUID
import sarus_data_spec.manager.typing as manager_typing
import sarus_data_spec.protobuf as sp
import sarus_data_spec.storage.typing as storage_typing

logger = logging.getLogger(__name__)

try:
    import tensorflow as tf
except ModuleNotFoundError:
    logger.warning("tensorflow not found, tensorflow datasets not available")

try:
    import sklearn  # noqa: F401
except ModuleNotFoundError:
    logger.warning("sklearn not found, sklearn models not available")

try:
    from sarus_differential_privacy.query import (
        PrivateQuery as RealPrivateQuery,
    )

    PrivateQuery = RealPrivateQuery
except ImportError:
    PrivateQuery = t.Any  # type: ignore
    warnings.warn(
        "`sarus_differential_privacy` not installed. "
        "DP primitives not available."
    )

# this is really bad but in QB actually it is not defined!
Task = t.Any

try:
    import transformers  # noqa: F401
except ImportError:
    warnings.warn("`transformers` not installed. LLM not available.")


if t.TYPE_CHECKING:
    from sklearn import svm

    DataSpecValue = t.Union[pd.DataFrame, np.ndarray, svm.SVC]
else:
    DataSpecValue = t.Any


# List of types a Dataset can be converted to
DatasetCastable = t.Union[
    pd.DataFrame,
    pd.Series,
    t.Iterator[pa.RecordBatch],
    t.AsyncIterator[pa.RecordBatch],
    pd.core.groupby.DataFrameGroupBy,
    pd.core.groupby.SeriesGroupBy,
]


P = t.TypeVar("P", bound=Protobuf, covariant=True)


@t.runtime_checkable
class HasProtobuf(t.Protocol[P]):
    """An object backed by a protocol buffer message."""

    def protobuf(self) -> P:
        """Returns the underlying protobuf object."""
        ...

    def prototype(self) -> t.Type[P]:
        """Returns the type of protobuf."""
        ...

    def type_name(self) -> str:
        """Returns the name of the type."""
        ...

    def __getitem__(self, key: str) -> str:
        """Returns the property referred by key"""
        ...

    def properties(self) -> t.Mapping[str, str]:
        """Returns the properties"""
        ...


@t.runtime_checkable
class Value(t.Protocol):
    """An object with value semantics."""

    def __bytes__(self) -> bytes: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    def __eq__(self, value: object) -> bool: ...

    def __hash__(self) -> int: ...


@t.runtime_checkable
class Frozen(t.Protocol):
    """An immutable object."""

    def _freeze(self) -> None:
        """Freeze the state of the object"""
        ...

    def _frozen(self) -> bool:
        """Check if the frozen object was left unchanged"""
        ...


PU = t.TypeVar("PU", bound=ProtobufWithUUID, covariant=True)


@t.runtime_checkable
class Referrable(HasProtobuf[PU], Frozen, t.Protocol[PU]):
    """Can be referred to by uuid."""

    def uuid(self) -> str:
        """Reference to use to refer to this object."""
        ...

    def referring(
        self, type_name: t.Optional[str] = None
    ) -> t.Collection[Referring[ProtobufWithUUID]]:
        """Referring objects pointing to this one."""
        ...

    def storage(self) -> storage_typing.Storage: ...

    def manager(self) -> manager_typing.Manager: ...


@t.runtime_checkable
class Referring(Referrable[PU], Frozen, t.Protocol[PU]):
    """Is referring to other Referrables"""

    _referred: t.MutableSet[str] = set()

    def referred(self) -> t.Collection[Referrable[ProtobufWithUUID]]:
        """Referred by this object."""
        ...

    def referred_uuid(self) -> t.Collection[str]:
        """Uuid of object referred by this object"""
        ...


FM = t.TypeVar("FM", bound=Protobuf)


@t.runtime_checkable
class Factory(t.Protocol):
    """Can produce objects from protobuf messages"""

    def register(self, name: str, type: t.Type[HasProtobuf[Protobuf]]) -> None:
        """Registers a class"""
        ...

    def create(self, message: FM, store: bool) -> HasProtobuf[FM]:
        """Returns a wrapped protobuf"""
        ...


class VariantConstraint(Referrable[sp.VariantConstraint], t.Protocol):
    def constraint_kind(self) -> ConstraintKind: ...

    def required_context(self) -> t.List[str]: ...

    def privacy_limit(self) -> t.Optional[PrivacyLimit]: ...

    def accept(self, visitor: TransformVisitor) -> None: ...


# Type alias
DS = t.TypeVar("DS", bound=t.Union[sp.Scalar, sp.Dataset])


class Attribute(Referring[sp.Attribute], t.Protocol):
    def prototype(self) -> t.Type[sp.Attribute]: ...

    def name(self) -> str: ...


@t.runtime_checkable
class DataSpec(Referring[DS], t.Protocol):
    def parents(
        self,
    ) -> t.Tuple[
        t.List[t.Union[DataSpec[DS], Transform]],
        t.Dict[str, t.Union[DataSpec[DS], Transform]],
    ]: ...

    def parents_list(
        self,
    ) -> t.List[DataSpec[DS]]: ...

    def variant(
        self,
        kind: ConstraintKind,
        public_context: t.Collection[str] = (),
        privacy_limit: t.Optional[PrivacyLimit] = None,
    ) -> t.Optional[DataSpec[DS]]: ...

    def variants(self) -> t.Collection[DataSpec]: ...

    def private_queries(self) -> t.List[PrivateQuery]:
        """Return the list of PrivateQueries used in a Dataspec's transform.

        It represents the privacy loss associated with the current computation.

        It can be used by Sarus when a user (Access object) reads a DP dataspec
        to update its accountant. Note that Private Query objects are generated
        with a random uuid so that even if they are submitted multiple times to
        an account, they are only accounted once (ask @cgastaud for more on
        accounting)."""
        ...

    def name(self) -> str: ...

    def doc(self) -> str: ...

    def is_pup(self) -> bool: ...

    def pup_token(self) -> t.Optional[str]:
        """Returns a PUP token if the dataset is PUP and None otherwise.

        The PUP token is stored in the properties of the VariantConstraint. It
        is a hash initialized with a value when the Dataset is protected.

        If a transform does not preserve the PEID then the token is set to None
        If a transform preserves the PEID assignment but changes the rows (e.g.
        sample, shuffle, filter,...) then the token's value is changed If a
        transform does not change the rows (e.g. selecting a column, adding a
        scalar,...) then the token is passed without change

        A Dataspec is PUP if its PUP token is not None. Two PUP Dataspecs are
        aligned (i.e. they have the same number of rows and all their rows have
        the same PEID) if their tokens are equal.
        """
        ...

    def rewritten_pup_token(self) -> t.Optional[str]:
        """Returns the PUP token for the DP variant of this dataspec
        during DP rewriting.

        Currently, the implementation assumes a single DP/PUP variant per
        dataspec, resulting in one possible value for
        "rewritten_pup_token."
        Future changes could introduce multiple variants, necessitating
        the implementation of priority rules.
        """
        ...

    def is_public(self) -> bool: ...

    def is_synthetic(self) -> bool:
        """Is the dataspec synthetic."""
        ...

    def is_dp(self) -> bool:
        """Is the dataspec the result of a DP transform."""
        ...

    def is_dp_writable(self) -> bool:
        """Check if it exists a variant of this dataspec
        that utilizes the dp equivalent, and this variant is is_dp."""
        ...

    def is_pup_writable(self) -> bool: ...

    def is_publishable(self) -> bool: ...

    def is_published(self) -> bool:
        """Check if the dataspec is the result of a DP transform or another
        published dataspec.
        There is at least one parent that is DP.
        Such a dataspec has at least one private query in its computation
        graph."""
        ...

    def is_transformed(self) -> bool:
        """Is the dataspec transformed."""
        ...

    def is_source(self) -> bool:
        """Is the dataspec a source dataspec."""
        ...

    def is_big_data_computable(self) -> bool:
        """Check if the dataspec can be computed if it is big data."""
        ...

    def is_remote(self) -> bool:
        """Is the dataspec a remotely defined dataset."""
        ...

    def sources(self, type_name: t.Optional[str]) -> t.Set[DataSpec]: ...

    def transform(self) -> Transform: ...

    def status(
        self, task_names: t.Optional[t.List[str]]
    ) -> t.Optional[Status]: ...

    def accept(self, visitor: Visitor) -> None: ...

    def attribute(self, name: str) -> t.Optional[Attribute]:
        """Return the attribute with the given name or None if not found."""
        ...

    def attributes(self, name: str) -> t.List[Attribute]:
        """Return all the attributes with the given name."""
        ...


class Dataset(DataSpec[sp.Dataset], t.Protocol):
    def prototype(self) -> t.Type[sp.Dataset]: ...

    def is_synthetic(self) -> bool: ...

    def has_admin_columns(self) -> bool: ...

    def is_protected(self) -> bool: ...

    def is_file(self) -> bool: ...

    def schema(self) -> Schema: ...

    async def async_schema(self) -> Schema: ...

    def size(self) -> t.Optional[Size]: ...

    def multiplicity(self) -> t.Optional[Multiplicity]: ...

    def bounds(self) -> t.Optional[Bounds]: ...

    def marginals(self) -> t.Optional[Marginals]: ...

    def to_arrow(
        self, batch_size: int = 10000
    ) -> t.Iterator[pa.RecordBatch]: ...

    async def async_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]: ...

    def to_sql(self) -> None: ...

    def push_sql(self) -> None: ...

    def spec(self) -> str: ...

    def __iter__(self) -> t.Iterator[pa.RecordBatch]: ...

    def to_pandas(self) -> pd.DataFrame: ...

    async def async_to_pandas(self) -> pd.DataFrame: ...

    def to_tensorflow(self) -> tf.data.Dataset: ...

    async def async_to_tensorflow(self) -> tf.data.Dataset: ...

    async def async_to(
        self, kind: t.Type, drop_admin: bool = True
    ) -> DatasetCastable:
        """Casts a Dataset to a Python type passed as argument."""
        ...

    def to(self, kind: t.Type, drop_admin: bool = True) -> DatasetCastable: ...

    def dot(self) -> str:
        """return a graphviz representation of the dataset"""
        ...

    def sql(
        self,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[SQLDialect] = None,
        batch_size: int = 10000,
    ) -> t.Iterator[pa.RecordBatch]:
        """Executes the sql method on the dataset"""
        ...

    def foreign_keys(self) -> t.Dict[Path, Path]:
        """returns foreign keys of the dataset"""
        ...

    def primary_keys(self) -> t.List[Path]:
        """Returns a list of the paths to all primary keys"""
        ...

    def links(self) -> Links:
        """Returns the foreign keys
        distributions of the dataset computed
        with dp"""
        ...


class Scalar(DataSpec[sp.Scalar], t.Protocol):
    def prototype(self) -> t.Type[sp.Scalar]:
        """Return the type of the underlying protobuf."""
        ...

    def is_pretrained_model(self) -> bool: ...

    def is_privacy_params(self) -> bool:
        """Is the scalar privacy parameters."""

    def is_random_seed(self) -> bool:
        """Is the scalar a random seed."""

    def is_synthetic_model(self) -> bool:
        """is the scalar a synthetic model"""

    def value(self) -> DataSpecValue: ...

    async def async_value(self) -> DataSpecValue: ...

    def spec(self) -> str: ...


class Visitor(t.Protocol):
    """A visitor class for Dataset"""

    def all(self, visited: DataSpec) -> None: ...

    def transformed(
        self,
        visited: DataSpec,
        transform: Transform,
        *arguments: DataSpec,
        **named_arguments: DataSpec,
    ) -> None: ...

    def other(self, visited: DataSpec) -> None: ...


class Bounds(Referring[sp.Bounds], t.Protocol):
    """A python abstract class to describe bounds"""

    def prototype(self) -> t.Type[sp.Bounds]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset: ...

    def statistics(self) -> Statistics: ...


class Marginals(Referring[sp.Marginals], t.Protocol):
    """A python abstract class to describe marginals"""

    def prototype(self) -> t.Type[sp.Marginals]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset: ...

    def statistics(self) -> Statistics: ...


class Size(Referring[sp.Size], t.Protocol):
    """A python abstract class to describe size"""

    def prototype(self) -> t.Type[sp.Size]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset: ...

    def statistics(self) -> Statistics: ...


class Multiplicity(Referring[sp.Multiplicity], t.Protocol):
    """A python abstract class to describe size"""

    def prototype(self) -> t.Type[sp.Multiplicity]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset: ...

    def statistics(self) -> Statistics: ...


class Schema(Referring[sp.Schema], t.Protocol):
    """A python abstract class to describe schemas"""

    def prototype(self) -> t.Type[sp.Schema]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str: ...

    def dataset(self) -> Dataset: ...

    def to_arrow(self) -> pa.Schema: ...

    def type(self) -> Type: ...

    def has_admin_columns(self) -> bool: ...

    def is_privacy_unit_tracking(self) -> bool: ...

    def tables(self) -> t.List[Path]: ...

    def privacy_unit_tracking_paths(self) -> Path: ...

    def data_type(self) -> Type: ...

    def private_tables(self) -> t.List[Path]: ...

    def public_tables(self) -> t.List[Path]: ...


class Status(Referring[sp.Status], t.Protocol):
    """A python abstract class to describe status"""

    def prototype(self) -> t.Type[sp.Status]:
        """Return the type of the underlying protobuf."""
        ...

    def dataspec(self) -> DataSpec: ...

    def datetime(self) -> dt.datetime: ...

    def update(
        self,
        task_stages: t.Optional[t.Mapping[str, Stage]],
        properties: t.Optional[t.Mapping[str, str]],
    ) -> t.Tuple[Status, bool]: ...

    def task(self, task: str) -> t.Optional[Stage]: ...

    def pending(self) -> bool: ...

    def processing(self) -> bool: ...

    def ready(self) -> bool: ...

    def error(self) -> bool: ...

    def owner(
        self,
    ) -> manager_typing.Manager:  # TODO: Maybe find a better name, but this was shadowing the actual manager of this object.  # noqa: E501
        ...

    def clear_task(self, task: str) -> t.Tuple[Status, bool]:
        """Creates a new status removing the task specified.
        If the task does not exist, nothing is created"""


class Stage(HasProtobuf[sp.Status.Stage], t.Protocol):
    def accept(self, visitor: StageVisitor) -> None: ...

    def stage(self) -> str: ...

    def ready(self) -> bool: ...

    def processing(self) -> bool: ...

    def pending(self) -> bool: ...

    def error(self) -> bool: ...


class StageVisitor(t.Protocol):
    """A visitor class for Status/Stage"""

    def pending(self) -> None: ...

    def processing(self) -> None: ...

    def ready(self) -> None: ...

    def error(self) -> None: ...


@t.runtime_checkable
class Transform(Referrable[sp.Transform], t.Protocol):
    """A python abstract class to describe transforms"""

    def prototype(self) -> t.Type[sp.Transform]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str: ...

    def doc(self) -> str: ...

    def spec(self) -> str: ...

    def is_composed(self) -> bool:
        """Is the transform composed."""
        ...

    def is_variable(self) -> bool:
        """Is the transform a variable."""
        ...

    def is_external(self) -> bool:
        """Is the transform an external operation."""
        ...

    def infer_dataset_or_scalar(
        self,
        *arguments: t.Union[DataSpec, Transform],
        **named_arguments: t.Union[DataSpec, Transform],
    ) -> t.Tuple[str, t.Callable[[DataSpec], None]]:
        """Guess if the external transform output is a Dataset or a Scalar.

        Registers schema if it is a Dataset and returns the value type.
        """
        ...

    def output_type(
        self,
    ) -> t.Optional[
        t.Literal["sarus_data_spec.Scalar", "sarus_data_spec.Dataset"]
    ]: ...

    def transforms(self) -> t.Set[Transform]:
        """return all transforms (and avoid infinite recursions/loops)"""
        ...

    def variables(self) -> t.Set[Transform]:
        """Return all the variables from a composed transform"""
        ...

    def compose(
        self,
        *compose_arguments: Transform,
        **compose_named_arguments: Transform,
    ) -> Transform: ...

    def apply(
        self,
        *apply_arguments: DataSpec,
        **apply_named_arguments: DataSpec,
    ) -> DataSpec: ...

    def abstract(
        self,
        *arguments: str,
        **named_arguments: str,
    ) -> Transform: ...

    def __call__(
        self,
        *arguments: t.Union[Transform, DataSpec, int, str],
        **named_arguments: t.Union[Transform, DataSpec, int, str],
    ) -> t.Union[Transform, DataSpec]:
        """Applies the transform to another element"""
        ...

    def __mul__(self, argument: Transform) -> Transform: ...

    def accept(self, visitor: TransformVisitor) -> None: ...

    def transform_to_apply(self) -> Transform:
        """Return the transform of a composed transform."""

    def composed_parents(
        self,
    ) -> t.Tuple[t.List[Transform], t.Dict[str, Transform]]:
        """Return the parents of a composed transform."""

    def composed_callable(self) -> t.Callable[..., t.Any]:
        """Return the composed transform's equivalent callable.

        The function takes an undefined number of named arguments.
        """


class TransformVisitor(t.Protocol):
    """A visitor class for Transform"""

    def all(self, visited: Transform) -> None: ...

    def composed(
        self,
        visited: Transform,
        transform: Transform,
        *arguments: Transform,
        **named_arguments: Transform,
    ) -> None: ...

    def variable(
        self,
        visited: Transform,
        name: str,
        position: int,
    ) -> None: ...

    def other(self, visited: Transform) -> None: ...


class Path(HasProtobuf[sp.Path], Frozen, Value, t.Protocol):
    """
    A python class to describe Paths
    A Path is essentially a tree of paths
    Each Path in the tree is a sequence of Labels
    """

    def prototype(self) -> t.Type[sp.Path]:
        """Return the type of the underlying protobuf."""
        ...

    def label(self) -> str: ...

    def sub_paths(self) -> t.List[Path]:
        """Select within self the suffix paths that have
        select_path as their prefixes
        """
        ...

    def is_empty(self) -> bool:
        """Tells if the path is empty (no label and no subpath)"""
        ...

    def has_sub_paths(self) -> bool:
        """Tells if the path has sub-paths"""
        ...

    def select(self, select_path: Path) -> t.List[Path]: ...

    def to_strings_list(self) -> t.List[t.List[str]]: ...

    def to_dict(self) -> t.Dict[str, str]: ...


class Type(HasProtobuf[sp.Type], Frozen, Value, t.Protocol):
    def prototype(self) -> t.Type[sp.Type]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str:
        """Returns the name of the underlying protobuf."""
        ...

    def data_type(self) -> Type:
        """Returns the first type level containing the data,
        hence skips the protected_entity struct if there is one"""

    def has_admin_columns(self) -> bool:
        """Return True if the Type has administrative columns."""

    def has_privacy_unit_tracking(self) -> bool:
        """Return True if the Type has protection information."""

    def structs(self: Type) -> t.Optional[t.List[Path]]:
        """Returns the path to the first level structs encountered in the
        type.
        For example, Union[Struct1,Union[Struct2[Struct3]] will return only a
        path that brings to Struct1 and Struct2.
        """
        ...

    def get(self, item: Path) -> Type:
        """Return a subtype of the considered type defined by the path."""
        ...

    def leaves(self) -> t.List[Type]:
        """Returns the leaves contained in the type tree structure"""
        ...

    def children(self) -> t.Dict[str, Type]:
        """Returns the children contained in the type tree structure"""
        ...

    # A Visitor acceptor
    def accept(self, visitor: TypeVisitor) -> None: ...

    # A new Visitor acceptor
    def accept_(self, visitor: TypeVisitor_[VisitedType]) -> VisitedType: ...

    def sub_types(self: Type, item: Path) -> t.List[Type]:
        """Returns the terminal nodes contained in the path"""
        ...

    def default(self: Type) -> pa.Array:
        """Returns an example of arrow array matching the type.
        For an optional type, it sets the default missing value.
        """

    def numpy_default(self: Type) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it sets the default missing value
        """

    def tensorflow_default(self, is_optional: bool = False) -> t.Any:
        """This methods returns a dictionary with tensors as leaves
        that match the type. For an optional type, we consider
        the case where the field is missing, and set the default value
        for each missing type.
        """

    def example(self: Type) -> pa.Array:
        """Returns an example of arrow array matching the type.
        For an optional type, it returns a non missing
        value of the type.
        """

    def numpy_example(self: Type) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it returns a non
        missing value of the type.
        """

    def tensorflow_example(self: Type) -> t.Any:
        """Returns an example of a dictionary with tensors as leaves
        that match the type..
        For an optional type, it returns a non missing value of the type.
        """

    def path_leaves(self) -> t.Sequence[Path]:
        """Returns the list of each path to a leaf in the type. If the type
        is a leaf, it returns an empty list"""


class IdBase(IntEnum):
    INT64 = 0
    INT32 = 1
    INT16 = 2
    INT8 = 3
    STRING = 4
    BYTES = 5


class DatetimeBase(IntEnum):
    INT64_NS = 0
    INT64_MS = 1
    STRING = 2


class DateBase(IntEnum):
    INT32 = 0
    STRING = 1


class TimeBase(IntEnum):
    INT64_NS = 0
    INT32_MS = 1
    STRING = 2
    INT64_US = 3


class IntegerBase(IntEnum):
    INT64 = 0
    INT32 = 1
    INT16 = 2
    INT8 = 3
    UINT64 = 4
    UINT32 = 5
    UINT16 = 6
    UINT8 = 7


class FloatBase(IntEnum):
    FLOAT64 = 0
    FLOAT32 = 1
    FLOAT16 = 2


class ConstraintKind(Enum):
    SYNTHETIC = sp.ConstraintKind.SYNTHETIC
    PUP = sp.ConstraintKind.PUP
    DP = sp.ConstraintKind.DP
    PUBLIC = sp.ConstraintKind.PUBLIC
    MOCK = sp.ConstraintKind.MOCK
    PUP_FOR_REWRITING = sp.ConstraintKind.PUP_FOR_REWRITING


class SqlOpId(Enum):
    NONE = 0
    PUP = 1
    DP = 2


class SQLDialect(Enum):
    """SQL Dialects"""

    POSTGRES = 1
    SQL_SERVER = 2
    MY_SQL = 3
    SQLLITE = 4
    ORACLE = 5
    BIG_QUERY = 6
    REDSHIFT = 7
    HIVE = 8
    DATABRICKS = 9
    MONGODB = 10


class InferredDistributionName(Enum):
    UNIFORM = "Uniform"
    NORMAL = "Normal"
    EXPONENTIAL = "Exponential"
    GAMMA = "Gamma"
    BETA = "Beta"
    PARETO = "Pareto"


class TypeVisitor(t.Protocol):
    """A visitor class for Type"""

    @abstractmethod
    def Null(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None: ...

    @abstractmethod
    def Unit(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None: ...

    @abstractmethod
    def Boolean(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None: ...

    @abstractmethod
    def Id(
        self,
        unique: bool,
        reference: t.Optional[Path] = None,
        base: t.Optional[IdBase] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Integer(
        self,
        min: int,
        max: int,
        base: IntegerBase,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Enum(
        self,
        name: str,
        name_values: t.Sequence[t.Tuple[str, int]],
        ordered: bool,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Float(
        self,
        min: float,
        max: float,
        base: FloatBase,
        possible_values: t.Iterable[float],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Text(
        self,
        encoding: str,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Bytes(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None: ...

    @abstractmethod
    def Struct(
        self,
        fields: t.Mapping[str, Type],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Union(
        self,
        fields: t.Mapping[str, Type],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Optional(
        self,
        type: Type,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def List(
        self,
        type: Type,
        max_size: int,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Array(
        self,
        type: Type,
        shape: t.Tuple[int, ...],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Datetime(
        self,
        format: str,
        min: str,
        max: str,
        base: DatetimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Time(
        self,
        format: str,
        min: str,
        max: str,
        base: TimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Date(
        self,
        format: str,
        min: str,
        max: str,
        base: DateBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Duration(
        self,
        unit: str,
        min: int,
        max: int,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Constrained(
        self,
        type: Type,
        constraint: Predicate,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Hypothesis(
        self,
        *types: t.Tuple[Type, float],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...


VisitedType = t.TypeVar("VisitedType")


class TypeVisitor_(t.Protocol, t.Generic[VisitedType]):
    """A visitor class for Type"""

    def default(self) -> VisitedType:
        """This is the minimal implementation to provide"""
        ...

    def Null(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType: ...

    def Unit(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType: ...

    def Boolean(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType: ...

    def Id(
        self,
        unique: bool,
        reference: t.Optional[Path] = None,
        base: t.Optional[IdBase] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Integer(
        self,
        min: int,
        max: int,
        base: IntegerBase,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Enum(
        self,
        name: str,
        name_values: t.Sequence[t.Tuple[str, int]],
        ordered: bool,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Float(
        self,
        min: float,
        max: float,
        base: FloatBase,
        possible_values: t.Iterable[float],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Text(
        self,
        encoding: str,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Bytes(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> VisitedType: ...

    def Struct(
        self,
        fields: t.Mapping[str, VisitedType],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Union(
        self,
        fields: t.Mapping[str, VisitedType],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Optional(
        self,
        type_: VisitedType,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def List(
        self,
        type_: VisitedType,
        max_size: int,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Array(
        self,
        type_: VisitedType,
        shape: t.Tuple[int, ...],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Datetime(
        self,
        format: str,
        min: str,
        max: str,
        base: DatetimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Time(
        self,
        format: str,
        min: str,
        max: str,
        base: TimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Date(
        self,
        format: str,
        min: str,
        max: str,
        base: DateBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Duration(
        self,
        unit: str,
        min: int,
        max: int,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Constrained(
        self,
        type_: VisitedType,
        constraint: Predicate,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...

    def Hypothesis(
        self,
        *types: t.Tuple[VisitedType, float],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> VisitedType: ...


class Predicate(HasProtobuf[sp.Predicate], Frozen, Value, t.Protocol):
    """A python class to describe types"""

    def prototype(self) -> t.Type[sp.Predicate]:
        """Return the type of the underlying protobuf."""

    # A bunch of operators
    def __or__(self, predicate: Predicate) -> Predicate:
        """Union operator"""

    def __and__(self, predicate: Predicate) -> Predicate:
        """Inter operator"""

    def __invert__(self) -> Predicate:
        """Complement"""


class Statistics(HasProtobuf[sp.Statistics], Frozen, Value, t.Protocol):
    """A python class to describe statistics"""

    def prototype(self) -> t.Type[sp.Statistics]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str: ...

    def distribution(self) -> Distribution: ...

    def size(self) -> int: ...

    def multiplicity(self) -> float: ...

    def accept(self, visitor: StatisticsVisitor) -> None: ...

    def nodes_statistics(self, path: Path) -> t.List[Statistics]:
        """Returns the List of each statistics corresponding at the leaves
        of path"""
        ...

    def children(self) -> t.Dict[str, Statistics]:
        """Returns the children contained in the type tree structure"""
        ...


class Distribution(HasProtobuf[sp.Distribution], Frozen, Value, t.Protocol):
    """A python class to describe distributions"""

    def prototype(self) -> t.Type[sp.Distribution]:
        """Return the type of the underlying protobuf."""
        ...

    def values(self) -> t.Union[t.List[float], t.List[int]]: ...

    def probabilities(self) -> t.List[float]: ...

    def names(self) -> t.Union[t.List[bool], t.List[str]]: ...

    def min_value(self) -> t.Union[int, float]: ...

    def max_value(self) -> t.Union[int, float]: ...


class StatisticsVisitor(t.Protocol):
    """A visitor class for Statistics"""

    @abstractmethod
    def Null(self, size: int, multiplicity: float) -> None: ...

    @abstractmethod
    def Unit(self, size: int, multiplicity: float) -> None: ...

    def Boolean(
        self,
        size: int,
        multiplicity: float,
        probabilities: t.Optional[t.List[float]] = None,
        names: t.Optional[t.List[bool]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Id(self, size: int, multiplicity: float) -> None: ...

    @abstractmethod
    def Integer(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Enum(
        self,
        size: int,
        multiplicity: float,
        probabilities: t.Optional[t.List[float]] = None,
        names: t.Optional[t.List[str]] = None,
        values: t.Optional[t.List[float]] = None,
        name: str = "Enum",
    ) -> None: ...

    @abstractmethod
    def Float(
        self,
        size: int,
        multiplicity: float,
        min_value: float,
        max_value: float,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[float]] = None,
    ) -> None: ...

    @abstractmethod
    def Text(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        example: str = "",
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Bytes(self, size: int, multiplicity: float) -> None: ...

    @abstractmethod
    def Struct(
        self,
        fields: t.Mapping[str, Statistics],
        size: int,
        multiplicity: float,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Union(
        self,
        fields: t.Mapping[str, Statistics],
        size: int,
        multiplicity: float,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None: ...

    @abstractmethod
    def Optional(
        self, statistics: Statistics, size: int, multiplicity: float
    ) -> None: ...

    @abstractmethod
    def List(
        self,
        statistics: Statistics,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        name: str = "List",
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Array(
        self,
        statistics: Statistics,
        size: int,
        multiplicity: float,
        min_values: t.Optional[t.List[float]] = None,
        max_values: t.Optional[t.List[float]] = None,
        name: str = "Array",
        probabilities: t.Optional[t.List[t.List[float]]] = None,
        values: t.Optional[t.List[t.List[float]]] = None,
    ) -> None: ...

    @abstractmethod
    def Datetime(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Date(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Time(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Duration(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None: ...

    @abstractmethod
    def Constrained(
        self, statistics: Statistics, size: int, multiplicity: float
    ) -> None: ...


class InferredDistribution(t.Protocol):
    """A python class to to infer user input distribution

    Attributes:
        nparams: number of parameters
    """

    nparams: int

    def estimate_params(self, x: np.ndarray) -> None:
        """estimate distribution parameters (non-DP) from data column"""
        ...

    def log_likelihood(self, x: np.ndarray) -> float:
        """compute log-likelihood of the distribution on data column"""
        ...

    def preprocess(self, x: np.ndarray) -> np.ndarray:
        """Shift/scale data to be able to estimate distribution parameters"""
        ...

    def params(self) -> t.Mapping[str, float]:
        """return distribution parameters"""
        ...


class InferredAlphabet(t.Protocol):
    """A python class to to infer user input charset

    Attributes:
        charset (t.List[int]): list with int representation of unique chars
        complexity (int): charset intervals used to generate the alphabet
            e.g. if alphabet (ascii) is [1,2,3, ..., 126] has complexity=1
            if alphabet is [1,2,3] U [10] = [1,2,3,10] has complexity=2
    """

    charset: t.List[int]
    complexity: int


T = t.TypeVar("T", covariant=True)


class Links(Referring[sp.Links], t.Protocol):
    """A python abstract class to describe all
    the links statistics in a dataset"""

    def prototype(self) -> t.Type[sp.Links]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset: ...

    def links_statistics(self) -> t.List[LinkStatistics]: ...


class LinkStatistics(HasProtobuf[sp.Links.LinkStat], t.Protocol):
    """A python class to describe the statistics of a link
    for a foreign key"""

    def prototype(self) -> t.Type[sp.Links.LinkStat]:
        """Return the type of the underlying protobuf."""
        ...

    def pointing(self) -> Path:
        """returns the path of the foreign key column"""
        ...

    def pointed(self) -> Path:
        """returns the path of the column pointed by a foreign_key"""
        ...

    def distribution(self) -> Distribution:
        """Returns the distribution of counts
        for the given pointing/pointed"""
        ...


class PrivacyLimit(t.Protocol):
    """An abstract Privacy Limit class."""

    def delta_epsilon_dict(self) -> t.Dict[float, float]:
        """Returns the limit as a dictionnary {delta: epsilon}"""
        pass


NestedQueryDict = t.MutableMapping[str, t.Union[str, "NestedQueryDict"]]
NestedTypeDict = t.MutableMapping[str, t.Union[Type, "NestedTypeDict"]]
