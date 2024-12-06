from math import ceil
from typing import Union
import logging
import typing as t

import numpy as np
import pandas as pd

from sarus_data_spec.constants import MAX_MAX_MULT
from sarus_data_spec.dataspec_validator.signature import SarusBoundSignature
from sarus_data_spec.manager.ops.processor.external.pandas.pandas_dp import (
    get_budget,
)
from sarus_data_spec.protobuf.utilities import unwrap
import sarus_data_spec.typing as st

from ..external_op import DEFAULT_MAX_MAX_MULT, ExternalOpImplementation

GroupBy = Union[
    pd.core.groupby.DataFrameGroupBy,
    pd.core.groupby.SeriesGroupBy,
]

logger = logging.getLogger(__name__)

try:
    from sarus_data_spec.sarus_statistics.ops.bounds.op import BoundOp
    from sarus_data_spec.sarus_statistics.ops.histograms.op import (
        GroupByCountOp,
    )
    from sarus_data_spec.sarus_statistics.ops.max_multiplicity.op import (
        MaxMultiplicityOp,
    )
    from sarus_data_spec.sarus_statistics.ops.mean.op import GroupByMeanOp
    from sarus_data_spec.sarus_statistics.ops.median.op import GroupbyMedianOp
    from sarus_data_spec.sarus_statistics.ops.std.op import GroupByStdOp
    from sarus_data_spec.sarus_statistics.ops.sum.op import GroupBySumOp
    from sarus_data_spec.sarus_statistics.ops.tau_thresholding.op import (
        TauThresholdingOp,
    )
except ModuleNotFoundError as e_groupby_dp:
    if "sarus_data_spec.sarus_statistics" not in str(e_groupby_dp):
        raise

try:
    from sarus_differential_privacy.query import ComposedPrivateQuery
except ModuleNotFoundError as e_groupby_dp:
    if "sarus_differential_privacy" not in str(e_groupby_dp):
        raise

try:
    from sarus_data_spec.sarus_query_builder.builders.bounds_builder import (
        simple_bounds_builder,
    )
    from sarus_data_spec.sarus_query_builder.builders.composed_builder import (
        simple_composed_builder,
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
    from sarus_data_spec.sarus_query_builder.builders.tau_thresholding_builder import (  # noqa : E501
        tau_threshold_builder_delta,
    )
    from sarus_data_spec.sarus_query_builder.core.core import (
        OptimizableQueryBuilder,
    )
    from sarus_data_spec.sarus_query_builder.protobuf.query_pb2 import (
        GenericTask,
        Query,
    )
except ModuleNotFoundError as e_groupby_dp:
    if "sarus" not in str(e_groupby_dp):
        raise
    OptimizableQueryBuilder = t.Any  # type: ignore

NUMERIC_TYPES = ("integer", "float", "boolean")

DEFAULT_DELTA = 0.01


def has_budget(signature: SarusBoundSignature) -> bool:
    """Retrieve (epsilon, delta) from signature"""
    return "budget" in signature


def compute_tau_thresholding(
    parent_ds: st.Dataset,
    tau_thresholding_task: st.Task,
    keys_name: t.List[t.Any],
    max_mul: float,
    random_generator: np.random.Generator,
) -> t.List[t.Any]:
    dataset_above_tau_threshold = TauThresholdingOp(
        parent_ds,
        tau_thresholding_task.parameters["epsilon_tau_thresholding"],
        tau_thresholding_task.parameters["delta_tau_thresholding"],
    ).value(keys_name, max_mul, random_generator)
    keys_values = list(dataset_above_tau_threshold.index)
    if len(keys_values) == 0:
        raise ValueError(
            "Found no keys for the groupby, this may be due to an insufficient budget"
        )
    return keys_values


class pd_count_groupby_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_COUNT_GROUPBY_DP"
    _non_dp_equivalent_id = "pandas.PD_COUNT_GROUPBY"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        return True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        if "budget" in signature:
            _, delta = await get_budget(signature)
        else:
            delta = DEFAULT_DELTA
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )

        n_cols = len(parent_schema.data_type().children())

        # add tau thresholding
        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_counts_builder = laplace_builder(
            parent_ds, Query(laplace_mechanism=Query.LaplaceMechanism())
        )

        # tau thresholding builder
        tau_builder = tau_threshold_builder_delta(parent_ds, delta)

        builders_list: t.List[OptimizableQueryBuilder] = [
            max_mult_builder,
            tau_builder,
        ]
        builders_list.extend(n_cols * [column_counts_builder])

        # add another builder
        builder = simple_composed_builder(parent_ds, builders_list)
        return builder

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
        dataframegroupby: pd.core.groupby.DataFrameGroupBy = (
            await parent_ds.async_to(pd.core.groupby.DataFrameGroupBy)
        )
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, tau_thresholding_task, shape_task = (
            tasks[0],
            tasks[1],
            tasks[2:],
        )

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))

        # Compute DP value

        # we supposed: if max_mult_task has no compute then max mult is 1
        if max_mult_task.HasField("compute"):
            max_mul = MaxMultiplicityOp(
                parent_ds,
                epsilon,  # parameter for quantiles
                max_mult_task.compute.noise_user_count,
                max_mult_task.compute.noise_multiplicity,
                max_mult_task.compute.max_max_multiplicity,
            ).value(random_generator)
        else:
            max_mul = 1

        # keys values from synthetic data
        # syn_parent = parent_ds.variant(st.ConstraintKind.SYNTHETIC)
        # dataframegroupby_synth = await
        # syn_parent.async_to(pd.core.groupby.DataFrameGroupBy)
        # keys_values = [key for key,_ in dataframegroupby_synth]

        # keys values from tau thresholding
        # work with only one index name for the group by
        keys_name = dataframegroupby.keys
        keys_values = compute_tau_thresholding(
            parent_ds,
            tau_thresholding_task,
            keys_name,
            max_mul,
            random_generator,
        )

        dataframes_with_counts = {}
        for index, column_name in enumerate(dataframegroupby.nth(0).columns):
            count_parameters = shape_task[index]
            dataframes_with_counts[column_name] = GroupByCountOp(
                parent_ds,
                count_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator, keys_values)

        for col_name, df in dataframes_with_counts.items():
            df.columns = [col_name]

        if len(dataframes_with_counts.keys()) == 1:
            return list(dataframes_with_counts.values())[0]
        else:
            return pd.concat(dataframes_with_counts.values(), axis=1)


