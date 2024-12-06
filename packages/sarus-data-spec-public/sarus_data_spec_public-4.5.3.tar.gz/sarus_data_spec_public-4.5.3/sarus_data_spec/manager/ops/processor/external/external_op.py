from __future__ import annotations

import hashlib
import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.arrow.admin_utils import (
    compute_admin_data,
    create_admin_columns,
    merge_data_and_admin,
)
from sarus_data_spec.arrow.array import fit_array_to_schema_type_async_gen
from sarus_data_spec.arrow.conversion import to_pyarrow_table
from sarus_data_spec.arrow.schema import type_from_arrow_schema
from sarus_data_spec.manager.ops.processor.utils_ops import (
    ensure_batch_correct_and_not_empty,
)
from sarus_data_spec.constants import (
    MAX_MAX_MULT,
    MULTIPLICITY,
)
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.dataspec_validator.signature import (
    SarusBoundSignature,
    SarusSignature,
    SarusSignatureValue,
)
from sarus_data_spec.dataspec_validator.typing import PUPKind
from sarus_data_spec.manager.async_utils import async_iter
from sarus_data_spec.manager.ops.base import (
    DatasetImplementation,
    DatasetStaticChecker,
    DataspecStaticChecker,
    ScalarImplementation,
)
from sarus_data_spec.schema import schema as schema_builder
from sarus_data_spec.size import size as size_builder
from sarus_data_spec.transform import external, transform_id
import sarus_data_spec.protobuf as sp
import sarus_data_spec.statistics as sds
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st

from .typing import NO_TRANSFORM_ID
from .utils import static_arguments

