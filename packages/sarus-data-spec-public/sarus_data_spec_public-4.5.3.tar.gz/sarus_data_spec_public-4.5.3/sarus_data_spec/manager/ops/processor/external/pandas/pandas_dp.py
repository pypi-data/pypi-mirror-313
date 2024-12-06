from math import ceil
import logging
import typing as t

import numpy as np
import pandas as pd

from sarus_data_spec.constants import MAX_MAX_MULT
from sarus_data_spec.dataspec_validator.signature import SarusBoundSignature
from sarus_data_spec.protobuf.utilities import unwrap
import sarus_data_spec.typing as st

from ..external_op import (
    DEFAULT_MAX_MAX_MULT,
    ExternalOpImplementation,
    retrieve_max_mult_info_from_parent,
)

logger = logging.getLogger(__name__)

try:
    from sarus_data_spec.sarus_statistics.ops.bounds.op import BoundOp
    from sarus_data_spec.sarus_statistics.ops.corr.op import CorrOp
    from sarus_data_spec.sarus_statistics.ops.histograms.op import (
        CountOp,
        HistogramOp,
    )
    from sarus_data_spec.sarus_statistics.ops.max_multiplicity.op import (
        MaxMultiplicityOp,
    )
    from sarus_data_spec.sarus_statistics.ops.mean.op import MeanOp
    from sarus_data_spec.sarus_statistics.ops.median.op import MedianOp
    from sarus_data_spec.sarus_statistics.ops.std.op import StdOp
    from sarus_data_spec.sarus_statistics.ops.sum.op import SumOp
    from sarus_data_spec.sarus_statistics.protobuf.multiplicity_pb2 import (
        MultiplicityParameters,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus_data_spec.sarus_statistics" not in str(e_pandas_dp):
        raise

try:
    from sarus_differential_privacy.query import ComposedPrivateQuery
except ModuleNotFoundError as e_pandas_dp:
    if "sarus_differential_privacy" not in str(e_pandas_dp):
        raise

try:
    from sarus_data_spec.sarus_query_builder.builders.bounds_builder import (
        simple_bounds_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.composed_builder import (
        ComposedBuilder,
        simple_composed_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.corr_builder import (
        corr_builder as simple_corr_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.max_multiplicity_builder import (  # noqa : E501
        simple_max_multiplicity_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.mean_builder import (
        mean_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.median_builder import (
        median_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.standard_mechanisms_builder import (  # noqa : E501
        laplace_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.std_builder import (
        std_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.sum_builder import (
        sum_builder,
    )
    from sarus_data_spec.sarus_query_builder.core.core import (
        OptimizableQueryBuilder,
    )
    from sarus_data_spec.sarus_query_builder.protobuf.query_pb2 import (
        GenericTask,
        Query,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus" not in str(e_pandas_dp):
        raise
    OptimizableQueryBuilder = t.Any  # type: ignore


NUMERIC_TYPES = ("integer", "float", "boolean")


class pd_shape_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_SHAPE_DP"
    _non_dp_equivalent_id = "pandas.PD_SHAPE"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        return True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        single_builder = laplace_builder(
            parent_ds,
            Query(laplace_mechanism=Query.LaplaceMechanism()),
        )
        return builder_from_multiplicity(
            single_builder, max_mult, max_max_mult
        )

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        """Return the PrivateQueries summarizing DP characteristics."""
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        if isinstance(query, ComposedPrivateQuery):
            return list(query.all_subqueries()), tasks
        else:
            return [query], tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        """Implementation of DP shape.

        A DP implementation receives additional arguments compared to a
        standard external implementation:
            - `budget`: a list of sp.Scalar.PrivacyParams.Point
                object containing each an epsilon and a delta values
            - `seed`: an integer used to parametrize random number generators
            - `pe`: the protected entity used by
            `sarus_data_spec.sarus_statistics`primitives
        """
        # Evaluate arguments
        parent_ds = signature.static_kwargs()["this"]
        (dataframe, budget, seed) = await signature.collect_args()

        # Get QB task parametrization
        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget[0].epsilon
        shape = dataframe.shape
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        random_generator = np.random.default_rng(abs(seed))
        max_mul, shape_task = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )
        assert len(shape_task) == 1
        n_rows = CountOp(
            parent_ds,
            noise=shape_task[0].parameters["noise"],
        ).value(None, max_mul, random_generator)

        dp_shape = (n_rows, *shape[1:])
        return dp_shape


class pd_sum_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_SUM_DP"
    _non_dp_equivalent_id = "pandas.PD_SUM"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return (axis == 0 or axis is None) and (numeric_only is True)

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        column_bounds_sum_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    sum_builder(parent_ds, Query(sum=Query.Sum())),
                ],
            )
        )
        n_cols = len(parent_schema.data_type().children())
        single_builder = simple_composed_builder(
            parent_ds, n_cols * [column_bounds_sum_builder]
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        return builder_from_multiplicity(
            single_builder, max_mult, max_max_mult
        )

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )
        sum_dp_dict = {}
        schema_fields = parent_schema.data_type().children()
        for tasks_column, (column_name, column_type) in zip(
            unwrapped_other_tasks, (schema_fields.items())
        ):
            bounds_parameters, sum_parameters = (
                t.cast(GenericTask, unwrap(tasks_column.subtasks[0])),
                t.cast(GenericTask, unwrap(tasks_column.subtasks[0])),
            )
            type_pb = column_type.protobuf()
            if type_pb.WhichOneof("type") == "optional":
                if not skipna:
                    sum_dp_dict[column_name] = np.nan
                    continue
                type_pb = type_pb.optional.type
            if type_pb.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            # TODO parent_ds doesn't have a size
            # if parent_ds.size().children()[column_name].size()
            #  < min_count:
            #     sum_dp_dict[column_name] = np.nan
            #     continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            sum_op = SumOp(
                parent_ds,
                sum_parameters.parameters["noise"],
            )
            sum_dp_dict[column_name] = sum_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            sum_dp = pd.Series(sum_dp_dict)
        else:
            sum_dp = list(sum_dp_dict.values()).pop()

        return sum_dp


class pd_mean_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEAN_DP"
    _non_dp_equivalent_id = "pandas.PD_MEAN"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return (axis == 0) and (numeric_only is True)

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        n_cols = len(parent_schema.data_type().children())
        column_bounds_mean_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    mean_builder(parent_ds, Query(mean=Query.Mean())),
                ],
            )
        )
        builder = simple_composed_builder(
            parent_ds,
            n_cols * [column_bounds_mean_builder],
        )
        return builder_from_multiplicity(builder, max_mult, max_max_mult)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )
        mean_dp_dict = {}
        schema_fields = parent_schema.data_type().children()
        for tasks_column, (column_name, column_type) in zip(
            unwrapped_other_tasks, (schema_fields.items())
        ):
            bounds_parameters, mean_parameters = (
                t.cast(GenericTask, unwrap(tasks_column.subtasks[0])),
                t.cast(GenericTask, unwrap(tasks_column.subtasks[1])),
            )

            type_pb = column_type.protobuf()
            if type_pb.WhichOneof("type") == "optional":
                if not skipna:
                    mean_dp_dict[column_name] = np.nan
                    continue
                type_pb = type_pb.optional.type
            if type_pb.WhichOneof("type") not in NUMERIC_TYPES:
                continue
            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            mean_op = MeanOp(
                parent_ds,
                mean_parameters.parameters["noise"],
            )
            mean_dp_dict[column_name] = mean_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            mean_dp = pd.Series(mean_dp_dict)
        else:
            mean_dp = list(mean_dp_dict.values()).pop()

        return mean_dp


class pd_median_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEDIAN_DP"
    _non_dp_equivalent_id = "pandas.PD_MEDIAN"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return axis == 0 and numeric_only is True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        n_cols = len(parent_schema.data_type().children())
        column_bounds_median_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    median_builder(parent_ds, Query(median=Query.Median())),
                ],
            )
        )
        builder = simple_composed_builder(
            parent_ds,
            n_cols * [column_bounds_median_builder],
        )
        return builder_from_multiplicity(builder, max_mult, max_max_mult)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        epsilon = budget_value[0].epsilon

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )

        median_dp_dict = {}
        schema_fields = parent_schema.data_type().children()
        for tasks_column, (column_name, column_type) in zip(
            unwrapped_other_tasks, (schema_fields.items())
        ):
            bounds_parameters, median_parameters = (
                t.cast(GenericTask, unwrap(tasks_column.subtasks[0])),
                t.cast(GenericTask, unwrap(tasks_column.subtasks[1])),
            )
            type_pb = column_type.protobuf()
            if type_pb.WhichOneof("type") == "optional":
                if not skipna:
                    median_dp_dict[column_name] = np.nan
                    continue
                type_pb = type_pb.optional.type

            if type_pb.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            median_op = MedianOp(
                parent_ds,
                median_parameters.parameters["noise"],
            )
            median_dp_dict[column_name] = median_op.value(
                column_name, max_mul, bounds, random_generator
            )
        if signature["this"].python_type() == str(pd.DataFrame):
            median_dp = pd.Series(median_dp_dict)
        else:
            median_dp = list(median_dp_dict.values()).pop()

        return median_dp