class pd_mean_groupby_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEAN_GROUPBY_DP"
    _non_dp_equivalent_id = "pandas.PD_MEAN_GROUPBY"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`numeric_only` is `True`"""
        numeric_only = signature["numeric_only"].static_value()
        return numeric_only is True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        if "budget" in signature:
            _, delta = await get_budget(signature)
        else:
            delta = DEFAULT_DELTA

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
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
        tau_builder = tau_threshold_builder_delta(parent_ds, delta)
        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder, tau_builder]
            + n_cols * [column_bounds_mean_builder],
        )
        return builder

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
        dataframegroupby: pd.core.groupby.DataFrameGroupBy = (
            await parent_ds.async_to(pd.core.groupby.DataFrameGroupBy)
        )
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        tasks = [unwrap(subtask) for subtask in tasks.subtasks]

        max_mult_task, tau_thresholding_task, mean_tasks = (
            tasks[0],
            tasks[1],
            tasks[2:],
        )

        # Compute DP value
        random_generator = np.random.default_rng(abs(seed_value))
        epsilon = budget_value[0].epsilon

        # we supposed: if max_mult_task has no compute then max mult is 1
        if max_mult_task.HasField("compute"):
            max_mul = MaxMultiplicityOp(
                parent_ds,
                epsilon,  # parameter for quantiles
                max_mult_task.compute.noise_user_count,
                max_mult_task.compute.noise_multiplicity,
                max_mult_task.compute.max_max_multiplicity,
            ).value(random_generator)
        else:
            max_mul = 1

        keys_name = dataframegroupby.keys

        keys_values = compute_tau_thresholding(
            parent_ds,
            tau_thresholding_task,
            keys_name,
            max_mul,
            random_generator,
        )

        dataframes_with_dp_means = {}
        for index, column_name in enumerate(dataframegroupby.nth(0).columns):
            subtasks = [unwrap(task) for task in mean_tasks[index].subtasks]

            bounds_parameters, mean_parameters = (
                t.cast(GenericTask, subtasks[0]),
                t.cast(GenericTask, subtasks[1]),
            )
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof("type") == "optional":
                dataframes_with_dp_means[column_name] = dataframegroupby.apply(
                    lambda x: np.nan
                ).to_frame(name="Mean")
                continue
            if column_type.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            mean_op = GroupByMeanOp(
                parent_ds,
                mean_parameters.parameters["noise"],
            )
            dataframes_with_dp_means[column_name] = mean_op.value(
                column_name, max_mul, bounds, random_generator, keys_values
            )

        for col_name, df in dataframes_with_dp_means.items():
            df.columns = [col_name]

        if len(dataframes_with_dp_means.keys()) == 1:
            return list(dataframes_with_dp_means.values())[0]
        else:
            return pd.concat(dataframes_with_dp_means.values(), axis=1)


class pd_median_groupby_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEDIAN_GROUPBY_DP"
    _non_dp_equivalent_id = "pandas.PD_MEDIAN_GROUPBY"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`numeric_only` is `True`"""
        numeric_only = signature["numeric_only"].static_value()
        return numeric_only is True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        if "budget" in signature:
            _, delta = await get_budget(signature)
        else:
            delta = DEFAULT_DELTA
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        tau_builder = tau_threshold_builder_delta(parent_ds, delta)

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
            [max_mult_builder, tau_builder]
            + n_cols * [column_bounds_median_builder],
        )
        return builder

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
        dataframegroupby: pd.core.groupby.DataFrameGroupBy = (
            await parent_ds.async_to(pd.core.groupby.DataFrameGroupBy)
        )
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, tau_thresholding_task, median_tasks = (
            tasks[0],
            tasks[1],
            tasks[2:],
        )

        random_generator = np.random.default_rng(abs(seed_value))
        epsilon = budget_value[0].epsilon

        # Compute DP value

        # we supposed: if max_mult_task has no compute then max mult is 1
        if max_mult_task.HasField("compute"):
            max_mul = MaxMultiplicityOp(
                parent_ds,
                epsilon,  # parameter for quantiles
                max_mult_task.compute.noise_user_count,
                max_mult_task.compute.noise_multiplicity,
                max_mult_task.compute.max_max_multiplicity,
            ).value(random_generator)
        else:
            max_mul = 1

        keys_name = dataframegroupby.keys

        keys_values = compute_tau_thresholding(
            parent_ds,
            tau_thresholding_task,
            keys_name,
            max_mul,
            random_generator,
        )

        dataframes_with_dp_median = {}
        for index, column_name in enumerate(dataframegroupby.nth(0).columns):
            subtasks = [unwrap(task) for task in median_tasks[index].subtasks]
            bounds_parameters, median_parameters = (
                t.cast(GenericTask, subtasks[0]),
                t.cast(GenericTask, subtasks[1]),
            )
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof("type") == "optional":
                dataframes_with_dp_median[column_name] = (
                    dataframegroupby.apply(
                        lambda x: np.nan
                    ).to_frame(name="Median")
                )
                continue
            if column_type.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            median_op = GroupbyMedianOp(
                parent_ds,
                median_parameters.parameters["noise"],
            )
            dataframes_with_dp_median[column_name] = median_op.value(
                column_name, max_mul, bounds, random_generator, keys_values
            )

        for col_name, df in dataframes_with_dp_median.items():
            df.columns = [col_name]

        if len(dataframes_with_dp_median.keys()) == 1:
            return list(dataframes_with_dp_median.values())[0]
        else:
            return pd.concat(dataframes_with_dp_median.values(), axis=1)


