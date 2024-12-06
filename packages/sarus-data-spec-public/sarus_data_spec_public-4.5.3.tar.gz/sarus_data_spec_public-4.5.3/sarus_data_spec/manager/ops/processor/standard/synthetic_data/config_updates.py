from __future__ import annotations

import typing as t
import numpy as np

from sarus_data_spec import typing as st
from sarus_data_spec.path import straight_path
from sarus_data_spec.constants import DATA, OPTIONAL_VALUE, PU_COLUMN

try:
    import sarus_synthetic_data.configs.global_config as sd_config
    import sarus_synthetic_data.configs.typing as sd_typing
    from sarus_synthetic_data.correlations_generator.jax_model.codecs.categorical import (
        CategoricalBuilder,
    )
    from sarus_synthetic_data.correlations_generator.jax_model.codecs.dynamic_array import (
        DynamicArrayBuilder,
    )
    from sarus_synthetic_data.correlations_generator.jax_model.codecs.optional import (
        OptionalBuilder,
    )
    from sarus_synthetic_data.correlations_generator.jax_model.codecs.struct import (
        StructBuilder,
    )
    from sarus_synthetic_data.correlations_generator.jax_model.codecs.text import (
        TextBuilder,
    )
except ModuleNotFoundError:
    pass
import pyarrow as pa
import os


def update_config(
    config_with_noise: sd_config.SyntheticConfig,
    synthetic_data_dir: str,
    parent_stats: st.Statistics,
    links_stats: t.List[st.LinkStatistics],
) -> sd_config.SyntheticConfig:
    config_with_noise.saving_directory = synthetic_data_dir
    for table_name, table_config in config_with_noise.tables.items():
        table_path = straight_path([DATA, *table_name])
        table_stat = parent_stats.nodes_statistics(table_path)[0]
        current_saving_dir = os.path.join(synthetic_data_dir, *table_name)
        update_table_config(table_stat, table_config, current_saving_dir)

    links_list = [
        sd_config.LinkInfo(
            primary_key=tuple(
                link_statistics.pointed().to_strings_list()[0][1:]
            ),
            foreign_key=tuple(
                link_statistics.pointing().to_strings_list()[0][1:]
            ),
            count_distribution=sd_config.IntegerDistribution(
                values=link_statistics.distribution().values(),  # type:ignore[arg-type]
                probabilities=link_statistics.distribution().probabilities(),
            ),
        )
        for link_statistics in links_stats
    ]
    if len(links_list) > 0:
        config_with_noise.links = sd_config.LinksConfig(
            links_info_list=links_list, seed=2
        )
    return config_with_noise


def update_table_config(
    table_stat: st.Statistics,
    table_config: sd_config.TableConfig,
    current_saving_dir: str,
) -> sd_config.TableConfig:
    """Methods updates:
    - each of the correlation/independent config (see respective method for how)
    -
    """
    if table_config.independent_generation is not None:
        table_config.independent_generation.sampling_config.total_size = (
            table_stat.size()
        )
        update_values_and_probabilities_config(
            table_stat, table_config.independent_generation
        )

    if table_config.correlation_generation is not None:
        correlation_config = update_correlation_config(
            table_stat, table_config.correlation_generation, current_saving_dir
        )
        table_config.correlation_generation = correlation_config
    return table_config


def update_values_and_probabilities_config(
    table_stat: st.Statistics,
    config: t.Union[sd_config.IndependentConfig, sd_config.CorrelationConfig],
) -> None:
    """Method that updates the following fields of the config:
    - the number of lines to to be sampled for the table
    - the distribution of each column
    """

    stat_fields = table_stat.children()

    for column_name, col_config in config.columns.items():
        curr_stat = stat_fields[column_name]

        if isinstance(
            col_config, sd_config.OptionalIndependentColumn
        ) or isinstance(col_config, sd_config.OptionalCorrelationColumn):
            size_all = curr_stat.size()
            size_non_null = curr_stat.children()[OPTIONAL_VALUE].size()
            col_config.distribution = type(col_config.distribution)(
                values=[0, 1],
                probabilities=[
                    1 - size_non_null / size_all,
                    size_non_null / size_all,
                ],
            )
            child_col = col_config.child_col
            if not isinstance(child_col, sd_config.SimpleColumn):
                distrib = curr_stat.children()[OPTIONAL_VALUE].distribution()
                if isinstance(child_col, sd_config.ColumnWithStrDistribution):
                    child_col.distribution = type(child_col.distribution)(
                        values=child_col.distribution.values,
                        probabilities=distrib.probabilities(),
                    )
                else:
                    child_col.distribution = type(child_col.distribution)(
                        values=distrib.values(),  # type:ignore[arg-type]
                        probabilities=distrib.probabilities(),
                    )

                if isinstance(child_col, sd_config.TextCorrelationCol):
                    # average chars per token is 4
                    child_col.tokenizer_max_length = np.ceil(
                        distrib.values()[-1] / 4
                    ).astype(int)

                if isinstance(child_col, sd_config.TrigramsColumn):
                    child_col.trigrams_max_length = distrib.values()[-1]  # type:ignore

        elif not isinstance(col_config, sd_config.SimpleColumn):
            distrib = curr_stat.distribution()
            if isinstance(col_config, sd_config.ColumnWithStrDistribution):
                col_config.distribution = type(col_config.distribution)(
                    values=col_config.distribution.values,
                    probabilities=distrib.probabilities(),
                )
            else:
                col_config.distribution = type(col_config.distribution)(
                    values=distrib.values(),  # type:ignore[arg-type]
                    probabilities=distrib.probabilities(),
                )

            if isinstance(col_config, sd_config.TextCorrelationCol):
                # average chars per token is 4
                col_config.tokenizer_max_length = np.ceil(
                    distrib.values()[-1] / 4
                ).astype(int)

            if isinstance(col_config, sd_config.TrigramsColumn):
                col_config.trigrams_max_length = distrib.values()[-1]  # type:ignore


