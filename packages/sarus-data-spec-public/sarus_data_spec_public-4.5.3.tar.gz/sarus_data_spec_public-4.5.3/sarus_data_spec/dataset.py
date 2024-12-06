from __future__ import annotations

from os.path import basename
from typing import (
    TYPE_CHECKING,
    AsyncIterator,
    Collection,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)
from urllib.parse import urlparse
import json
import typing as t
import warnings

import pandas as pd
import pyarrow as pa

try:
    import tensorflow as tf
except ModuleNotFoundError:
    pass  # Warning is displayed by typing.py

try:
    from sqlalchemy.engine import make_url
except ModuleNotFoundError:
    warnings.warn("SqlAlchemy not found, sql operations not available")


from sarus_data_spec.base import Referring
from sarus_data_spec.constants import DATASET_SLUGNAME, PROMPT
from sarus_data_spec.protobuf.utilities import to_base64
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.transform import Transform, external
import sarus_data_spec.protobuf as sp
import sarus_data_spec.transform as sdtr
import sarus_data_spec.typing as st

if TYPE_CHECKING:
    from sarus_data_spec.bounds import Bounds
    from sarus_data_spec.links import Links
    from sarus_data_spec.marginals import Marginals
    from sarus_data_spec.multiplicity import Multiplicity
    from sarus_data_spec.size import Size