class pd_std_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_STD_DP"
    _non_dp_equivalent_id = "pandas.PD_STD"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return axis == 0 and numeric_only is True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        n_cols = len(parent_schema.data_type().children())
        column_bounds_std_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    std_builder(parent_ds, Query(std=Query.Std())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            n_cols * [column_bounds_std_builder],
        )
        return builder_from_multiplicity(builder, max_mult, max_max_mult)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        epsilon = budget_value[0].epsilon
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )

        std_dp_dict = {}
        schema_fields = parent_schema.data_type().children()
        for tasks_column, (column_name, column_type) in zip(
            unwrapped_other_tasks, (schema_fields.items())
        ):
            bounds_parameters, std_parameters = (
                t.cast(GenericTask, unwrap(tasks_column.subtasks[0])),
                t.cast(GenericTask, unwrap(tasks_column.subtasks[0])),
            )
            type_pb = column_type.protobuf()
            if type_pb.HasField("optional"):
                if not skipna:
                    std_dp_dict[column_name] = np.nan
                    continue
                type_pb = type_pb.optional.type
            if type_pb.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            std_op = StdOp(
                parent_ds,
                std_parameters.parameters["noise_mean"],
                std_parameters.parameters["noise_square"],
                std_parameters.parameters["noise_count"],
            )
            std_dp_dict[column_name] = std_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            std_dp = pd.Series(std_dp_dict)
        else:
            std_dp = list(std_dp_dict.values()).pop()

        return std_dp


