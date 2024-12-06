import hashlib
import logging
import typing as t

import pyarrow as pa

from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.base import (
    DatasetImplementation,
    DatasetStaticChecker,
    DataspecStaticChecker,
    ScalarImplementation,
    _ensure_batch_correct,
)

try:
    import pyqrlew as pyqrl
    from sarus_data_spec.manager.ops.sql_utils.pyqrlew_utils import (
        compose_and_translate_queries,
        compose_and_translate_query,
    )
    from sarus_data_spec.manager.ops.sql_utils.pyqrlew_utils import (
        pyqrlew_dataset,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Pyqrlew not installed. Can't process SQL queries")

from sarus_data_spec.scalar import Scalar
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class StandardDatasetStaticChecker(DatasetStaticChecker):
    def parent(self, kind: str = "dataset") -> t.Union[st.Dataset, st.Scalar]:
        return parent(self.dataset, kind=kind)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_marginals(self) -> st.Marginals:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_marginals(parent)

    def pup_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """By default we implement that the transform inherits the PUP status
        but changes the PUP token."""
        parent_dataspecs = parents(self.dataset)
        parent_dataspecs = [
            element
            for element in parent_dataspecs
            if isinstance(element, Dataset)
        ]
        if len(parent_dataspecs) > 1:
            # #TODO: we should check if all the pup_token are equals
            logger.info(
                "PUP token propagation not supported when mixing two dataspecs, setting "
                f"PUP token to None for dataspec {self.dataset.uuid()}"
            )
            return None
        parent_token = self.parent().pup_token()
        if parent_token is None:
            return None

        transform = self.dataset.transform()
        h = hashlib.md5(usedforsecurity=False)
        h.update(parent_token.encode("ascii"))
        h.update(transform.protobuf().SerializeToString())

        return h.hexdigest()

    def rewritten_pup_token(
        self, public_context: t.Collection[str]
    ) -> t.Optional[str]:
        """By default we implement that the transform inherits the PUP status
        but changes the PUP token."""
        parent_token = self.parent().rewritten_pup_token()
        if parent_token is None:
            return None

        transform = self.dataset.transform()
        h = hashlib.md5(usedforsecurity=False)
        h.update(parent_token.encode("ascii"))
        h.update(transform.protobuf().SerializeToString())

        return h.hexdigest()


class StandardDatasetImplementation(DatasetImplementation):
    """Object that executes first routing among ops between
    transformed/source and processor
    """

    def parents(self) -> t.List[t.Union[st.DataSpec, st.Transform]]:
        return parents(self.dataset)

    def parent(self, kind: str = "dataset") -> t.Union[st.Dataset, st.Scalar]:
        return parent(self.dataset, kind=kind)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind="scalar")
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)

    async def parent_size(self) -> st.Size:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_size(parent)

    async def parent_multiplicity(self) -> st.Multiplicity:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_multiplicity(parent)

    async def parent_bounds(self) -> st.Bounds:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_bounds(parent)

    async def parent_marginals(self) -> st.Marginals:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_marginals(parent)

    async def ensure_batch_correct(
        self,
        async_iterator: t.AsyncIterator[pa.RecordBatch],
        func_to_apply: t.Callable,
        batch_size: int,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Method that executes func_to_apply on each batch
        of the async_iterator but rather than directly returning
        the result, it accumulates them and returns them progressively
        so that each new batch has batch_size."""

        return _ensure_batch_correct(async_iterator, func_to_apply, batch_size)

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        """Returns a dict of queries equivalent to the current transform.
        If the the transform does not change the schema, then return None"""
        raise NotImplementedError(
            "No SQL implementation for dataset issued from"
            f" {self.dataset.transform().spec()} transform."
        )

    async def sql(
        self,
        query: t.Union[str, st.NestedQueryDict],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """It rewrites and/or composes the query and sends it to the parent."""
        queries_transform = await self.sql_implementation()
        current_schema = await self.dataset.manager().async_schema(
            self.dataset
        )
        parent_ds = t.cast(st.Dataset, self.parent(kind="dataset"))
        parent_schema = await self.parent_schema()
        if (
            queries_transform is None
            and current_schema.name() == parent_schema.name()
        ):
            parent_query = query
        else:
            assert queries_transform
            parent_pyqrl_ds = await pyqrlew_dataset(
                parent_ds, str(parent_schema)
            )
            queries_transform = {
                (current_schema.name(), *path): query
                for (path, query) in queries_transform.items()
            }
            current_pyqrl_ds = parent_pyqrl_ds.from_queries(
                list(queries_transform.items())
            )
            relations = [
                (path, pyqrl.Relation.from_query(q, parent_pyqrl_ds))
                for (path, q) in queries_transform.items()
            ]
            if isinstance(query, str):
                parent_query = compose_and_translate_query(
                    query, current_pyqrl_ds, relations
                )
            else:
                parent_query = compose_and_translate_queries(
                    query, current_pyqrl_ds, relations
                )

        logger.info(
            f"query {parent_query} sent to the "
            f"parent dataset {parent_ds.uuid()}"
        )
        return await parent_ds.manager().async_sql(
            dataset=parent_ds,
            query=parent_query,
            dialect=dialect,
            batch_size=batch_size,
            result_type=result_type,
        )


class StandardScalarStaticChecker(DataspecStaticChecker): ...


class StandardScalarImplementation(ScalarImplementation):
    def parent(self, kind: str = "dataset") -> st.DataSpec:
        return parent(self.scalar, kind=kind)

    def parents(self) -> t.List[t.Union[st.DataSpec, st.Transform]]:
        return parents(self.scalar)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind="dataset")
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind="scalar")
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)


def parent(dataspec: st.DataSpec, kind: str) -> t.Union[st.Dataset, st.Scalar]:
    pars = parents(dataspec)
    if kind == "dataset":
        parent: t.Union[t.List[Scalar], t.List[Dataset]] = [
            element for element in pars if isinstance(element, Dataset)
        ]
    else:
        parent = [element for element in pars if isinstance(element, Scalar)]
    assert len(parent) == 1
    return parent[0]


def parents(
    dataspec: st.DataSpec,
) -> t.List[t.Union[st.DataSpec, st.Transform]]:
    parents_args, parents_kwargs = dataspec.parents()
    parents_args.extend(parents_kwargs.values())
    return parents_args