class Dataset(Referring[sp.Dataset]):
    """A python class to describe datasets"""

    def __init__(self, protobuf: sp.Dataset, store: bool = True) -> None:
        if protobuf.spec.HasField("transformed"):
            transformed = protobuf.spec.transformed
            self._referred = {
                transformed.transform,
                *transformed.arguments,
                *list(transformed.named_arguments.values()),
            }

        super().__init__(protobuf=protobuf, store=store)

    def prototype(self) -> Type[sp.Dataset]:
        """Return the type of the underlying protobuf."""
        return sp.Dataset

    def name(self) -> str:
        return self._protobuf.name

    def doc(self) -> str:
        return self._protobuf.doc

    def is_transformed(self) -> bool:
        """Is the dataset composed."""
        return self._protobuf.spec.HasField("transformed")

    def is_file(self) -> bool:
        """Is the dataset composed."""
        return self._protobuf.spec.HasField("file")

    def is_synthetic(self) -> bool:
        """Is the dataset synthetic."""
        return self.manager().dataspec_validator().is_synthetic(self)

    def has_admin_columns(self) -> bool:
        return self.schema().has_admin_columns()

    def is_protected(self) -> bool:
        return self.schema().is_privacy_unit_tracking()

    def is_pup(self) -> bool:
        """Is the dataset PUP."""
        return self.pup_token() is not None

    def pup_token(self) -> Optional[str]:
        """Returns the dataset PUP token."""
        return self.manager().dataspec_validator().pup_token(self)

    def rewritten_pup_token(self) -> Optional[str]:
        """Returns the PUP token for the DP variant of this dataspec
        during DP rewriting.

        Currently, the implementation assumes a single DP/PUP variant per
        dataspec, resulting in one possible value for
        "rewritten_pup_token."
        Future changes could introduce multiple variants, necessitating
        the implementation of priority rules.
        """
        return self.manager().dataspec_validator().rewritten_pup_token(self)

    def is_dp(self) -> bool:
        """Is the dataspec the result of a DP transform"""
        return self.manager().dataspec_validator().is_dp(self)

    def is_public(self) -> bool:
        """Is the dataset public."""
        return self.manager().dataspec_validator().is_public(self)

    def is_dp_writable(self) -> bool:
        """Check if there exists a variant of this dataspec
        that utilizes the dp equivalent, and this variant is is_dp."""
        return self.manager().dataspec_validator().is_dp_writable(self)

    def is_pup_writable(self) -> bool:
        """Check if there exists a variant of this dataspec that is is_pup.
        The dataspec is is_pup_writable if it has a non-None
        rewritten_pup_token."""
        return self.manager().dataspec_validator().is_pup_writable(self)

    def is_publishable(self) -> bool:
        """Check if there exists a variant of this dataspec that is
        published."""
        return self.manager().dataspec_validator().is_publishable(self)

    def is_published(self) -> bool:
        """Check if the dataspec is the result of a DP transform or another
        published dataspec.
        There is at least one parent that is DP.
        Such a dataspec has at least one private query in its computation
        graph."""
        return self.manager().dataspec_validator().is_published(self)

    def is_remote(self) -> bool:
        """Is the dataspec a remotely defined dataset."""
        return self.manager().is_remote(self)

    def is_source(self) -> bool:
        """Is the dataset not composed."""
        return not self.is_transformed()

    def is_big_data_computable(self) -> bool:
        return self.manager().dataspec_validator().is_big_data_computable(self)

    def sql(
        self,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
    ) -> Iterator[pa.RecordBatch]:
        """Executes the sql method on the dataset"""
        return self.manager().sql(self, query, dialect, batch_size)

    def sources(
        self, type_name: t.Optional[str] = sp.type_name(sp.Dataset)
    ) -> Set[st.DataSpec]:
        """Returns the set of non-transformed datasets that are parents
        of the current dataset"""
        sources = self.storage().sources(self, type_name=type_name)
        return sources

    def status(
        self, task_names: t.Optional[t.List[str]] = None
    ) -> t.Optional[st.Status]:
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

    def schema(self) -> st.Schema:
        return self.manager().schema(self)

    async def async_schema(self) -> st.Schema:
        return await self.manager().async_schema(self)

    def size(self) -> t.Optional[Size]:
        return cast("Size", self.manager().size(self))

    def multiplicity(self) -> t.Optional[Multiplicity]:
        return cast("Multiplicity", self.manager().multiplicity(self))

    def bounds(self) -> t.Optional[Bounds]:
        return cast("Bounds", self.manager().bounds(self))

    def marginals(self) -> t.Optional[Marginals]:
        return cast("Marginals", self.manager().marginals(self))

    def links(self) -> st.Links:
        return cast("Links", self.manager().links(self))

    def transform(self) -> st.Transform:
        return cast(
            st.Transform,
            self.storage().referrable(
                self.protobuf().spec.transformed.transform
            ),
        )

    def to_arrow(self, batch_size: int = 10000) -> t.Iterator[pa.RecordBatch]:
        return self.manager().to_arrow(self, batch_size)

    async def async_to_arrow(
        self, batch_size: int = 10000
    ) -> AsyncIterator[pa.RecordBatch]:
        return await self.manager().async_to_arrow(self, batch_size)

    def to_sql(self) -> None:
        return self.manager().to_sql(self)

    def push_sql(self) -> None:
        return self.manager().push_sql(self)

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
        accounting).
        """
        return self.manager().dataspec_validator().private_queries(self)

    def spec(self) -> str:
        return cast(str, self._protobuf.spec.WhichOneof("spec"))

    def __iter__(self) -> Iterator[pa.RecordBatch]:
        return self.to_arrow(batch_size=1)

    def to_pandas(self) -> pd.DataFrame:
        return self.manager().to_pandas(self)

    async def async_to_pandas(self) -> pd.DataFrame:
        return await self.manager().async_to_pandas(self)

    async def async_to(
        self, kind: t.Type, drop_admin: bool = True
    ) -> st.DatasetCastable:
        """Convert a Dataset's to a Python type."""
        return await self.manager().async_to(self, kind, drop_admin)

    def to(self, kind: t.Type, drop_admin: bool = True) -> st.DatasetCastable:
        return self.manager().to(self, kind, drop_admin)

    def to_tensorflow(self) -> tf.data.Dataset:
        return self.manager().to_tensorflow(self)

    async def async_to_tensorflow(self) -> tf.data.Dataset:
        return await self.manager().async_to_tensorflow(self)

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
                    cast(Dataset, self.storage().referrable(arg))
                    for arg in self._protobuf.spec.transformed.arguments
                ),
                **{
                    name: cast(Dataset, self.storage().referrable(arg))
                    for name, arg in self._protobuf.spec.transformed.named_arguments.items()  # noqa: E501
                },
            )
        else:
            visitor.other(self)

    def foreign_keys(self) -> Dict[st.Path, st.Path]:
        """returns foreign keys of the dataset"""
        return self.manager().foreign_keys(self)

    def dot(self) -> str:
        """return a graphviz representation of the dataset"""

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

    def primary_keys(self) -> List[st.Path]:
        return self.manager().primary_keys(self)

    def attribute(self, name: str) -> t.Optional[st.Attribute]:
        return self.manager().attribute(name=name, dataspec=self)

    def attributes(self, name: str) -> t.List[st.Attribute]:
        return self.manager().attributes(name=name, dataspec=self)