def update_correlation_config(
    table_stat: st.Statistics,
    correlation_config: sd_config.CorrelationConfig,
    current_saving_dir: str,
) -> sd_config.CorrelationConfig:
    correlation_config.training.check_pointing.output_dir = current_saving_dir
    correlation_config.sampling.total_size = table_stat.size()
    update_values_and_probabilities_config(
        table_stat=table_stat, config=correlation_config
    )
    stat_fields = table_stat.children()
    sub_builders = []
    sampling_temperature_text = (
        correlation_config.sampling.temperature_text_builder
    )
    for name, col_config in correlation_config.columns.items():
        builders = builder_from_col_config(
            name, col_config, stat_fields[name], sampling_temperature_text
        )
        sub_builders.extend(builders)

    struct = StructBuilder(
        name="table",
        sub_builders=sub_builders,
        n_heads=4,
        n_blocks=1,
        use_pretrained=False,
        load_pretrained_dir="",
        save_trained=False,
        save_trained_dir="",
        has_text=any(
            isinstance(col, sd_config.TextCorrelationCol)
            if not isinstance(col, sd_config.OptionalCorrelationColumn)
            else isinstance(col.child_col, sd_config.TextCorrelationCol)
            for col in correlation_config.columns.values()
        ),
    )
    # for DP
    max_mult = int(table_stat.multiplicity())
    list_builder = DynamicArrayBuilder(
        name=PU_COLUMN,
        value_builder=struct,
        batch_size=min(10, max_mult),
        max_size=max_mult,
        n_heads=4,
        n_blocks=1,
        use_pretrained=False,
        load_pretrained_dir="",
        save_trained=False,
        save_trained_dir="",
    )
    correlation_config.model.codec_builder.sub_builder = list_builder
    return correlation_config


def builder_from_col_config(
    name: str,
    col_config: t.Union[
        sd_config.OptionalCorrelationColumn,
        sd_config.NonOptionalCorrelationColumn,
    ],
    stats: st.Statistics,
    sampling_temperature_text: float,
) -> t.List[t.Any]:
    if isinstance(col_config, sd_config.OptionalCorrelationColumn):
        return [
            OptionalBuilder(
                sub_builder=el,
                name="optional_" + el.name,
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            )
            for el in builder_from_col_config(
                name,
                col_config.child_col,
                stats.children()[OPTIONAL_VALUE],
                sampling_temperature_text,
            )
        ]

    col_type = col_config.col_type
    distribution_kind = col_config.distribution_kind

    if (
        col_type == sd_typing.TypeKind.Datetime
        and distribution_kind == sd_typing.DistributionKind.quantiles
    ):
        vals = col_config.distribution.values
        min_year = pa.compute.year(
            pa.scalar(vals[0], pa.timestamp("ns"))
        ).as_py()
        max_year = pa.compute.year(
            pa.scalar(vals[-1], pa.timestamp("ns"))
        ).as_py()

        return [
            CategoricalBuilder(
                vocab_size=max_year - min_year + 1,
                name=name + "_year",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=12,
                name=name + "_month",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=31,
                name=name + "_day",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=24,
                name=name + "_hour",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=60,
                name=name + "_minutes",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=60,
                name=name + "_seconds",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
        ]
    elif (
        col_type == sd_typing.TypeKind.Date
        and distribution_kind == sd_typing.DistributionKind.quantiles
    ):
        vals = col_config.distribution.values
        min_year = pa.compute.year(
            pa.scalar(np.int32(vals[0]), pa.date32())
        ).as_py()
        max_year = pa.compute.year(
            pa.scalar(np.int32(vals[-1]), pa.date32())
        ).as_py()

        return [
            CategoricalBuilder(
                vocab_size=max_year - min_year + 1,
                name=name + "_year",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=12,
                name=name + "_month",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=31,
                name=name + "_day",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
        ]

    elif (
        col_type == sd_typing.TypeKind.Time
        and distribution_kind == sd_typing.DistributionKind.quantiles
    ):
        return [
            CategoricalBuilder(
                vocab_size=24,
                name=name + "_hour",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=60,
                name=name + "_minutes",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            CategoricalBuilder(
                vocab_size=60,
                name=name + "_seconds",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
        ]

    elif isinstance(col_config, sd_config.TextCorrelationCol):
        return [
            TextBuilder(
                name=name,
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
                n_tokens=10,
                max_length=t.cast(
                    int, min(stats.distribution().values()[-1], 100)
                ),  # TODO: this is number of char, should be number of tokens
                hidden_size=64,  # TinyStories
                temperature=sampling_temperature_text,
            )
        ]
    else:
        vals = col_config.distribution.values
        if (
            col_config.distribution_kind
            == sd_typing.DistributionKind.quantiles
            and vals[0] == vals[1]
        ):
            # for quantiles there are always at least 2 values
            vocab_size = len(vals) - 1
        else:
            vocab_size = len(vals)
        return [
            CategoricalBuilder(
                vocab_size=vocab_size,
                name=name,
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            )
        ]
