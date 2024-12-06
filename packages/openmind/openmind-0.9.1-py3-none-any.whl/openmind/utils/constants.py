# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# openMind is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from enum import Enum
import json
import os
import stat


class Tasks:
    # NLP
    text_classification = "text-classification"
    sentiment_analysis = "sentiment-analysis"
    text_generation = "text-generation"
    zero_shot_classification = "zero-shot-classification"
    zero_shot_object_detection = "zero-shot-object-detection"
    text2text_generation = "text2text-generation"
    token_classification = "token-classification"
    fill_mask = "fill-mask"
    question_answering = "question-answering"
    summarization = "summarization"
    table_question_answering = "table-question-answering"
    translation = "translation"
    # Computer vision
    depth_estimation = "depth-estimation"
    image_to_image = "image-to-image"
    zero_shot_image_classification = "zero-shot-image-classification"
    image_classification = "image-classification"
    # multi-modal tasks
    text_to_image = "text-to-image"
    mask_generation = "mask-generation"
    visual_question_answering = "visual-question-answering"
    feature_extraction = "feature-extraction"
    image_to_text = "image-to-text"
    text_to_video = "text-to-video"
    inpainting = "inpainting"


class Frameworks:
    ms = "ms"
    pt = "pt"


class Backends:
    transformers = "transformers"
    diffusers = "diffusers"
    mindformers = "mindformers"
    mindnlp = "mindnlp"
    mindone = "mindone"


class HubName(Enum):
    openmind_hub = "OpenMindHub"


DIFFUSERS_DEFINED_TASKS = [
    # diffusers
    Tasks.text_to_image,
    Tasks.image_to_image,
    Tasks.text_to_video,
    Tasks.inpainting,
]

MINDFORMERS_DEFINED_TASKS = [
    # mindformers
    Tasks.text_generation,
]

MINDNLP_DEFINED_TASKS = [
    # mindnlp
    Tasks.text_generation,
]

MINDONE_DEFINED_TASKS = [
    # diffusers
    Tasks.text_to_image,
    Tasks.image_to_image,
]

# These tasks will be registered in hf_utils.py.
TRANSFORMERS_DEFINED_TASKS = [
    # transformers
    Tasks.text_classification,
    Tasks.sentiment_analysis,
    Tasks.visual_question_answering,
    Tasks.zero_shot_classification,
    Tasks.zero_shot_object_detection,
    Tasks.mask_generation,
    Tasks.depth_estimation,
    Tasks.image_to_image,
    Tasks.zero_shot_image_classification,
    Tasks.text_generation,
    Tasks.feature_extraction,
    Tasks.image_classification,
    Tasks.image_to_text,
    Tasks.text2text_generation,
    Tasks.token_classification,
    Tasks.fill_mask,
    Tasks.question_answering,
    Tasks.summarization,
    Tasks.table_question_answering,
    Tasks.translation,
]


ENV_VARS_TRUE_VALUES = {"1", "ON", "YES", "TRUE"}
DEFAULT_FLAGS = os.O_WRONLY | os.O_CREAT
DEFAULT_MODES = stat.S_IWUSR | stat.S_IRUSR
LOG_CONTENT_BLACK_LIST = [
    "\r",
    "\n",
    "\t",
    "\f",
    "\v",
    "\b",
    "\u000A",
    "\u000D",
    "\u000C",
    "\u000B",
    "\u0008",
    "\u007F",
    "\u0009",
]
BLANKS = "    "
DEFAULT_TIMEOUT = 100

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(file_path, "public_address_lib.json"), "r") as cfg_file:
    json_file = cfg_file.read()
    MINDSPORE_INSTALL_URL = json.loads(json_file)["mindspore_url"]
    OPENMIND_URL = json.loads(json_file)["openmind_url"]
    OPENMIND_MODEL_URL = json.loads(json_file)["openmind_model_url"]
    OPENMIND_DATASET_DOWNLOAD_URL = json.loads(json_file)["openmind_dataset_download_url"]
    PT_NN_MODULE_URL = json.loads(json_file)["pt_nn_module_url"]
    HUGGINGFACE_CHAT_URL = json.loads(json_file)["huggingface_chat_url"]
    LLAMA_ADDRESS_URL = json.loads(json_file)["llama_address_url"]
    BART_PAPER_URL = json.loads(json_file)["bart_paper_url"]
    LLAMA_TOKENIZER_CONFIG_URL = json.loads(json_file)["llama_tokenizer_config_url"]
    LLAMA_TOKENIZER_MODEL_URL = json.loads(json_file)["llama_tokenizer_model_url"]
    LEGACY_PARAS_URL = json.loads(json_file)["legacy_paras_url"]
    PYTORCH_INSTALL_URL = json.loads(json_file)["pytorch_install_url"]
    MISTRAL_REPO_URL = json.loads(json_file)["mistral_repo_url"]
    URL_PATTERN = rf'^{json.loads(json_file)["openmind_api_url"]}([^/]+)/([^/]+)/([^/]+)/media/(.*)'
    OPENMIND_PREFIX = json.loads(json_file)["openmind_prefix"]
    HUGGINGFACE_MODEL_URL = json.loads(json_file)["huggingface_model_url"]

GB = 1024**3
GIT = ".git"
GIT_LOGS_HEAD = ".git/logs/HEAD"
SNAPSHOTS = "snapshots"
MODEL_CONFIG = "config.json"

# key in args for storing dynamic argument
DYNAMIC_ARG = "_dynamic_arg"

# key in args for storing specified arguments
SPECIFIED_ARGS = "_specified_args"

# default model path in docker
OPENMIND_CACHE_IN_DOCKER = "/home/openmind/models"

# default ge_config path in docker
GE_CONFIG_IN_DOCKER = "/home/openmind/ge_config"

PYTORCH_IN_TAG = "pytorch"
MINDSPORE_IN_TAG = "mindspore"

METADATA_EXTRA_INFO = {"python", "hardware", "pytorch", "mindspore", "cann", "openmind"}
DOCKER_TAG_PARRETN = r"^openeuler-python3\.(8|9|10)-(cann)?(.*?)(mindspore)?(.*?)(pytorch)?(.*?)openmind(.*?)$"

# default template name for corresponding model
CHAT_MODEL_TEMPLATE_MAPPINGS = {
    "Baichuan/Baichuan2_7b_chat_pt": "baichuan2",
    "PyTorch-NPU/chatglm3_6b": "chatglm3",
    "AI-Research/glm-4-9b-chat": "glm4",
    "AI-Research/Qwen2.5-7B-Instruct": "qwen",
}