# Builders
def transformed(
    transform: st.Transform,
    *arguments: t.Union[st.DataSpec, st.Transform],
    dataspec_type: Optional[str] = None,
    dataspec_name: Optional[str] = None,
    **named_arguments: t.Union[st.DataSpec, st.Transform],
) -> st.DataSpec:
    attach_info_callback = None

    if dataspec_type is None:
        transform_type = transform.output_type()
        if transform_type is not None:
            dataspec_type = transform_type
        else:
            dataspec_type, attach_info_callback = (
                transform.infer_dataset_or_scalar(
                    *arguments, **named_arguments
                )
            )

    if dataspec_name is None:
        dataspec_name = "Transformed"

    if dataspec_type == sp.type_name(sp.Scalar):
        output_dataspec: st.DataSpec = Scalar(
            sp.Scalar(
                name=dataspec_name,
                spec=sp.Scalar.Spec(
                    transformed=sp.Scalar.Transformed(
                        transform=transform.uuid(),
                        arguments=(a.uuid() for a in arguments),
                        named_arguments={
                            n: a.uuid() for n, a in named_arguments.items()
                        },
                    )
                ),
            )
        )
    else:
        properties = {}
        ds_args = [
            element
            for element in arguments
            if element.type_name() == sp.type_name(sp.Dataset)
        ]
        for element in named_arguments.values():
            if element.type_name() == sp.type_name(sp.Dataset):
                ds_args.append(element)
        if len(ds_args) == 1 and DATASET_SLUGNAME in ds_args[0].properties():
            properties[DATASET_SLUGNAME] = arguments[0].properties()[
                DATASET_SLUGNAME
            ]

        output_dataspec = Dataset(
            sp.Dataset(
                name=dataspec_name,
                spec=sp.Dataset.Spec(
                    transformed=sp.Dataset.Transformed(
                        transform=transform.uuid(),
                        arguments=(a.uuid() for a in arguments),
                        named_arguments={
                            n: a.uuid() for n, a in named_arguments.items()
                        },
                    )
                ),
                properties=properties,
            )
        )

    # Add additional information to the newly created Dataspec
    # (e.g. a mock variant)
    if attach_info_callback is not None:
        attach_info_callback(output_dataspec)
    return output_dataspec


def file(
    format: str,
    uri: str,
    doc: str = "A file dataset",
    properties: Optional[Mapping[str, str]] = None,
) -> Dataset:
    return Dataset(
        sp.Dataset(
            name=basename(urlparse(uri).path),
            doc=doc,
            spec=sp.Dataset.Spec(file=sp.Dataset.File(format=format, uri=uri)),
            properties=properties,
        )
    )


