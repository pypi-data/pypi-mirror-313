import csv
import os
from typing import Any, Dict, Optional

from tabulate import tabulate

from ..utils.logging import get_logger, set_verbosity_info
from ..utils.constants import DEFAULT_FLAGS, DEFAULT_MODES
from .builder import build_pipeline
from .pipeline_utils import SUPPORTED_TASK_MAPPING


logger = get_logger()
set_verbosity_info()


def pipeline(
    task: Optional[str] = None,
    model=None,
    config=None,
    tokenizer=None,
    feature_extractor=None,
    image_processor=None,
    framework: Optional[str] = None,
    backend: Optional[str] = None,
    model_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """
    Build a pipeline instance.
    Belowing docstring is mostly adapted from transformers.pipelines.pipeline

    Args:
        task:
            The task defining which pipeline will be returned.
        model:
            The model that will be used by the pipeline to make predictions.
            This can be a model identifier or an actual instance of a pretrained model.
            If not provided, the default for the `task` will be loaded.
        config:
            The configuration that will be used by the pipeline to instantiate
            the model. This can be a model identifier or an actual pretrained model
            configuration.
        tokenizer:
            The tokenizer that will be used by the pipeline to encode data for
            the model. This can be a model identifier or an actual pretrained tokenizer.
        feature_extractor:
            The feature extractor that will be used by the pipeline to encode data for
            the model. This can be a model identifier or an actual pretrained
             feature extractor.
        image_processor:
            The image_processor that will be used by the pipeline.
        framework (`str`, *optional*):
            The framework to use, either `"pt"` for PyTorch or "ms" for mindspore.
            The specified framework must be installed.
        backend (`str`, *optional*):
            backend is used to specify dependent libraries.
            The specified backend must be installed.
        kwargs:
            Additional keyword arguments passed along to the specific pipeline init.
            e.g. for transformers pipeline:
                revision (`str`, *optional*, defaults to `"main"`):
                    When passing a task name or a string model identifier:
                    The specific model version to use. It can be a branch name,
                    a tag name, or a commit id, since we use a git-based system for
                    storing models and other artifacts on openmind hub, so `revision`
                     can be any identifier allowed by git.
                use_fast (`bool`, *optional*, defaults to `True`):
                    Whether to use a Fast tokenizer if possible
                    (a [`PreTrainedTokenizerFast`]).
                device (`int` or `str` or `torch.device`):
                    Defines the device (*e.g.*, `"cpu"`, `"npu:0"`) on which this pipeline will be allocated.
                device_map (`str` or `Dict[str, Union[int, str, torch.device]`,
                *optional*):
                    Sent directly as `model_kwargs` (just a simpler shortcut).
                    When `accelerate` library is present, set `device_map="auto"` to
                    compute the most optimized `device_map` automatically.
                    Do not use `device_map` AND `device` at the same time as they will
                    conflict.
                torch_dtype (`str` or `torch.dtype`, *optional*):
                    Sent directly as `model_kwargs` (just a simpler shortcut) to use
                    the available precision for this model
                    (`torch.float16`, `torch.bfloat16`, ... or `"auto"`).
                trust_remote_code (`bool`, *optional*, defaults to `False`):
                    Whether to allow for custom code defined on the Hub in their own
                    modeling, configuration, tokenization or even pipeline files.
                    This option should only be set to `True` for repositories you trust
                    and in which you have read the code, as it will execute code present
                     on the Hub on your local machine.
                model_kwargs (`Dict[str, Any]`, *optional*):
                    Additional dictionary of keyword arguments passed along to the
                    model's `from_pretrained(...,**model_kwargs)` function.

    Returns:
        A suitable pipeline for the task.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> # will use transformers pipeline if not specified
    >>> pipe = pipeline(task="fill-mask", model="PyTorch-NPU/bert_base_uncased")

    >>> # if you want to use mindformers pipeline
    >>> pipe = pipeline("text-generation", model="MindSpore-Lab/qwen1_5_7b", backend="mindformers", framework="ms")
    ```
    """

    return build_pipeline(
        task, model, config, tokenizer, feature_extractor, image_processor, framework, backend, model_kwargs, **kwargs
    )


def generate_pipeline_report(print_report: bool = True, save_report: bool = False):
    table_rows = []
    for task, task_config in SUPPORTED_TASK_MAPPING.items():
        for framework, framework_config in task_config.items():
            if framework == "default_framework":
                continue
            for backend, backend_config in framework_config.items():
                if backend == "default_backend":
                    continue
                models = ", ".join(backend_config["supported_models"])
                table_rows.append([task, framework, backend, models])
    if save_report:
        with os.fdopen(os.open("pipeline_report.csv", DEFAULT_FLAGS, DEFAULT_MODES), "w", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Task", "Framework", "Backend", "Supported Models"])
            csvwriter.writerows(table_rows)
        logger.info("Pipeline report has been successfully written to pipeline_report.csv")

    if print_report:
        table = []
        for item in table_rows:
            task, framework, backend, models = item
            models = models.replace(", ", "\n")
            table.append(
                {
                    "Task": task,
                    "Framework": framework,
                    "Backend": backend,
                    "Supported Models": models,
                }
            )
        print(tabulate(table, headers="keys", tablefmt="grid"))