class pd_count_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_COUNT_DP"
    _non_dp_equivalent_id = "pandas.PD_COUNT"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        axis = signature["axis"].static_value()
        return bool(axis == 0)

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()

        parent_schema = await parent_ds.manager().async_schema(parent_ds)

        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        n_cols = len(parent_schema.data_type().children())
        column_counts_builder = laplace_builder(
            parent_ds, Query(laplace_mechanism=Query.LaplaceMechanism())
        )
        builder = simple_composed_builder(
            parent_ds, n_cols * [column_counts_builder]
        )
        return builder_from_multiplicity(builder, max_mult, max_max_mult)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )
        count_dp_dict = {}

        schema_fields = parent_schema.data_type().children()
        for count_parameter, column_name in zip(
            unwrapped_other_tasks, (schema_fields.keys())
        ):
            count_dp_dict[column_name] = CountOp(
                parent_ds,
                count_parameter.parameters["noise"],
            ).value(column_name, max_mul, random_generator)

        if signature["this"].python_type() == str(pd.DataFrame):
            count_dp = pd.Series(count_dp_dict)
        else:
            count_dp = list(count_dp_dict.values()).pop()
        return count_dp


class pd_value_counts_dp(ExternalOpImplementation):
    _transform_id: str = "pandas.PD_VALUE_COUNTS_DP"
    _non_dp_equivalent_id = "pandas.PD_VALUE_COUNTS"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        return signature["this"].python_type() == str(pd.Series)

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        n_cols = len(parent_schema.data_type().children())
        column_counts_builder = laplace_builder(
            parent_ds, Query(laplace_mechanism=Query.LaplaceMechanism())
        )
        builder = simple_composed_builder(
            parent_ds, n_cols * [column_counts_builder]
        )
        return builder_from_multiplicity(builder, max_mult, max_max_mult)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        """Return the PrivateQueries summarizing DP characteristics."""
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        """Implementation of DP shape.

        A DP implementation receives additional arguments compared to a
        standard external implementation:
            - `budget`: a list of sp.Scalar.PrivacyParams.Point
                object containing each an epsilon and a delta values
            - `seed`: an integer used to parametrize random number generators
            - `pe`: the protected entity used by
            `sarus_data_spec.sarus_statistics` primitives
        """
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        sort = await signature["sort"].collect()
        ascending = await signature["ascending"].collect()
        normalize = await signature["normalize"].collect()
        dropna = await signature["dropna"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))
        parent_schema = parent_ds.schema()
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )

        count_dp_dict = {}
        schema_fields = parent_schema.data_type().children()
        for count_parameters, column_name in zip(
            unwrapped_other_tasks, (schema_fields.keys())
        ):
            histogram = t.cast(
                t.Dict[str, float],
                HistogramOp(
                    parent_ds,
                    noise=count_parameters.parameters["noise"],
                    sort=sort,
                    ascending=ascending,
                    normalize=normalize,
                    dropna=dropna,
                ).value(column_name, max_mul, random_generator),
            )
            count_dp_dict[column_name] = histogram

        # for now only on series
        values = list(count_dp_dict.values())[0]
        name = list(count_dp_dict.keys())[0]
        # added to be conform to its expected schema
        count_dp = pd.Series(data=values, name=name)
        return count_dp


