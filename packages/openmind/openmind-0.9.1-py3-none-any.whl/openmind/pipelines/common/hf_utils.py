# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Lepton AI, Inc. All rights reserved.
#
# Adapted from
# https://github.com/leptonai/leptonai/blob/main/leptonai/photon/hf/hf_utils.py
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, Dict

from ...utils.constants import (
    DIFFUSERS_DEFINED_TASKS,
    TRANSFORMERS_DEFINED_TASKS,
    Backends,
    Tasks,
)
from ..pipeline_utils import download_from_repo
from .util import register_pipeline_creator, get_pipeline


PIPELINE_CREATOR_MAPPING: Dict[Tasks, Dict[Backends, Callable]] = {}


def create_diffusion_pipeline(
    task: str = None,
    model: str = None,
    use_silicondiff: bool = False,
    **kwargs,
):
    """
    device (`str` or `torch.device`):
        Defines the device(*e.g.*, `"cpu"`, `"npu:1"`) on which this pipeline will be allocated.
    """
    from accelerate.utils import is_npu_available

    revision = kwargs.pop("revision", None)
    cache_dir = kwargs.pop("cache_dir", None)
    force_download = kwargs.pop("force_download", False)
    device_map = kwargs.pop("device_map", None)
    device = kwargs.pop("device", None)
    torch_dtype = kwargs.pop("torch_dtype", None)

    if device is not None and device_map is not None:
        raise ValueError(
            "You cannot use both `pipeline(... device_map=..., device=...)` as those arguments might conflict, use only one."
        )

    if isinstance(model, str):
        model = download_from_repo(model, revision=revision, cache_dir=cache_dir, force_download=force_download)
    else:
        raise ValueError()

    pipeline_cls = get_pipeline(task, backend="diffusers")

    pipeline = pipeline_cls.from_pretrained(
        model,
        revision=revision,
        device_map=device_map,
        torch_dtype=torch_dtype,
    )

    if device is not None:
        pipeline = pipeline.to(device)

    if use_silicondiff:
        if not is_npu_available():
            raise RuntimeError(
                "Silicondiff currently only supports Ascend NPU. Please specify 'device=npu:0' in your configuration."
            )
        import silicondiff_npu

        pipeline.unet = silicondiff_npu.compile(pipeline.unet, dynamnic=True, use_jit=True)
        pipeline.vae.decoder = silicondiff_npu.compile(pipeline.vae.decoder, dynamnic=True, use_jit=True)

    return pipeline


for hf_task in DIFFUSERS_DEFINED_TASKS:
    register_pipeline_creator(PIPELINE_CREATOR_MAPPING, hf_task, Backends.diffusers, create_diffusion_pipeline)


def create_transformers_pipeline(
    task: str = None,
    model: str = None,
    config: str = None,
    tokenizer: str = None,
    feature_extractor: str = None,
    image_processor: str = None,
    model_kwargs: Dict = None,
    **kwargs,
):
    from transformers import pipeline, AutoTokenizer

    revision = kwargs.pop("revision", None)
    cache_dir = kwargs.pop("cache_dir", None)
    force_download = kwargs.pop("force_download", False)
    torch_dtype = kwargs.pop("torch_dtype", None)
    use_auth_token = kwargs.pop("use_auth_token", None)
    trust_remote_code = kwargs.pop("trust_remote_code", None)
    _commit_hash = kwargs.get("_commit_hash", None)

    if isinstance(model, str):
        model_name_or_path = download_from_repo(
            model, revision=revision, cache_dir=cache_dir, force_download=force_download
        )
    else:
        model_name_or_path = model

    if tokenizer is not None:
        if isinstance(tokenizer, str):
            tokenizer_name_or_path = download_from_repo(
                tokenizer, revision=revision, cache_dir=cache_dir, force_download=force_download
            )
        else:
            tokenizer_name_or_path = tokenizer
    else:
        if (task == "text-generation" or task == "text_generation") and isinstance(model, str):
            tokenizer_kwargs = {
                "revision": revision,
                "token": use_auth_token,
                "trust_remote_code": trust_remote_code,
                "_commit_hash": _commit_hash,
                "torch_dtype": torch_dtype,
            }
            tokenizer_name_or_path = AutoTokenizer.from_pretrained(model_name_or_path, **tokenizer_kwargs)
        else:
            tokenizer_name_or_path = tokenizer

    if isinstance(config, str):
        config_name_or_path = download_from_repo(
            config, revision=revision, cache_dir=cache_dir, force_download=force_download
        )
    else:
        config_name_or_path = config

    if isinstance(feature_extractor, str):
        feature_extractor_name_or_path = download_from_repo(
            feature_extractor, revision=revision, cache_dir=cache_dir, force_download=force_download
        )
    else:
        feature_extractor_name_or_path = feature_extractor

    if isinstance(image_processor, str):
        image_processor_name_or_path = download_from_repo(
            image_processor, revision=revision, cache_dir=cache_dir, force_download=force_download
        )
    else:
        image_processor_name_or_path = image_processor

    pipe = pipeline(
        task=task,
        model=model_name_or_path,
        tokenizer=tokenizer_name_or_path,
        config=config_name_or_path,
        feature_extractor=feature_extractor_name_or_path,
        image_processor=image_processor_name_or_path,
        revision=revision,
        torch_dtype=torch_dtype,
        trust_remote_code=trust_remote_code,
        model_kwargs=model_kwargs,
        **kwargs,
    )

    return pipe


for hf_task in TRANSFORMERS_DEFINED_TASKS:
    register_pipeline_creator(PIPELINE_CREATOR_MAPPING, hf_task, Backends.transformers, create_transformers_pipeline)