try:
    from sarus_data_spec.sarus_query_builder.core.core import (
        OptimizableQueryBuilder,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus" not in str(e_pandas_dp):
        raise

DEFAULT_MAX_MAX_MULT = "1000.0"


class ExternalScalarStaticChecker(DataspecStaticChecker):
    async def private_queries(self) -> t.List[st.PrivateQuery]:
        """Return the PrivateQueries summarizing DP characteristics."""
        implementation = external_implementation(self.dataspec.transform())
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )
        return await implementation.private_queries(bound_signature)

    def is_dp(self) -> bool:
        """Checks if the transform is DP and compatible with the arguments."""
        implementation = external_implementation(self.dataspec.transform())
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )
        return implementation.is_dp(bound_signature)

    def is_dp_able(self) -> bool:
        """Checks if the dataspec has a transform that either has a DP
        equivalent, allowing the rewritten dataspec to be considered DP
        if the input rewritten PUP token is not None."""
        if self.is_dp():
            return True

        transform = self.dataspec.transform()
        implementation = external_implementation(transform)
        dp_implementation = implementation.dp_equivalent()
        if dp_implementation is None:
            return False
        else:
            bound_signature = implementation.signature().bind_dataspec(
                self.dataspec
            )
            return dp_implementation.is_dp(bound_signature)

    def is_dp_writable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PUP arguments are PUP and aligned
            (i.e. same PUP token)
            - other dataspecs arguments are public
        """
        transform = self.dataspec.transform()
        implementation = external_implementation(transform)
        dp_implementation = implementation.dp_equivalent()
        if dp_implementation is None:
            return False
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )
        if not dp_implementation.is_dp(bound_signature):
            return False

        return bound_signature.rewritten_pup_token() is not None

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        transform = self.dataspec.transform()
        op_implementation = external_implementation(transform)
        py_args, py_kwargs, ds_args_pos, ds_types = static_arguments(transform)

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return None

        dp_transform_id = dp_implementation.transform_id()
        assert dp_transform_id is not None

        # Types won't be used since budget & seed are scalars
        ds_types["budget"] = ""
        ds_types["seed"] = ""

        return external(
            dp_transform_id,
            py_args=py_args,
            py_kwargs=py_kwargs,
            ds_args_pos=ds_args_pos,
            ds_types=ds_types,
        )

    def pup_transform(self) -> t.Optional[st.Transform]:
        transform = self.dataspec.transform()
        pup_implementation = pup_external_implementation(self.dataspec)
        if pup_implementation is None:
            return None
        py_args, py_kwargs, ds_args_pos, ds_types = static_arguments(transform)
        dp_transform_id = pup_implementation.transform_id()
        assert dp_transform_id is not None
        return external(
            dp_transform_id,
            py_args=py_args,
            py_kwargs=py_kwargs,
            ds_args_pos=ds_args_pos,
            ds_types=ds_types,
        )

    async def query_builder(self) -> OptimizableQueryBuilder:
        transform = self.dataspec.transform()
        implementation = external_implementation(transform)

        dp_implementation = (
            implementation
            if implementation.is_dp_equivalent()
            else implementation.dp_equivalent()
        )
        if dp_implementation is None:
            raise ValueError(
                """The dataspec does not have a dp equivalent,
                thus it does not have a query builder"""
            )
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )
        return await dp_implementation.query_builder(bound_signature)


class ExternalDatasetStaticChecker(
    ExternalScalarStaticChecker, DatasetStaticChecker
):
    def __init__(self, dataset: st.Dataset):
        super().__init__(dataset)
        self.dataset = dataset

    def pup_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """Return the dataspec's PUP token."""
        transform = self.dataspec.transform()
        implementation = external_implementation(transform)
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )

        input_token = bound_signature.pup_token()
        if input_token is None:
            return None

        pup_kind = implementation.pup_kind(bound_signature)
        if pup_kind == PUPKind.NOT_PUP:
            return None
        elif pup_kind == PUPKind.TOKEN_PRESERVING:
            return input_token
        else:  # PUP or ROW
            h = hashlib.md5(usedforsecurity=False)
            h.update(input_token.encode("ascii"))
            h.update(transform.protobuf().SerializeToString())
            new_token = h.hexdigest()
            return new_token

    def rewritten_pup_token(
        self, public_context: t.Collection[str]
    ) -> t.Optional[str]:
        transform = self.dataspec.transform()
        implementation = pup_external_implementation(self.dataspec)
        if implementation is None:
            return None
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )

        input_token = bound_signature.rewritten_pup_token()
        if input_token is None:
            return None

        pup_kind = implementation.pup_kind(bound_signature)
        if pup_kind == PUPKind.NOT_PUP:
            return None
        elif pup_kind == PUPKind.TOKEN_PRESERVING:
            return input_token
        else:  # PUP or ROW
            h = hashlib.md5(usedforsecurity=False)
            h.update(input_token.encode("ascii"))
            h.update(transform.protobuf().SerializeToString())
            new_token = h.hexdigest()
            return new_token

    def is_pup_able(self) -> bool:
        """Checks if the dataspec has a transform that either has a PUP
        equivalent or does not require one, allowing the rewritten dataspec to
        be considered 'PUP' if the input rewritten PUP token is not None."""
        implementation = pup_external_implementation(self.dataspec)
        if implementation is None:
            return False
        # probably not needed
        bound_signature = implementation.signature().bind_dataspec(
            self.dataspec
        )

        pup_kind = implementation.pup_kind(bound_signature)
        return not pup_kind == PUPKind.NOT_PUP

    async def schema(self) -> st.Schema:
        """Computes the schema of the dataspec.

        The schema is computed by computing the synthetic data value and
        converting the Pyarrow schema to a Sarus schema.q
        """
        syn_variant = self.dataset.variant(kind=st.ConstraintKind.SYNTHETIC)
        assert syn_variant is not None
        assert syn_variant.prototype() == sp.Dataset

        syn_dataset = t.cast(st.Dataset, syn_variant)
        arrow_iterator = await compute_external_to_arrow(
            syn_dataset, batch_size=1000
        )
        first_batch = await arrow_iterator.__anext__()
        schema = first_batch.schema

        schema_type = type_from_arrow_schema(schema)

        # retrieve max_mul from parent
        parents_args, parents_kwargs = self.dataset.parents()
        parents_args.extend(parents_kwargs.values())
        parents_args = [el for el in parents_args if isinstance(el, Dataset)]
        if len(parents_args) > 1 or len(parents_args) == 0:
            max_mult = ""  # we cannot infer max_mult in this case
            max_max_mult = DEFAULT_MAX_MAX_MULT
        else:
            parent_ds = t.cast(st.Dataset, parents_args[0])
            parent_schema = await self.dataset.manager().async_schema(
                parent_ds
            )
            max_mult = await retrieve_max_mult_info_from_parent(
                parent_ds=parent_ds, parent_schema=parent_schema
            )
            max_max_mult = parent_schema.properties().get(
                MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
            )
        properties = {}
        if self.dataset.is_pup():
            # If the dataset is PUP then the schema of the real data should
            # have protection but the synthetic data might not have it. We
            # need to add it manually.
            schema_type = sdt.protected_type(schema_type)
            # now take care of multiplicity
            implementation = external_implementation(self.dataset.transform())
            bound_signature = implementation.signature().bind_dataspec(
                self.dataset
            )
            pup_kind = implementation.pup_kind(bound_signature)
            if pup_kind == PUPKind.TOKEN_PRESERVING:
                if max_mult != "":
                    properties[MULTIPLICITY] = max_mult
                    properties[MAX_MAX_MULT] = max_mult
                else:
                    properties[MAX_MAX_MULT] = max_max_mult

            else:
                # in this case, rows are not preserved,
                # so the max multiplicity might change,
                # we take as bound the older one, this is
                # an approximation and may cause bias
                # if the dataset rows increase
                properties = {
                    MAX_MAX_MULT: max_mult if max_mult != "" else max_max_mult
                }
        else:
            properties = {}
        return schema_builder(
            self.dataset, schema_type=schema_type, properties=properties
        )


