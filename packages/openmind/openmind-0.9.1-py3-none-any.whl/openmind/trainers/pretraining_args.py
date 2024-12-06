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

import dataclasses
from dataclasses import dataclass, field
import re

import torch
import yaml

from .pretrainer_utils import print_in_main_process
from ..utils.generic import replace_invalid_characters


_dtype_map = {"bf16": torch.bfloat16, "fp16": torch.float16, "fp32": torch.float32}


@dataclass
class PreTrainingArguments:
    num_training_steps: int = field(metadata={"help": "Total number fo steps to train the model."})
    micro_batch_size: int = field(metadata={"help": "Batch size per model instance."})
    dp: int = field(metadata={"help": "Degree of Parallelism."})
    gradient_accumulation_steps: int = field(
        default=1, metadata={"help": "The number of gradient steps to accumulate before updating the model parameters."}
    )
    seq_length: int = field(default=None, metadata={"help": "Maximum sequence length to process."})
    megatron_dataset_flag: bool = field(
        default=None, metadata={"help": "Flags for whether or not to use a Megatron type dataset."}
    )
    data_path: str = field(default=None, metadata={"help": "Path to the training dataset."})
    save_dir: str = field(default=None, metadata={"help": "Output directory to save checkpoints to."})
    save_interval: int = field(default=None, metadata={"help": "Number of iterations between checkpoint saves."})
    eval_interval: int = field(
        default=None, metadata={"help": "Interval between running evaluation on validation set."}
    )
    openmind_model_path: str = field(default=None, metadata={"help": "The path of the Openmind model to be trained."})
    dtype: str = field(default="bf16", metadata={"help": "The dtype mode that the model is running on."})
    plugin_args: dict = field(default=None, metadata={"help": "Parameters related to accelerate plugins."})
    dataloader_config: dict = field(default=None, metadata={"help": "The parameters of dataloader."})
    report_to: str = field(default=None, metadata={"help": "Whom will accelerate report the log to."})
    project_name: str = field(default="accelerate-megatron", metadata={"help": "The name of the project"})

    @staticmethod
    def from_yaml(config_path: str):
        with open(config_path, "r") as file:
            config_data = yaml.safe_load(file)
        return PreTrainingArguments(**config_data)

    def __post_init__(self):
        self.batch_size = self.micro_batch_size * self.gradient_accumulation_steps * self.dp
        if self.data_path is not None and self.megatron_dataset_flag is None:
            raise ValueError(
                "Since you filled in data_path in PreTrainArguments, you have to specify the "
                "megatron_dataset_flag parameter at the same time."
            )

        self.dtype = self.dtype.lower()
        if self.dtype not in _dtype_map:
            error_msg = f"Unknown dtype:{self.dtype}. Supported dtypes:{','.join(_dtype_map.keys())}"
            raise ValueError(replace_invalid_characters(error_msg))

        for f in dataclasses.fields(self):
            value = getattr(self, f.name)
            if value:
                if f.type is str:
                    if re.match(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)$", value):
                        setattr(self, f.name, float(value))
                        print_in_main_process(
                            f"WARNING: PreTrainingArguments transferring the type of {f.name} from str to float!"
                        )
                if f.type is dict:
                    self._scientific_str_to_float(value)

    def get_mixed_precision(self):
        if self.dtype == "fp32":
            return "no"
        return self.dtype

    def get_torch_dtype(self):
        return _dtype_map.get(self.dtype)

    def get_distributed_train_args(self):
        return self.plugin_args.copy()

    def update_distributed_train_args(self, extra_args: dict):
        self.plugin_args.update(extra_args)

    def get_dataloader_config(self):
        return self.dataloader_config.copy()

    def _scientific_str_to_float(self, config_dict: dict):
        for key, value in config_dict.items():
            if isinstance(value, str):
                if re.match(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)$", value):
                    config_dict[key] = float(value)
                    print_in_main_process(
                        f"WARNING: PreTrainingArguments transferring the type of {key} from str to float!"
                    )
            if isinstance(value, dict):
                self._scientific_str_to_float(value)
