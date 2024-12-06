# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Alibaba, Inc. and its affiliates.  All rights reserved.
#
# Adapted from
# https://github.com/modelscope/modelscope/blob/v1.8.4/modelscope/utils/hf_util.py
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

import os
from typing import List, Optional, Union

from transformers import (
    AutoConfig as HfAutoConfig,
    AutoFeatureExtractor as HfAutoFeatureExtractor,
    AutoImageProcessor as HfAutoImageProcessor,
    AutoModel as HfAutoModel,
    AutoModelForCausalLM as HfAutoModelForCausalLM,
    AutoModelForPreTraining as HfAutoModelForPreTraining,
    AutoModelForQuestionAnswering as HfAutoModelForQuestionAnswering,
    AutoModelForSequenceClassification as HfAutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM as HfAutoModelForSeq2SeqLM,
    AutoModelForTokenClassification as HfAutoModelForTokenClassification,
    AutoProcessor as HfAutoProcessor,
    AutoTokenizer as HfAutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from ..utils.hub import OpenMindHub
from ..utils.hub import OMValidationError
from ..utils.generic import replace_invalid_characters


def _patch_pretrained_model():
    """
    Monkey patch `PreTrainedModel.from_pretrained` to adapt to openMind Hub.
    This patch will alter the behavior of the `from_pretrained` method for `PreTrainedModel` and its subclasses.
    Previously, when invoking `from_pretrained`, models were loaded from the Hugging Face Hub.
    However, with this patch applied, the method will now load models from openMind Hub instead.
    """
    orig_func = PreTrainedModel.from_pretrained.__func__

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
        if not os.path.exists(pretrained_model_name_or_path):
            local_dir = OpenMindHub.snapshot_download(
                pretrained_model_name_or_path,
                revision=kwargs.pop("revision", None),
                ignore_patterns=kwargs.pop("ignore_patterns", None),
                cache_dir=kwargs.pop("cache_dir", None),
                force_download=kwargs.pop("force_download", None),
            )
        else:
            local_dir = pretrained_model_name_or_path
        return orig_func(cls, local_dir, *args, **kwargs)

    PreTrainedModel.from_pretrained = from_pretrained


def _patch_pretrained_tokenizer_base():
    """
    Monkey patch `PreTrainedTokenizerBase.from_pretrained` to adapt to openMind Hub.
    This patch will alter the behavior of the `from_pretrained` method for `PreTrainedTokenizerBase` and its subclasses.
    Previously, when invoking `from_pretrained`, models were loaded from the Hugging Face Hub.
    However, with this patch applied, the method will now load tokenizers from openMind Hub instead.
    """
    orig_func = PreTrainedTokenizerBase.from_pretrained.__func__

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
        if not os.path.exists(pretrained_model_name_or_path):
            local_dir = OpenMindHub.snapshot_download(
                pretrained_model_name_or_path,
                revision=kwargs.pop("revision", None),
                ignore_patterns=kwargs.pop("ignore_patterns", None),
                cache_dir=kwargs.pop("cache_dir", None),
                force_download=kwargs.pop("force_download", None),
            )
        else:
            local_dir = pretrained_model_name_or_path
        return orig_func(cls, local_dir, *args, **kwargs)

    PreTrainedTokenizerBase.from_pretrained = from_pretrained


_patch_pretrained_model()
_patch_pretrained_tokenizer_base()


def get_wrapped_autoclass(
    auto_class,
    allow_patterns: Optional[Union[List[str], str]] = None,
    ignore_patterns: Optional[Union[List[str], str]] = None,
    **kwargs,
):
    """Get a custom wrapper class for auto-classes to download files from the openMind Hub"""

    class Wrapper(auto_class):
        @classmethod
        def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
            if not os.path.exists(pretrained_model_name_or_path):
                # In the Case of 'AutoXXX.from_pretrained(path)', if `path` is not existed,
                # we will raise OSError and remind users to provide a valid path or repo_id of a model
                # on the Hub.
                try:
                    local_dir = OpenMindHub.snapshot_download(
                        pretrained_model_name_or_path,
                        revision=kwargs.pop("revision", None),
                        allow_patterns=kwargs.pop("allow_patterns", allow_patterns),
                        ignore_patterns=kwargs.pop("ignore_patterns", ignore_patterns),
                        cache_dir=kwargs.pop("cache_dir", None),
                        force_download=kwargs.pop("force_download", None),
                    )
                except OMValidationError as e:
                    error_msg = (
                        f"Incorrect path_or_model_id: '{pretrained_model_name_or_path}'. Please provide either"
                        f"the path to a local folder or the repo_id of a model on the Hub."
                    )
                    raise OSError(replace_invalid_characters(error_msg)) from e

            else:
                local_dir = pretrained_model_name_or_path
            return auto_class.from_pretrained(local_dir, *args, **kwargs)

    Wrapper.__name__ = auto_class.__name__
    Wrapper.__qualname__ = auto_class.__qualname__
    return Wrapper


AutoConfig = get_wrapped_autoclass(HfAutoConfig, allow_patterns=["*.json", "*.py"])
AutoFeatureExtractor = get_wrapped_autoclass(HfAutoFeatureExtractor, ignore_patterns=["*.h5", "*.msgpack"])
AutoImageProcessor = get_wrapped_autoclass(HfAutoImageProcessor, ignore_patterns=["*.h5", "*.msgpack"])
AutoProcessor = get_wrapped_autoclass(HfAutoProcessor, ignore_patterns=["*.bin", "*.safetensors", "*.h5", "*.msgpack"])
AutoTokenizer = get_wrapped_autoclass(HfAutoTokenizer, ignore_patterns=["*.bin", "*.safetensors", "*.h5", "*.msgpack"])
AutoModel = get_wrapped_autoclass(HfAutoModel, ignore_patterns=["*.h5", "*.msgpack"])
AutoModelForCausalLM = get_wrapped_autoclass(HfAutoModelForCausalLM, ignore_patterns=["*.h5", "*.msgpack"])
AutoModelForPreTraining = get_wrapped_autoclass(HfAutoModelForPreTraining, ignore_patterns=["*.h5", "*.msgpack"])
AutoModelForQuestionAnswering = get_wrapped_autoclass(
    HfAutoModelForQuestionAnswering, ignore_patterns=["*.h5", "*.msgpack"]
)
AutoModelForSequenceClassification = get_wrapped_autoclass(
    HfAutoModelForSequenceClassification, ignore_patterns=["*.h5", "*.msgpack"]
)
AutoModelForSeq2SeqLM = get_wrapped_autoclass(HfAutoModelForSeq2SeqLM, ignore_patterns=["*.h5", "*.msgpack"])
AutoModelForTokenClassification = get_wrapped_autoclass(
    HfAutoModelForTokenClassification, ignore_patterns=["*.h5", "*.msgpack"]
)