class pd_std_groupby_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_STD_GROUPBY_DP"
    _non_dp_equivalent_id = "pandas.PD_STD_GROUPBY"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        return True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        if "budget" in signature:
            _, delta = await get_budget(signature)
        else:
            delta = DEFAULT_DELTA
        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )

        tau_builder = tau_threshold_builder_delta(parent_ds, delta)

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
            [max_mult_builder, tau_builder]
            + n_cols * [column_bounds_std_builder],
        )
        return builder

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
        dataframegroupby: pd.core.groupby.DataFrameGroupBy = (
            await parent_ds.async_to(pd.core.groupby.DataFrameGroupBy)
        )
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]

        max_mult_task, tau_thresholding_task, std_tasks = (
            tasks[0],
            tasks[1],
            tasks[2:],
        )

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))

        # Compute DP value

        # we supposed: if max_mult_task has no compute then max mult is 1
        if max_mult_task.HasField("compute"):
            max_mul = MaxMultiplicityOp(
                parent_ds,
                epsilon,  # parameter for quantiles
                max_mult_task.compute.noise_user_count,
                max_mult_task.compute.noise_multiplicity,
                max_mult_task.compute.max_max_multiplicity,
            ).value(random_generator)
        else:
            max_mul = 1

        keys_name = dataframegroupby.keys
        keys_values = compute_tau_thresholding(
            parent_ds,
            tau_thresholding_task,
            keys_name,
            max_mul,
            random_generator,
        )

        dataframes_with_dp_std = {}
        for index, column_name in enumerate(dataframegroupby.nth(0).columns):
            subtasks = [unwrap(task) for task in std_tasks[index].subtasks]
            bounds_parameters, std_parameters = (
                t.cast(GenericTask, subtasks[0]),
                t.cast(GenericTask, subtasks[1]),
            )
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof("type") == "optional":
                dataframes_with_dp_std[column_name] = dataframegroupby.apply(
                    lambda x: np.nan
                ).to_frame(name="Std")
                continue
            if column_type.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            std_op = GroupByStdOp(
                parent_ds,
                std_parameters.parameters["noise_mean"],
                std_parameters.parameters["noise_square"],
                std_parameters.parameters["noise_count"],
            )
            dataframes_with_dp_std[column_name] = std_op.value(
                column_name, max_mul, bounds, random_generator, keys_values
            )

        for col_name, df in dataframes_with_dp_std.items():
            df.columns = [col_name]

        if len(dataframes_with_dp_std.keys()) == 1:
            return list(dataframes_with_dp_std.values())[0]
        else:
            return pd.concat(dataframes_with_dp_std.values(), axis=1)