class pd_corr_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_CORR_DP"
    _non_dp_equivalent_id = "pandas.PD_CORR"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """
        `numeric_only` is `True`
        DataFrame
        `method = Pearson`
        `min_periods = 1`
        """
        method = signature["method"].static_value()
        min_periods = signature["min_periods"].static_value()
        is_dataframe = bool(
            signature["this"].python_type() == str(pd.DataFrame)
        )
        return is_dataframe and (min_periods == 1) and (method == "pearson")

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        corr_builder: OptimizableQueryBuilder = simple_corr_builder(
            parent_ds, Query(covariance=Query.Covariance())
        )

        return builder_from_multiplicity(corr_builder, max_mult, max_max_mult)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        epsilon, delta = await get_budget(signature)
        builder = await self.query_builder(signature=signature)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = t.cast(ComposedPrivateQuery, builder.private_query(tasks))
        if isinstance(query, ComposedPrivateQuery):
            return list(query.all_subqueries()), tasks
        else:
            return [query], tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        epsilon = budget_value[0].epsilon
        # Compute DP value
        random_generator = np.random.default_rng(abs(seed_value))
        parent_schema = parent_ds.schema()
        max_mult = await retrieve_max_mult_info_from_parent(
            parent_ds, parent_schema
        )
        max_mul, unwrapped_other_tasks = retrieve_or_compute_max_mult(
            max_mult, tasks, parent_ds, random_generator, epsilon
        )
        assert len(unwrapped_other_tasks) == 1
        corr_dp = CorrOp(
            parent_ds,
            unwrapped_other_tasks[0].parameters["epsilon"],
            unwrapped_other_tasks[0].parameters["dims"],
        ).value(max_mul, random_generator=random_generator)

        return corr_dp


async def get_budget(signature: SarusBoundSignature) -> t.Tuple[float, float]:
    """Retrieve (epsilon, delta) from signature"""
    budget = await signature["budget"].collect()
    if len(budget) != 1:
        raise NotImplementedError(
            "The PrivacyParams contains more than 1 point in the privacy "
            "profile."
        )

    epsilon = budget[0].epsilon
    delta = budget[0].delta
    if epsilon == 0.0:
        raise ValueError("`epsilon` should be greater than 0.")

    return epsilon, delta


def builder_from_multiplicity(
    builder: OptimizableQueryBuilder, max_mult: str, max_max_mult: int
) -> OptimizableQueryBuilder:
    """Adds a builder from multiplicity if the max_mult is empty"""

    if max_mult != "":
        # in this case no need to recompute it
        return builder
    max_mult_builder = simple_max_multiplicity_builder(
        builder.dataset,
        Query(
            max_multiplicity=Query.MaxMultiplicity(
                max_max_multiplicity=max_max_mult
            )
        ),
    )
    # need to recompute it, take MAX_MAX_MULT as bound
    if isinstance(builder, ComposedBuilder):
        builder._builders.insert(0, max_mult_builder)  # type:ignore
        builder._weights.insert(0, 1)  # type:ignore
    else:
        builder = simple_composed_builder(
            builder.dataset,
            [max_mult_builder, builder],
        )
    return builder


def retrieve_or_compute_max_mult(
    max_mult: str,
    tasks: st.Task,
    parent_ds: st.Dataset,
    random_generator: np.random.Generator,
    epsilon: float,
) -> t.Tuple[int, t.List[st.Task]]:
    """Either retrieves the max_mult if it is not an empty string or computes it
    using the tasks"""

    if max_mult == "":
        # there is no pre-computed max_multiplicity so we need
        # to recompute it
        unwrapped = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, unwrapped_other_tasks = (
            t.cast(MultiplicityParameters, unwrapped[0]),
            t.cast(t.List[GenericTask], unwrapped[1:]),
        )
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.compute.noise_user_count,
            max_mult_task.compute.noise_multiplicity,
            max_mult_task.compute.max_max_multiplicity,
        ).value(random_generator)
    else:
        max_mul = float(max_mult)
        if hasattr(tasks, "subtasks"):
            unwrapped_other_tasks = t.cast(
                t.List[GenericTask],
                [unwrap(subtask) for subtask in tasks.subtasks],
            )  # for type compatibility mainly
        else:
            unwrapped_other_tasks = [tasks]
    return ceil(max_mul), unwrapped_other_tasks
