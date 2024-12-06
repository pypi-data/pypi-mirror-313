import logging
import typing as t
import warnings
import os
from pathlib import Path
from sarus_data_spec.manager.async_utils import async_iter

try:
    import sarus_llm.recipes.serving as llm_serving
except (ModuleNotFoundError, ValueError, RuntimeError):
    warnings.warn("Sarus LLM not available")

import pyarrow as pa
import sys
from sarus_data_spec.constants import PUBLIC
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
)
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema
from sarus_data_spec.type import Struct, Text
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
import pyarrow.csv as pa_csv
from sarus_data_spec.transform import LORA_ATTN_MODULES

logger = logging.getLogger()


class GenerateFromModelStaticChecker(StandardDatasetStaticChecker):
    async def schema(self) -> st.Schema:
        _, kwargs = self.dataset.parents()
        pretrained_model = kwargs["model"]
        assert isinstance(pretrained_model, Scalar)
        prompts = kwargs["prompts"]
        assert isinstance(prompts, Dataset)
        is_public = pretrained_model.is_public() and prompts.is_public()
        return schema(
            dataset=self.dataset,
            schema_type=Struct(
                {"text": Text()}, properties={PUBLIC: str(is_public)}
            ),
        )


class GenerateFromModel(StandardDatasetImplementation):
    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        _, kwargs = self.dataset.parents()
        pretrained_model = kwargs["model"]
        prompts = kwargs["prompts"]
        transform = self.dataset.transform()

        assert (
            pretrained_model.prototype() == sp.Scalar  # type: ignore # noqa: E501
        ), "pretrained model should be a Scalar"
        pretrained_ds = t.cast(st.Scalar, pretrained_model)

        pretrained = await pretrained_ds.async_value()
        foundation_model_name, checkpoint_path, sample_type = pretrained
        assert prompts.prototype() == sp.Dataset, "prompts should be a Dataset"
        prompts_ds = t.cast(st.Dataset, prompts)

        # if finetuned need to get model info
        transform_spec = pretrained_ds.transform().spec()
        if transform_spec in ["fit_model", "fit_model_dp"]:
            model_specs = getattr(
                pretrained_ds.transform().protobuf().spec, transform_spec
            )
            quantization = model_specs.quantize
            use_lora = model_specs.use_lora
            lora_attn_modules = model_specs.lora_attn_modules
            apply_lora_to_mlp = model_specs.apply_lora_to_mlp
            apply_lora_to_output = model_specs.apply_lora_to_output
            lora_alpha = model_specs.lora_alpha
            lora_rank = model_specs.lora_rank

        else:
            quantization = False
            use_lora = False
            # next params passed but unused
            lora_attn_modules = []
            apply_lora_to_mlp = False
            apply_lora_to_output = False
            lora_alpha = 256
            lora_rank = 128

        specs = transform.protobuf().spec.generate_from_model
        dataset = pa.concat_tables(
            [
                pa.Table.from_struct_array(batch.column("sarus_data"))
                async for batch in await prompts_ds.async_to_arrow()
            ]
        )

        # saving_dir
        saving_dir = os.path.join(
            self.dataset.manager().parquet_dir(),
            "llm_sampling",
            self.dataset.uuid(),
        )
        os.makedirs(saving_dir, exist_ok=True)
        # get foundation_model_name
        json_file = os.path.join(saving_dir, "llm_input.jsonl")
        dataset.to_pandas().to_json(json_file, orient="records", lines=True)
        tokenization_dir = os.path.join(
            saving_dir,
            "tokenization",
        )
        sample_saving_dir = os.path.join(saving_dir, "sample.csv")
        cmd, env = prepare_sampling_cmd_env(
            sample_type=sample_type,
            foundation_model_name=foundation_model_name,
            temperature=specs.temperature,
            max_tokens=specs.max_new_tokens,
            restoring_path=checkpoint_path,
            data_dir=json_file,
            tokenization_dir=tokenization_dir,
            sample_saving_dir=sample_saving_dir,
            quantization=quantization,
            use_lora=use_lora,
            lora_attn_modules=lora_attn_modules,
            apply_lora_to_mlp=apply_lora_to_mlp,
            apply_lora_to_output=apply_lora_to_output,
            lora_rank=lora_rank,
            lora_alpha=lora_alpha,
        )
        self.dataset.manager().launch_job(command=cmd, env=env)
        tab = pa_csv.read_csv(sample_saving_dir)
        return async_iter(tab.to_batches(max_chunksize=batch_size))


def prepare_sampling_cmd_env(
    sample_type: str,
    foundation_model_name: str,
    data_dir: str,
    tokenization_dir: str,
    restoring_path: str,
    temperature: float,
    max_tokens: int,
    sample_saving_dir: str,
    quantization: bool,
    use_lora: bool,
    lora_attn_modules: t.Optional[t.List[LORA_ATTN_MODULES]],
    apply_lora_to_mlp: bool,
    apply_lora_to_output: bool,
    lora_rank: int,
    lora_alpha: int,
) -> t.Tuple[t.List[str], t.Dict[str, str]]:
    """
    Prepares and returns the command list and an environment
    with the correct DeepSpeed environment variables.
    """

    cmd = [sys.executable, llm_serving.__file__]
    config_file = str(
        os.path.join(Path(__file__).parent, "sampling_config.yaml")
    )
    cmd.extend(["--config", config_file])
    cmd.append(f"sample_type={sample_type}")
    cmd.append(f"foundation_model_name={foundation_model_name}")
    if not quantization:
        # default is True
        cmd.append("quantization.load_in_4bit=False")
    if not use_lora:
        # remove lora config
        cmd.append("~lora")
    else:
        if lora_attn_modules is not None:
            cmd.append(f"lora.lora_attn_modules={lora_attn_modules}")
        cmd.append(f"lora.apply_lora_to_mlp={apply_lora_to_mlp}")
        cmd.append(f"lora.apply_lora_to_output={apply_lora_to_output}")
    # dataset info
    cmd.append(f"dataset.data_dir={data_dir}")
    cmd.append(f"dataset.tokenization_dir={tokenization_dir}")
    cmd.append("sampler.triton_kernel=False")
    cmd.append(f"sampler.temperature={temperature}")
    cmd.append(f"sampler.max_length={max_tokens}")
    checkpoint_path = restoring_path if restoring_path != "" else None
    cmd.append(f"checkpoint_path={checkpoint_path}")
    cmd.append(f"saving_dir={sample_saving_dir}")

    current_env = os.environ.copy()
    return cmd, current_env