class pd_sum_groupby_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_SUM_GROUPBY_DP"
    _non_dp_equivalent_id = "pandas.PD_SUM_GROUPBY"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`numeric_only` is `True`"""
        numeric_only = signature["numeric_only"].static_value()
        return numeric_only is True

    async def query_builder(
        self, signature: SarusBoundSignature
    ) -> OptimizableQueryBuilder:
        parent_ds = signature["this"].static_value()
        if "budget" in signature:
            _, delta = await get_budget(signature)
        else:
            delta = DEFAULT_DELTA

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = ceil(
            float(
                parent_schema.properties().get(
                    MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT
                )
            )
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        tau_builder = tau_threshold_builder_delta(parent_ds, delta)

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

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder, tau_builder]
            + n_cols * [column_bounds_sum_builder],
        )
        return builder

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
        dataframegroupby: pd.core.groupby.DataFrameGroupBy = (
            await parent_ds.async_to(pd.core.groupby.DataFrameGroupBy)
        )
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        # Compute DP value
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, tau_thresholding_task, sum_tasks = (
            tasks[0],
            tasks[1],
            tasks[2:],
        )

        random_generator = np.random.default_rng(abs(seed_value))

        # we supposed: if max_mult_task has no compute then max mult is 1
        if max_mult_task.HasField("compute"):
            max_mul = MaxMultiplicityOp(
                parent_ds,
                epsilon,  # parameter for quantiles
                max_mult_task.compute.noise_user_count,
                max_mult_task.compute.noise_multiplicity,
                max_mult_task.compute.max_max_multiplicity,
            ).value(random_generator)
        else:
            max_mul = 1

        keys_name = dataframegroupby.keys
        keys_values = compute_tau_thresholding(
            parent_ds,
            tau_thresholding_task,
            keys_name,
            max_mul,
            random_generator,
        )

        dataframes_with_dp_sum = {}
        for index, column_name in enumerate(dataframegroupby.nth(0).columns):
            subtasks = [unwrap(task) for task in sum_tasks[index].subtasks]
            bounds_parameters, sum_parameters = (
                t.cast(GenericTask, subtasks[0]),
                t.cast(GenericTask, subtasks[1]),
            )
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof("type") == "optional":
                dataframes_with_dp_sum[column_name] = dataframegroupby.apply(
                    lambda x: np.nan
                ).to_frame(name="Sum")
                continue
            if column_type.WhichOneof("type") not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters["noise"],
            ).value(column_name, max_mul, random_generator)
            sum_op = GroupBySumOp(
                parent_ds,
                sum_parameters.parameters["noise"],
            )
            dataframes_with_dp_sum[column_name] = sum_op.value(
                column_name, max_mul, bounds, random_generator, keys_values
            )

        for col_name, df in dataframes_with_dp_sum.items():
            df.columns = [col_name]

        if len(dataframes_with_dp_sum.keys()) == 1:
            return list(dataframes_with_dp_sum.values())[0]
        else:
            return pd.concat(dataframes_with_dp_sum.values(), axis=1)