def csv_file(
    uri: str,
    doc: str = "A csv file dataset",
    properties: Optional[Mapping[str, str]] = None,
) -> Dataset:
    return Dataset(
        sp.Dataset(
            name=basename(urlparse(uri).path),
            doc=doc,
            spec=sp.Dataset.Spec(file=sp.Dataset.File(format="csv", uri=uri)),
            properties=properties,
        )
    )


def files(
    name: str,
    format: str,
    uri_pattern: str,
    doc: str = "Dataset split into files",
    properties: Optional[Mapping[str, str]] = None,
) -> Dataset:
    return Dataset(
        sp.Dataset(
            name=name,
            doc=doc,
            spec=sp.Dataset.Spec(
                files=sp.Dataset.Files(format=format, uri_pattern=uri_pattern)
            ),
            properties=properties,
        )
    )


def csv_files(
    name: str,
    uri_pattern: str,
    doc: str = "A csv file dataset",
    properties: Optional[Mapping[str, str]] = None,
) -> Dataset:
    return Dataset(
        sp.Dataset(
            name=name,
            doc=doc,
            spec=sp.Dataset.Spec(
                files=sp.Dataset.Files(format="csv", uri_pattern=uri_pattern)
            ),
            properties=properties,
        )
    )


def sql(
    uri: str,
    tables: Optional[
        Collection[Tuple[str, str]]
    ] = None,  # pairs schema/table_name
    properties: Optional[Mapping[str, str]] = None,
) -> Dataset:
    parsed_uri = make_url(uri)
    if parsed_uri.database is None:
        name = f"{parsed_uri.drivername}_db_dataset"
    else:
        name = parsed_uri.database
    if tables is None:
        tables = []
    return Dataset(
        sp.Dataset(
            name=name,
            doc=f"Data from {uri}",
            spec=sp.Dataset.Spec(
                sql=sp.Dataset.Sql(
                    uri=uri,
                    tables=[
                        sp.Dataset.Sql.Table(
                            schema=element[0], table=element[1]
                        )
                        for element in tables
                    ],
                )
            ),
            properties=properties,
        )
    )


def mapped_sql(
    uri: str,
    mapping_sql: Mapping[st.Path, st.Path],
    schemas: Optional[Collection[str]] = None,
) -> Dataset:
    parsed_uri = make_url(uri)
    if parsed_uri.database is None:
        name = f"{parsed_uri.drivername}_db_dataset"
    else:
        name = parsed_uri.database

    serialized_mapping = json.dumps(
        {
            to_base64(original_table.protobuf()): to_base64(
                synthetic_table.protobuf()
            )
            for original_table, synthetic_table in mapping_sql.items()
        }
    )
    properties = {"sql_mapping": serialized_mapping}
    return Dataset(
        sp.Dataset(
            name=name,
            doc=f"Data from {uri}",
            spec=sp.Dataset.Spec(
                sql=sp.Dataset.Sql(
                    uri=uri,
                )
            ),
            properties=properties,
        )
    )


def make_prompts(prompts: List[str]) -> st.Dataset:
    return t.cast(
        st.Dataset,
        external(
            id="pandas.PD_DATAFRAME",
            py_kwargs={"data": {PROMPT: prompts}},
        )(),
    )


def huggingface(name: str, split: str) -> st.Dataset:
    return Dataset(
        sp.Dataset(
            name=name,
            doc="Dataset from Huggingface hub",
            spec=sp.Dataset.Spec(
                huggingface=sp.Dataset.Huggingface(name=name, split=split)
            ),
        )
    )


if t.TYPE_CHECKING:
    test_sql: st.Dataset = sql(uri="sqlite:///:memory:")
    test_file: st.Dataset = file(format="", uri="")
    test_csv_file: st.Dataset = csv_file(uri="")
    test_files: st.Dataset = files(name="", uri_pattern="", format="")
    test_csv_files: st.Dataset = csv_files(name="", uri_pattern="")
    test_transformed: st.DataSpec = transformed(
        sdtr.privacy_unit_tracking(), sql(uri="sqlite:///:memory:")
    )
