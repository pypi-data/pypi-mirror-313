from __future__ import annotations

import typing as t

try:
    from sarus_synthetic_data.configs import typing as syn_typing
    import sarus_synthetic_data.configs.global_config as syn_config
    import sarus_synthetic_data.configs.independent as ind_conf
    import sarus_synthetic_data.configs.correlation as corr_conf
    from sarus_synthetic_data.correlations_generator.jax_model.codecs.batch import (
        BatchBuilder,
    )
    from sarus_synthetic_data.correlations_generator.jax_model.codec import (
        CodecBuilder,
    )
except ModuleNotFoundError:
    pass
from sarus_data_spec import typing as st, type as sdt
from sarus_data_spec.constants import (
    PU_COLUMN,
    PUBLIC,
    WEIGHTS,
)


def generate_synthetic_config(
    _type: st.Type,
    use_jax_text: bool,
    correlation: bool,
    public_tables: t.List[t.Tuple[str, ...]],
    **kwargs: t.Any,
) -> syn_config.SyntheticConfig:
    """Utility method to generate a table config"""

    if use_jax_text and not correlation:
        raise ValueError(
            "Correlation should be chose if we want to use jax for text"
        )
    table_configs = generate_table_config(
        _type,
        correlation=correlation,
        use_jax_text=use_jax_text,
        public_tables=public_tables,
        **kwargs,
    )

    return syn_config.SyntheticConfig(
        saving_directory="",
        tables=table_configs,
        privacy_unit_col=PU_COLUMN,
        is_private_col=PUBLIC,
        weights_col=WEIGHTS,
    )


def generate_table_config(
    _type: st.Type,
    correlation: bool,
    use_jax_text: bool,
    public_tables: t.List[t.Tuple[str, ...]],
    curr_path: t.Tuple[str, ...] = (),
    **kwargs: t.Any,
) -> t.Dict[t.Tuple[str, ...], syn_config.TableConfig]:
    class ConfigCreator(sdt.TypeVisitor):
        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.config = {
                name: item
                for field_name, field_type in fields.items()
                for name, item in generate_table_config(
                    _type=field_type,
                    use_jax_text=use_jax_text,
                    correlation=correlation,
                    public_tables=public_tables,
                    curr_path=(*curr_path, field_name),
                    **kwargs,
                ).items()
            }

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if curr_path in public_tables:
                config = syn_config.TableConfig(
                    data_uri="",
                    is_public=True,
                    independent_generation=None,
                    correlation_generation=None,
                )

            elif correlation:
                corr_columns = {}
                ind_columns = {}

                for field_name, field_type in _type.children().items():
                    col_config = generate_col_config(
                        _type=field_type,
                        use_jax_text=use_jax_text,
                        correlation=correlation,
                    )
                    if isinstance(
                        col_config, syn_config.SimpleColumn
                    ) or isinstance(col_config, syn_config.TrigramsColumn):
                        ind_columns[field_name] = col_config
                    else:
                        corr_columns[field_name] = col_config
                config = syn_config.TableConfig(
                    data_uri="",
                    is_public=False,
                    independent_generation=syn_config.IndependentConfig(
                        columns=ind_columns,
                        sampling_config=ind_conf.SamplingConfig(
                            total_size=0, should_jit=True, seed=0
                        ),
                        training_config=ind_conf.TrainingConfig(
                            should_jit=True, seed=0
                        ),
                    )
                    if len(ind_columns) > 0
                    else None,
                    correlation_generation=default_correlation_config(
                        corr_columns,
                        num_steps=10000,
                        physical_batch_size=10,
                        gradient_accumulation_steps=100,
                        **kwargs,
                    )
                    if len(corr_columns) > 0
                    else None,
                )
            else:
                config = syn_config.TableConfig(
                    data_uri="",
                    is_public=False,
                    independent_generation=syn_config.IndependentConfig(
                        columns={
                            field_name: generate_col_config(  # type:ignore
                                _type=field_type,
                                use_jax_text=False,
                                correlation=False,
                            )
                            for field_name, field_type in fields.items()
                        },
                        sampling_config=ind_conf.SamplingConfig(
                            total_size=0, should_jit=True, seed=0
                        ),
                        training_config=ind_conf.TrainingConfig(
                            should_jit=True, seed=0
                        ),
                    ),
                )
            self.config = {curr_path: config}

    visitor = ConfigCreator()
    _type.accept(visitor)
    return visitor.config