class ExternalDatasetOp(DatasetImplementation):
    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        batches_async_it = await compute_external_to_arrow(
            self.dataset, batch_size
        )
        schema = await self.dataset.async_schema()
        # make sure the arrow array is conform to its schema.
        return fit_array_to_schema_type_async_gen(
            batches_async_it, schema.type()
        )

    async def size(self) -> st.Size:
        implementation = external_implementation(self.dataset.transform())
        bound_signature = implementation.signature().bind_dataspec(
            self.dataset
        )
        pup_kind = implementation.pup_kind(bound_signature)
        if pup_kind == PUPKind.TOKEN_PRESERVING or pup_kind == PUPKind.PUP:
            syn_variant = self.dataset.variant(
                kind=st.ConstraintKind.SYNTHETIC
            )
            assert syn_variant is not None
            syn_variant = t.cast(Dataset, syn_variant)
            import warnings

            warnings.warn(
                "Using hack to compute sizes of dataset with synthetic variant"
            )
            size = len(
                await syn_variant.manager().async_to_pandas(syn_variant)
            )
            return size_builder(
                dataset=self.dataset,
                statistics=sds.Struct(fields={}, multiplicity=1.0, size=size),
            )
        else:
            raise NotImplementedError(
                f"Size not implemented for transform"
                f" {self.dataset.transform().spec()}"
            )


class ExternalScalarOp(ScalarImplementation):
    async def value(self) -> t.Any:
        transform = self.scalar.transform()
        ds_args, ds_kwargs = self.scalar.parents()
        return await async_compute_external_value(
            transform, *ds_args, **ds_kwargs
        )


async def async_compute_external_value(
    transform: st.Transform,
    *ds_args: t.Union[st.DataSpec, st.Transform],
    **ds_kwargs: t.Union[st.DataSpec, st.Transform],
) -> t.Any:
    """Compute the value of an external transform applied on Dataspecs.

    This function computes the output value without manipulating the
    corresponding Dataspec. This is useful when we need to have access
    to the value of a Dataspec before its creation:
      - for computing a Mock value and inferring if the result is
        a Scalar or a Dataset.
    """
    implementation = external_implementation(transform)
    bound_signature = implementation.signature().bind(
        transform, *ds_args, **ds_kwargs
    )
    bound_signature.static_validation()
    data = await implementation.compute(bound_signature)
    return data


