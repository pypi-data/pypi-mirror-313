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

import os
import yaml
import ast

from ..utils import replace_invalid_characters


def safe_load_yaml(path):
    if path is None:
        raise ValueError("param `path` is required for `safe_load_yaml` func.")

    if not isinstance(path, str):
        err_msg = f"param `path` should be string format for `safe_load_yaml func`, but got {type(path)} type."
        raise TypeError(replace_invalid_characters(err_msg))

    if not os.path.exists(path):
        err_msg = f"yaml file path {path} does not exist."
        raise FileNotFoundError(replace_invalid_characters(err_msg))

    path = os.path.realpath(path)

    if not path.endswith(".yaml") and not path.endswith(".yml"):
        err_msg = f"path {path} is not a yaml/yml file path."
        raise ValueError(replace_invalid_characters(err_msg))

    with open(path, "r") as file:
        content = yaml.safe_load(file)

    return content


def try_to_trans_to_bool(flag):
    # local_dir_use_symlinks can be str or bool
    try:
        output = ast.literal_eval(flag)
        return output if isinstance(output, bool) else flag
    except Exception:
        return flag


def try_to_trans_to_list(patterns):
    # allow_patterns/ignore_patterns can be str or List[str]
    try:
        output = ast.literal_eval(patterns)
        return output if isinstance(output, list) else patterns
    except Exception:
        return patterns


def try_to_trans_to_dict(input_or_path):
    # input_or_path can be prompt str or key-value str
    try:
        output = ast.literal_eval(input_or_path)
        return output if isinstance(output, dict) else input_or_path
    except Exception:
        return input_or_path
