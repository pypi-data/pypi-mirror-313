# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Alibaba, Inc. and its affiliates.  All rights reserved.
#
# Adapted from
# https://github.com/modelscope/modelscope/blob/v1.14.0/modelscope/msdatasets/ms_dataset.py
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

import enum
import os
from typing import Mapping, Optional, Sequence, Union
from packaging import version

import openmind_hub
import datasets
from .datasets_util import load_dataset_with_ctx
from ..utils import replace_invalid_characters
from ..utils.logging import get_logger
from ..utils.hub import OM_DATASETS_CACHE

logger = get_logger()


class DownloadMode(enum.Enum):
    """How to treat existing datasets"""

    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"


class OmDataset:
    @staticmethod
    def load_dataset(
        path: Optional[str] = None,
        name: Optional[str] = None,
        revision: Optional[str] = "main",
        split: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
        download_mode: Optional[DownloadMode] = DownloadMode.REUSE_DATASET_IF_EXISTS,
        cache_dir: Optional[str] = None,
        token: Optional[str] = None,
        dataset_info_only: Optional[bool] = False,
        trust_remote_code: bool = None,
        streaming: bool = False,
        **config_kwargs,
    ):

        current_version = datasets.__version__
        min_version = version.parse("2.18.0")
        max_version = version.parse("2.21.0")
        current_version_parsed = version.parse(current_version)

        if current_version_parsed > max_version or current_version_parsed < min_version:
            raise ImportError(
                replace_invalid_characters(f"supported datasets versions are between {min_version} and {max_version}")
            )

        if not isinstance(path, str):
            raise ValueError(replace_invalid_characters(f"path must be `str` , but got {type(path)}"))

        is_local_path = os.path.exists(path)

        if not is_local_path and path.count("/") != 1:
            raise ValueError("The path should be in the form of `namespace/datasetname` or local path")
        elif is_local_path:
            logger.info("Using local dataset")
        else:
            try:
                openmind_hub.repo_info(repo_id=path, repo_type="dataset", token=token)
            except Exception:
                raise ValueError(
                    "The path is not valid `namespace/datasetname`, or not valid local path, or token is necessary for private repo"
                )

        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)

        if not cache_dir:
            cache_dir = OM_DATASETS_CACHE

        with load_dataset_with_ctx(
            path=path,
            name=name,
            data_dir=data_dir,
            data_files=data_files,
            split=split,
            cache_dir=cache_dir,
            features=None,
            download_config=None,
            download_mode=download_mode.value,
            revision=revision,
            token=token,
            dataset_info_only=dataset_info_only,
            trust_remote_code=trust_remote_code,
            streaming=streaming,
            **config_kwargs,
        ) as dataset_res:
            return dataset_res