def default_correlation_config(
    corr_columns: t.Dict[str, syn_config.CorrelationColumn],
    sampling_batch_size: int = 100,
    num_steps: int = 1000,
    physical_batch_size: int = 100,
    gradient_accumulation_steps: int = 10,
    should_jit: bool = True,
    temperature_text_builder: float = 0.6,
) -> syn_config.CorrelationConfig:
    training = corr_conf.TrainingConfig(
        optimizer=corr_conf.OptimizerConfig(
            clipping_norm=1e-2,
            noise_multiplier=1e5,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=5e-3,
        ),
        check_pointing=corr_conf.CheckpointingConfig(
            output_dir="", save_every_steps=-1
        ),
        should_jit=should_jit,
        num_train_steps=num_steps,
        physical_batch_size=physical_batch_size,
    )
    model_config = default_model_config()
    sampling = corr_conf.SamplingConfig(
        sampling_batch_size,
        should_jit=should_jit,
        seed=1,
        total_size=0,
        temperature_text_builder=temperature_text_builder,
    )
    return syn_config.CorrelationConfig(
        columns=corr_columns,
        model=model_config,
        training=training,
        sampling=sampling,
    )


def default_model_config(
    embedding_dimension: int = 32,
) -> corr_conf.ModelConfig:
    return corr_conf.ModelConfig(
        load_params_from_checkpoint=False,
        load_pretrained_params=True,
        embedding_dimension=embedding_dimension,
        model_checkpoint_dir="",
        params_checkpoint_dir="",
        codec_builder=BatchBuilder(
            name="rows",
            sub_builder=CodecBuilder(
                name="default",
                use_pretrained=False,
                load_pretrained_dir="",
                save_trained=False,
                save_trained_dir="",
            ),
            use_pretrained=False,
            load_pretrained_dir="",
            save_trained=False,
            save_trained_dir="",
        ),
    )


def generate_col_config(
    _type: st.Type, use_jax_text: bool, correlation: bool
) -> syn_config.CorrelationColumn:
    """Generate columns config for any model"""

    class ColConfig(sdt.TypeVisitor):
        column: t.Union[
            syn_config.CorrelationColumn, syn_config.IndependentColumn
        ]

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            if correlation:
                self.column = syn_config.OptionalCorrelationColumn(
                    distribution=syn_config.IntegerDistribution(),
                    child_col=generate_col_config(  # type:ignore
                        _type=type,
                        use_jax_text=use_jax_text,
                        correlation=correlation,
                    ),
                )
            else:
                self.column = syn_config.OptionalIndependentColumn(
                    distribution=syn_config.IntegerDistribution(),
                    child_col=generate_col_config(  # type:ignore
                        _type=type,
                        use_jax_text=use_jax_text,
                        correlation=correlation,
                    ),
                )

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.column = syn_config.ColumnWithIntegerDistribution(
                distribution_kind=syn_typing.DistributionKind.histogram,
                distribution=syn_config.IntegerDistribution(),
                example=_type.example(),
                col_type=syn_typing.TypeKind.Boolean,
            )

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Integer
            self.column = syn_config.ColumnWithIntegerDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.IntegerDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Date
            self.column = syn_config.ColumnWithIntegerDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.IntegerDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Datetime
            self.column = syn_config.ColumnWithIntegerDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.IntegerDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Time
            self.column = syn_config.ColumnWithIntegerDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.IntegerDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Float
            self.column = syn_config.ColumnWithFloatDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.FloatDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = syn_typing.DistributionKind.histogram
            col_type = syn_typing.TypeKind.Text
            self.column = syn_config.ColumnWithStrDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.StrDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            self.column = syn_config.SimpleColumn(
                col_type=syn_typing.TypeKind.Id, example=_type.example()
            )

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Text

            if distribution_kind == syn_typing.DistributionKind.histogram:
                self.column = syn_config.ColumnWithStrDistribution(
                    distribution_kind=distribution_kind,
                    distribution=syn_config.StrDistribution(
                        values=t.cast(list, possible_values)
                    ),
                    example=_type.example(),
                    col_type=col_type,
                )
            else:
                if use_jax_text and correlation:
                    self.column = syn_config.TextCorrelationCol(
                        tokenizer_max_length=0,
                        distribution_kind=distribution_kind,
                        distribution=syn_config.IntegerDistribution(),
                        example=_type.example(),
                        col_type=col_type,
                    )
                else:
                    self.column = syn_config.TrigramsColumn(
                        distribution_kind=distribution_kind,
                        distribution=syn_config.IntegerDistribution(),
                        example=_type.example(),
                        col_type=col_type,
                        trigrams_noise=0,
                        trigrams_max_length=0,
                        trigrams_char_set=[],
                        sample_batch_size=10000,
                    )

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            self.column = syn_config.SimpleColumn(
                col_type=syn_typing.TypeKind.Unit, example=_type.example()
            )

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            distribution_kind = (
                syn_typing.DistributionKind.histogram
                if len(t.cast(list, possible_values)) > 0
                else syn_typing.DistributionKind.quantiles
            )
            col_type = syn_typing.TypeKind.Duration
            self.column = syn_config.ColumnWithIntegerDistribution(
                distribution_kind=distribution_kind,
                distribution=syn_config.IntegerDistribution(),
                example=_type.example(),
                col_type=col_type,
            )

    visitor = ColConfig()
    _type.accept(visitor)
    return visitor.column  # type:ignore