class ExternalOpImplementation:
    """External PUP op implementation class.

    This class wraps together several elements of an external op
    implementation:
        - `call` is the function that computes the output value from the
          input(s) value(s).
    """

    _transform_id: str = NO_TRANSFORM_ID
    _dp_equivalent_id: t.Optional[str] = None
    _non_dp_equivalent_id: t.Optional[str] = None
    _pup_equivalent_id: t.Optional[str] = None
    _non_pup_equivalent_id: t.Optional[str] = None
    _signature: t.Optional[SarusSignature] = None

    def transform_id(self) -> str:
        return self._transform_id

    def dp_equivalent_id(self) -> t.Optional[str]:
        return self._dp_equivalent_id

    def is_dp_equivalent(self) -> bool:
        return self._non_dp_equivalent_id is not None

    def dp_equivalent(self) -> t.Optional[ExternalOpImplementation]:
        if not self._dp_equivalent_id:
            return None

        return external_implementation_from_id(self._dp_equivalent_id)

    def pup_equivalent(self) -> t.Optional[ExternalOpImplementation]:
        if not self._pup_equivalent_id:
            return None

        return external_implementation_from_id(self._pup_equivalent_id)

    def signature(self) -> SarusSignature:
        if self._signature is not None:
            return self._signature

        if self._non_dp_equivalent_id is None:
            raise ValueError(
                f"External implementation {self.transform_id()} has no "
                "signature defined and no non-DP equivalent."
            )

        non_dp_signature = external_implementation_from_id(
            self._non_dp_equivalent_id
        ).signature()
        return non_dp_signature.make_dp()

    async def compute(self, bound_signature: SarusBoundSignature) -> t.Any:
        if self.is_dp(bound_signature):
            return await self.call_dp(bound_signature)
        else:
            signature_value = await bound_signature.collect_signature_value()
            return self.call(signature_value)

    def call(self, signature_value: SarusSignatureValue) -> t.Any:
        raise NotImplementedError

    async def call_dp(self, bound_signature: SarusBoundSignature) -> t.Any:
        """DP ops `call` need to be async to compute schema, tasks, etc"""
        raise NotImplementedError

    def pup_kind(self, bound_signature: SarusBoundSignature) -> PUPKind:
        """Return the PUP properties of the transform.

        It takes the transform arguments as input because it can depend on some
        transform parameters. For instance, it is not PUP if we are aggregating
        the rows (axis=0) and it is PUP if we are aggregating the columns
        (axis=1).
        """
        # Default implementation
        return PUPKind.NOT_PUP

    def is_dp(self, bound_signature: SarusBoundSignature) -> bool:
        """Return True if the DP transform is compatible with the arguments.

        It takes the transform arguments as input because it can depend on some
        transform parameters. For instance, if we are aggregating the rows
        (axis=0), then there might be an equivalent DP transform but if we are
        aggregating the columns there might not (axis=1).
        """
        # Default implementation
        return False

    async def private_queries(
        self, signature: SarusBoundSignature
    ) -> t.List[st.PrivateQuery]:
        """Takes as input the args of the transform (static and dynamic)."""
        if not signature.is_dp():
            return []
        queries, _ = await self.private_queries_and_task(signature)
        return queries

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        raise NotImplementedError

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        raise NotImplementedError

    def callable(
        self, composed_transform: st.Transform
    ) -> t.Callable[..., t.Awaitable[t.Any]]:
        """Build the transform's async callable.

        The function takes an undefined number of named arguments.

        It first collects the current transform's signature concrete values
        using the passed variables' values. The concrete values are stored in a
        SarusBoundSignature object so we can compute the current transform's
        output by simply using the implementation's `call` method.
        """
        lambda_signature = self.signature().bind_composed(composed_transform)
        previous_callable = lambda_signature.callable()

        def composed_callable(*vars: t.Any, **kwvars: t.Any) -> t.Any:
            signature_value = previous_callable(*vars, **kwvars)
            return self.call(signature_value)

        return composed_callable

    def py_output_hint(
        self,
        transform: st.Transform,
        *arguments: t.Union[st.DataSpec, st.Transform],
        **named_arguments: t.Union[st.DataSpec, st.Transform],
    ) -> t.Optional[str]:
        """May return a hint on the output's Python type.

        It returns an empty string by default."""
        return None


