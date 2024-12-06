# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Lepton AI, Inc. and its affiliates.  All rights reserved.
#
# Adapted from
# https://github.com/leptonai/leptonai/blob/main/leptonai/registry.py#L6
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

import importlib
from typing import Callable, Dict
from ...utils.constants import (
    Backends,
    Tasks,
)


def register_pipeline_creator(mapping: Dict, task: Tasks, backend: Backends, pipeline_creator: Callable):
    if task not in mapping:
        mapping[task] = {backend: pipeline_creator}
    else:
        mapping[task][backend] = pipeline_creator


def get_pipeline(task, backend):
    pipelines = {
        "text-to-image": ("diffusers", "AutoPipelineForText2Image"),
        "image-to-image": ("diffusers", "AutoPipelineForImage2Image"),
        "inpainting": ("diffusers", "AutoPipelineForInpainting"),
        "text-to-video": ("diffusers", "DiffusionPipeline"),
    }

    if task not in pipelines:
        raise ValueError(f"The {task} task is not supported.")

    backend_module, pipeline_class = pipelines[task]

    if backend == "diffusers":
        module = importlib.import_module(backend_module)
    elif backend == "mindone":
        module = importlib.import_module(f"{backend}.{backend_module}")
    else:
        raise ValueError(f"The {backend} backend is not supported.")

    return getattr(module, pipeline_class)