def external_implementation(
    transform: st.Transform,
) -> ExternalOpImplementation:
    """Return the implementation of an external op from a DataSpec.

    The mapping is done by the config file.
    """
    assert transform and transform.is_external()
    id = transform_id(transform)
    return external_implementation_from_id(id)


def pup_external_implementation(
    dataspec: st.DataSpec,
) -> t.Optional[ExternalOpImplementation]:
    transform = dataspec.transform()
    implementation = external_implementation(transform)
    bound_signature = implementation.signature().bind_dataspec(dataspec)
    pup_kind = implementation.pup_kind(bound_signature)
    if not pup_kind == PUPKind.NOT_PUP:
        return implementation
    else:
        pup_implementation = implementation.pup_equivalent()
        if pup_implementation is None:
            return None
        else:
            pup_kind = pup_implementation.pup_kind(bound_signature)
            if pup_kind == PUPKind.NOT_PUP:
                return None
            else:
                return pup_implementation


def external_implementation_from_id(id: str) -> ExternalOpImplementation:
    # Imported here to avoid circular imports
    from . import ROUTING

    library, op_name = id.split(".")
    op_implementation = t.cast(
        ExternalOpImplementation, ROUTING[library][op_name]
    )
    return op_implementation


async def retrieve_max_mult_info_from_parent(
    parent_ds: st.Dataset, parent_schema: st.Schema
) -> str:
    """If the dataset is transformed by an external the max_mult
    lies in the schema while for standard transforms we can derive
     the multiplicity from the parent directly"""
    if not parent_ds.is_transformed():
        return ""
    if parent_ds.transform().is_external():
        max_mult = parent_schema.properties().get(MULTIPLICITY, "")
    else:
        try:
            max_mult = str(
                (await parent_ds.manager().async_multiplicity(parent_ds))
                .statistics()
                .multiplicity()
            )
        except Exception:
            # this is for the mock, not very nice
            max_mult = ""
    return max_mult


async def compute_external_to_arrow(
    dataset: st.Dataset, batch_size: int
) -> t.AsyncIterator[pa.RecordBatch]:
    """It computes arrow record batches of a dataset from the external op implementation"""
    transform = dataset.transform()
    implementation = external_implementation(transform)
    bound_signature = implementation.signature().bind_dataspec(dataset)
    bound_signature.static_validation()

    if dataset.is_pup():
        result = await implementation.compute(bound_signature)
        if (
            isinstance(result, pd.Series)
            and implementation.pup_kind(bound_signature) == PUPKind.ROW
        ):
            # Reformat the series as a dataframe with a single row
            result = result.to_frame().transpose()
        ds_result = t.cast(st.DatasetCastable, result)
        admin_data = await bound_signature.admin_data()
        output_admin_data = compute_admin_data(admin_data, ds_result)
        data_table = to_pyarrow_table(ds_result)
        table = merge_data_and_admin(data_table, output_admin_data)

    else:
        result = await implementation.compute(bound_signature)
        data_table = to_pyarrow_table(result)
        table = create_admin_columns(data_table)

    async_iterator = async_iter(table.to_batches(max_chunksize=batch_size))
    return await ensure_batch_correct_and_not_empty(
        dataset, async_iterator, batch_size
    )
