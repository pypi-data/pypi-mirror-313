# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.
# Copyright 2022 The HuggingFace Team. All rights reserved.
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
import gc
from abc import ABC
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Dict, Optional, Union
from uuid import uuid4
import warnings

from openmind_hub import (
    _CACHED_NO_EXIST,
    OM_HOME,
    OM_HUB_CACHE,
    REGEX_COMMIT_HASH,
    CommitOperationAdd,
    create_branch,
    create_commit,
    create_repo,
    http_get,
    om_hub_download,
    om_hub_url,
    try_to_load_from_cache,
)
from openmind_hub import upload_folder
from openmind_hub import snapshot_download
from openmind_hub import model_info, get_model_ci_info
from openmind_hub import (
    EntryNotFoundError,
    GatedRepoError,
    LocalEntryNotFoundError,
    OMValidationError,
    RepositoryNotFoundError,
    RevisionNotFoundError,
    build_om_headers,
    om_raise_for_status,
)
import requests
from requests import HTTPError

from .. import __version__
from ..utils import logging
from ..utils.constants import (
    ENV_VARS_TRUE_VALUES,
    OPENMIND_MODEL_URL,
    OPENMIND_URL,
    URL_PATTERN,
    HubName,
)
from ..utils.generic import working_or_temp_dir, replace_invalid_characters
from ..utils.import_utils import is_torch_available
from ..utils.logging import tqdm

logger = logging.get_logger(__name__)  # pylint: disable=invalid-name

_HUB_CLIENT = None
SESSION_ID = uuid4().hex
PYTORCH_PRETRAINED_BERT_CACHE = os.getenv("PYTORCH_PRETRAINED_BERT_CACHE", OM_HUB_CACHE)
PYTORCH_OPENMIND_CACHE = os.getenv("PYTORCH_OPENMIND_CACHE", PYTORCH_PRETRAINED_BERT_CACHE)
OPENMIND_DYNAMIC_MODULE_NAME = "openmind_modules"
_is_offline_mode = True if os.environ.get("OPENMIND_OFFLINE", "0").upper() in ENV_VARS_TRUE_VALUES else False
_default_endpoint = OPENMIND_URL

OPENMIND_CACHE = os.getenv("OPENMIND_CACHE", OM_HUB_CACHE)
OPENMIND_RESOLVE_ENDPOINT = os.environ.get("OM_ENDPOINT", _default_endpoint)
OM_MODULES_CACHE = os.getenv("OM_MODULES_CACHE", os.path.join(OM_HOME, "modules"))
OM_DATASETS_CACHE = os.path.join(OM_HOME, "datasets")


def is_offline_mode():
    return _is_offline_mode


class BaseHub(ABC):
    @staticmethod
    def http_user_agent(user_agent: Union[Dict, str, None] = None):
        raise NotImplementedError()

    @staticmethod
    def get_file_from_repo(
        path_or_repo: Union[str, os.PathLike],
        filename: str,
        cache_dir: Optional[Union[str, os.PathLike]] = None,
        force_download: bool = False,
        resume_download: bool = False,
        proxies: Optional[Dict[str, str]] = None,
        token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        local_files_only: bool = False,
        subfolder: str = "",
        **deprecated_kwargs,
    ):
        raise NotImplementedError()

    @staticmethod
    def cached_file(
        path_or_repo_id: Union[str, os.PathLike],
        filename: str,
        cache_dir: Optional[Union[str, os.PathLike]] = None,
        force_download: bool = False,
        resume_download: bool = False,
        proxies: Optional[Dict[str, str]] = None,
        token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        local_files_only: bool = False,
        subfolder: str = "",
        repo_type: Optional[str] = None,
        user_agent: Optional[Union[str, Dict[str, str]]] = None,
        _raise_exceptions_for_missing_entries: bool = True,
        _raise_exceptions_for_connection_errors: bool = True,
        _commit_hash: Optional[str] = None,
        **deprecated_kwargs,
    ):
        raise NotImplementedError()

    @staticmethod
    def download_url(url, proxies=None):
        raise NotImplementedError()

    @staticmethod
    def has_file(
        path_or_repo: Union[str, os.PathLike],
        filename: str,
        revision: Optional[str] = None,
        proxies: Optional[Dict[str, str]] = None,
        token: Optional[Union[bool, str]] = None,
        **deprecated_kwargs,
    ):
        raise NotImplementedError()

    @staticmethod
    def get_checkpoint_shard_files(
        pretrained_model_name_or_path: Union[str, os.PathLike],
        index_filename: Union[str, os.PathLike],
        cache_dir: Union[str, os.PathLike] = None,
        force_download: bool = False,
        proxies: Optional[str] = None,
        resume_download: bool = False,
        local_files_only: bool = False,
        token: Optional[str] = None,
        user_agent: Optional[Union[str, Dict[str, str]]] = None,
        revision: Optional[str] = None,
        subfolder: str = "",
        _commit_hash: Optional[str] = None,
        **deprecated_kwargs,
    ):
        raise NotImplementedError()

    @staticmethod
    def get_all_cached_files():
        raise NotImplementedError()

    @staticmethod
    def upload_folder(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def snapshot_download(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def create_repo(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def get_model_info(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def get_model_ci_info(*args, **kwargs):
        raise NotImplementedError()


class OpenMindHub(BaseHub):
    @staticmethod
    def download_url(url, proxies=None):
        """
        Downloads a given url in a temporary file. This function is not safe to use in multiple processes.
        Its only use is for deprecated behavior allowing to download config/models with a single url instead
        of using the Hub.

        Args:
            url (`str`): The url of the file to download.
            proxies (`Dict[str, str]`, *optional*):
                A dictionary of proxy servers to use by protocol or endpoint. The proxies are used on each request.

        Returns:
            `str`: The location of the temporary file where the url was downloaded.
        """
        warnings.warn(
            f"Using `from_pretrained` with the url of a file (here {url}) is deprecated. You should host your file "
            f"on the Hub instead and use the repository ID. Note"
            " that this is not compatible with the caching system (your file will be downloaded at each execution) or"
            " multiple processes (each process will download the file in a different temporary file).",
            FutureWarning,
        )

        dir_name = os.path.join(OM_HOME, "tmp_files_from_url")
        os.makedirs(dir_name, exist_ok=True)

        with tempfile.NamedTemporaryFile(dir=dir_name, delete=False) as temp_file:
            http_get(url, temp_file, proxies=proxies)
            tmp_file = temp_file.name
            logger.info(f"Downloading temporary file into {tmp_file} from url {url}")
        return tmp_file

    @staticmethod
    def http_user_agent(user_agent: Union[Dict, str, None] = None) -> str:
        """
        Formats a user-agent string with basic info about a request.
        """
        ua = f"openmind/{__version__}; python/{sys.version.split()[0]}; session_id/{SESSION_ID}"
        if is_torch_available():
            import torch

            ua += f"; torch/{torch.__version__}"
        if isinstance(user_agent, dict):
            ua += "; " + "; ".join(f"{k}/{v}" for k, v in user_agent.items())
        elif isinstance(user_agent, str):
            ua += "; " + user_agent
        return ua

    @staticmethod
    def get_checkpoint_shard_files(
        pretrained_model_name_or_path: Union[str, os.PathLike],
        index_filename: Union[str, os.PathLike],
        cache_dir: Union[str, os.PathLike] = None,
        force_download: bool = False,
        proxies: Optional[str] = None,
        resume_download: bool = False,
        local_files_only: bool = False,
        token: Optional[str] = None,
        user_agent: Optional[Union[str, Dict[str, str]]] = None,
        revision: Optional[str] = None,
        subfolder: str = "",
        _commit_hash: Optional[str] = None,
        **deprecated_kwargs,
    ):
        """
        For a given model:

        - download and cache all the shards of a sharded checkpoint if `pretrained_model_name_or_path` is a
         model ID on the
          Hub
        - returns the list of paths to all the shards, as well as some metadata.

        For the description of each arg, see [`PreTrainedModel.from_pretrained`]. `index_filename` is the full
        path to the
        index (downloaded and cached if `pretrained_model_name_or_path` is a model ID on the Hub).
        """
        if not os.path.isfile(index_filename):
            error_msg = f"Can't find a checkpoint index ({index_filename}) in {pretrained_model_name_or_path}."
            raise ValueError(replace_invalid_characters(error_msg))
        with open(index_filename, "r") as f:
            index = json.loads(f.read())

        shard_filenames = sorted(set(index["weight_map"].values()))
        sharded_metadata = index["metadata"]
        sharded_metadata["all_checkpoint_keys"] = list(index["weight_map"].keys())
        sharded_metadata["weight_map"] = index["weight_map"].copy()

        # First, let's deal with local folder.
        if os.path.isdir(pretrained_model_name_or_path):
            shard_filenames = [os.path.join(pretrained_model_name_or_path, subfolder, f) for f in shard_filenames]
            return shard_filenames, sharded_metadata

        # At this stage pretrained_model_name_or_path is a model identifier on the Hub
        cached_filenames = []
        # Check if the model is already cached or not. We only try the last checkpoint, this should cover most cases of
        # downloaded (if interrupted).
        last_shard = try_to_load_from_cache(
            pretrained_model_name_or_path, shard_filenames[-1], cache_dir=cache_dir, revision=_commit_hash
        )
        show_progress_bar = last_shard is None or force_download
        for shard_filename in tqdm(shard_filenames, desc="Downloading shards", disable=not show_progress_bar):
            try:
                # Load from URL
                cached_filename = OpenMindHub.cached_file(
                    pretrained_model_name_or_path,
                    shard_filename,
                    cache_dir=cache_dir,
                    force_download=force_download,
                    proxies=proxies,
                    resume_download=resume_download,
                    local_files_only=local_files_only,
                    token=token,
                    user_agent=user_agent,
                    revision=revision,
                    subfolder=subfolder,
                    _commit_hash=_commit_hash,
                )
            except EntryNotFoundError as e:
                if token:
                    del token
                    gc.collect()
                error_msg = (
                    f"{pretrained_model_name_or_path} does not appear to have a file named "
                    f"{shard_filename} which is required according to the checkpoint index."
                )
                raise EnvironmentError(replace_invalid_characters(error_msg)) from e
            except HTTPError as e:
                if token:
                    del token
                    gc.collect()
                error_msg = (
                    f"We couldn't connect to '{OPENMIND_RESOLVE_ENDPOINT}' to load "
                    f"{shard_filename}. You should try again after checking your internet connection."
                )
                raise EnvironmentError(replace_invalid_characters(error_msg)) from e

            cached_filenames.append(cached_filename)

        del token
        gc.collect()

        return cached_filenames, sharded_metadata

    @staticmethod
    def cached_file(
        path_or_repo_id: Union[str, os.PathLike],
        filename: str,
        cache_dir: Optional[Union[str, os.PathLike]] = None,
        force_download: bool = False,
        resume_download: bool = False,
        proxies: Optional[Dict[str, str]] = None,
        token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        local_files_only: bool = False,
        subfolder: str = "",
        repo_type: Optional[str] = None,
        user_agent: Optional[Union[str, Dict[str, str]]] = None,
        _raise_exceptions_for_missing_entries: bool = True,
        _raise_exceptions_for_connection_errors: bool = True,
        _commit_hash: Optional[str] = None,
        **deprecated_kwargs,
    ) -> Optional[str]:
        """
        Tries to locate a file in a local folder and repo, downloads and cache it if necessary.

        Args:
            path_or_repo_id (`str` or `os.PathLike`):
                This can be either:
                - a string, the *model id* of a model repo on openmind.
                - a path to a *directory* potentially containing the file.
            filename (`str`):
                The name of the file to locate in `path_or_repo`.
            cache_dir (`str` or `os.PathLike`, *optional*):
                Path to a directory in which a downloaded pretrained model configuration should be cached if the
                standard cache should not be used.
            force_download (`bool`, *optional*, defaults to `False`):
                Whether or not to force to (re-)download the configuration files and override the cached versions
                if they exist.
            resume_download (`bool`, *optional*, defaults to `False`):
                Whether or not to delete incompletely received file. Attempts to resume the download if such a
                file exists.
            proxies (`Dict[str, str]`, *optional*):
                A dictionary of proxy servers to use by protocol or endpoint. The proxies are used on each request.
            token (`str` or *bool*, *optional*):
                The token to use as HTTP bearer authorization for remote files.
            revision (`str`, *optional*, defaults to `"main"`):
                The specific model version to use. It can be a branch name, a tag name, or a commit id,
                since we use a git-based system for storing models and other artifacts on modelers.cn,
                so `revision` can be any identifier allowed by git.
            local_files_only (`bool`, *optional*, defaults to `False`):
                If `True`, will only try to load the tokenizer configuration from local files.
            subfolder (`str`, *optional*, defaults to `""`):
                In case the relevant files are located inside a subfolder of the model repo on modelers.cn,
                you can specify the folder name here.
            repo_type (`str`, *optional*):
                Specify the repo type (useful when downloading from a space for instance).

        <Tip>

        Passing `token=True` is required when you want to use a private model.

        </Tip>

        Returns:
            `Optional[str]`: Returns the resolved file (to the cache folder if downloaded from a repo).

        Examples:

        ```python
        # Download a model weight from the Hub and cache it.
        model_weights_file = cached_file("PyTorch-NPU/bert_base_uncased", "pytorch_model.bin")
        ```
        """
        if is_offline_mode() and not local_files_only:
            logger.info("Offline mode: forcing local_files_only=True")
            local_files_only = True
        if subfolder is None:
            subfolder = ""

        path_or_repo_id = str(path_or_repo_id)
        full_filename = os.path.join(subfolder, filename)
        if os.path.isdir(path_or_repo_id):
            resolved_file = os.path.join(os.path.join(path_or_repo_id, subfolder), filename)
            if not os.path.isfile(resolved_file):
                if _raise_exceptions_for_missing_entries:
                    error_msg = (
                        f"{path_or_repo_id} does not appear to have a file named {full_filename}. "
                        f"Checkout '{OPENMIND_URL}/{path_or_repo_id}/{revision}' for available files."
                    )
                    raise EnvironmentError(replace_invalid_characters(error_msg))
                else:
                    return None
            return resolved_file

        if cache_dir is None:
            cache_dir = OPENMIND_CACHE
        if isinstance(cache_dir, Path):
            cache_dir = str(cache_dir)

        if _commit_hash is not None and not force_download:
            # If the file is cached under that commit hash, we return it directly.
            # NOTE param `repo_type` is not supported now, remove it temporary
            resolved_file = try_to_load_from_cache(
                path_or_repo_id,
                full_filename,
                cache_dir=cache_dir,
                revision=_commit_hash,
            )
            if resolved_file is not None:
                if resolved_file is not _CACHED_NO_EXIST:
                    return resolved_file
                elif not _raise_exceptions_for_missing_entries:
                    return None
                else:
                    error_msg = f"Could not locate {full_filename} inside {path_or_repo_id}."
                    raise EnvironmentError(replace_invalid_characters(error_msg))

        user_agent = OpenMindHub.http_user_agent(user_agent)  # noqa

        try:
            # Load from URL or cache if already cached
            resolved_file = om_hub_download(
                path_or_repo_id,
                filename,
                subfolder=None if not subfolder else subfolder,
                repo_type=repo_type,
                revision=revision,
                cache_dir=cache_dir,
                user_agent=user_agent,
                force_download=force_download,
                proxies=proxies,
                resume_download=resume_download,
                token=token,
                local_files_only=local_files_only,
            )

        except GatedRepoError as e:
            if token:
                del token
                gc.collect()
            error_msg = (
                f"You are trying to access a gated repo. Make sure to request access at "
                f"{OPENMIND_URL}/{path_or_repo_id} and pass a token having permission to "
                f"this repo by passing `token=<your_token>`."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except RepositoryNotFoundError as e:
            if token:
                del token
                gc.collect()
            error_msg = (
                f"{path_or_repo_id} is not a local folder and is not a valid model identifier listed "
                f"on {OPENMIND_MODEL_URL}. If this is a private repository, make sure to pass a token "
                f"having permission to this repo by passing `token=<your_token>`"
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except RevisionNotFoundError as e:
            if token:
                del token
                gc.collect()
            error_msg = (
                f"{revision} is not a valid git identifier (branch name, tag name or commit id) that "
                f"exists for this model name. Check the model page at '{OPENMIND_URL}/{path_or_repo_id}' "
                f"for available revisions."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except LocalEntryNotFoundError as e:
            if token:
                del token
                gc.collect()
            # We try to see if we have a cached version (not up to date):
            resolved_file = try_to_load_from_cache(
                path_or_repo_id, full_filename, cache_dir=cache_dir, revision=revision
            )
            if resolved_file is not None and resolved_file != _CACHED_NO_EXIST:
                return resolved_file
            if not _raise_exceptions_for_missing_entries or not _raise_exceptions_for_connection_errors:
                return None
            error_msg = (
                f"We couldn't connect to '{OPENMIND_RESOLVE_ENDPOINT}' to load this file, couldn't find "
                f"it in the cached files and it looks like {path_or_repo_id} is not the path to a directory "
                f"containing a file named {full_filename}. Checkout your internet connection."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except EntryNotFoundError as e:
            if token:
                del token
                gc.collect()
            if not _raise_exceptions_for_missing_entries:
                return None
            if revision is None:
                revision = "main"
            error_msg = (
                f"{path_or_repo_id} does not appear to have a file named {full_filename}. "
                f"Checkout '{OPENMIND_URL}/{path_or_repo_id}/{revision}' for available files."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except HTTPError as e:
            if token:
                del token
                gc.collect()
            # First we try to see if we have a cached version (not up to date):
            resolved_file = try_to_load_from_cache(
                path_or_repo_id, full_filename, cache_dir=cache_dir, revision=revision
            )
            if resolved_file is not None and resolved_file != _CACHED_NO_EXIST:
                return resolved_file
            if not _raise_exceptions_for_connection_errors:
                return None

            error_msg = f"There was a specific connection error when trying to load {path_or_repo_id}:{e}"
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except OMValidationError as e:
            if token:
                del token
                gc.collect()
            error_msg = (
                f"Incorrect path_or_model_id: '{path_or_repo_id}'. Please provide either the path to "
                f"a local folder or the repo_id of a model on the Hub."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e

        del token
        gc.collect()

        return resolved_file

    @staticmethod
    def get_file_from_repo(
        path_or_repo: Union[str, os.PathLike],
        filename: str,
        cache_dir: Optional[Union[str, os.PathLike]] = None,
        force_download: bool = False,
        resume_download: bool = False,
        proxies: Optional[Dict[str, str]] = None,
        token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        local_files_only: bool = False,
        subfolder: str = "",
        **deprecated_kwargs,
    ):
        """
        Tries to locate a file in a local folder and repo, downloads and cache it if necessary.

        Args:
            path_or_repo (`str` or `os.PathLike`):
                This can be either:

                - a string, the *model id* of a model repo on modelers.cn.
                - a path to a *directory* potentially containing the file.
            filename (`str`):
                The name of the file to locate in `path_or_repo`.
            cache_dir (`str` or `os.PathLike`, *optional*):
                Path to a directory in which a downloaded pretrained model configuration should be cached if the
                standard cache should not be used.
            force_download (`bool`, *optional*, defaults to `False`):
                Whether or not to force to (re-)download the configuration files and override the cached versions
                if they exist.
            resume_download (`bool`, *optional*, defaults to `False`):
                Whether or not to delete incompletely received file. Attempts to resume the download if such
                a file exists.
            proxies (`Dict[str, str]`, *optional*):
                A dictionary of proxy servers to use by protocol or endpoint. The proxies are used on each request.
            token (`str` or *bool*, *optional*):
                The token to use as HTTP bearer authorization for remote files.
            revision (`str`, *optional*, defaults to `"main"`):
                The specific model version to use. It can be a branch name, a tag name, or a commit id, since we use a
                git-based system for storing models and other artifacts on openmind, so `revision` can be any
                identifier allowed by git.
            local_files_only (`bool`, *optional*, defaults to `False`):
                If `True`, will only try to load the tokenizer configuration from local files.
            subfolder (`str`, *optional*, defaults to `""`):
                In case the relevant files are located inside a subfolder of the model repo on openmind, you can
                specify the folder name here.

        <Tip>

        Passing `token=True` is required when you want to use a private model.

        </Tip>

        Returns:
            `Optional[str]`: Returns the resolved file (to the cache folder if downloaded from a repo) or `None` if the
            file does not exist.

        Examples:

        ```python
        >>> # Download a tokenizer configuration from modelers.cn and cache.
        >>> tokenizer_config = get_file_from_repo("PyTorch-NPU/bert_base_uncased", "tokenizer_config.json")
        >>> # This model does not have a tokenizer config so the result will be None.
        >>> tokenizer_config = get_file_from_repo("PyTorch-NPU/resnet_50", "tokenizer_config.json")
        ```
        """
        rsp = OpenMindHub.cached_file(
            path_or_repo_id=path_or_repo,
            filename=filename,
            cache_dir=cache_dir,
            force_download=force_download,
            resume_download=resume_download,
            proxies=proxies,
            token=token,
            revision=revision,
            local_files_only=local_files_only,
            subfolder=subfolder,
            _raise_exceptions_for_missing_entries=False,
            _raise_exceptions_for_connection_errors=False,
        )

        del token
        gc.collect()

        return rsp

    @staticmethod
    def has_file(
        path_or_repo: Union[str, os.PathLike],
        filename: str,
        revision: Optional[str] = None,
        proxies: Optional[Dict[str, str]] = None,
        token: Optional[Union[bool, str]] = None,
        **deprecated_kwargs,
    ):
        """
        Checks if a repo contains a given file without downloading it. Works for remote repos and local folders.

        <Tip warning={false}>

        This function will raise an error if the repository `path_or_repo` is not valid or if `revision` does not exist
        for this repo, but will return False for regular connection errors.

        </Tip>
        """
        if os.path.isdir(path_or_repo):
            return os.path.isfile(os.path.join(path_or_repo, filename))

        url = om_hub_url(path_or_repo, filename=filename, revision=revision)
        headers = build_om_headers(token=token, user_agent=OpenMindHub.http_user_agent())

        del token
        gc.collect()

        r = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies, timeout=10)
        try:
            om_raise_for_status(r)
            return True
        except GatedRepoError as e:
            logger.error(e)
            error_msg = (
                f"{path_or_repo} is a gated repository. Make sure to request access at "
                f"{OPENMIND_URL}/{path_or_repo} and pass a token having permission to this repo "
                f"by passing `token=<your_token>`."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except RepositoryNotFoundError as e:
            logger.error(e)
            error_msg = f"{path_or_repo} is not a local folder or a valid repository name on {OPENMIND_URL}."
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except RevisionNotFoundError as e:
            logger.error(e)
            error_msg = (
                f"{revision} is not a valid git identifier (branch name, tag name or commit id) that exists "
                f"for this model name. Check the model page at '{OPENMIND_URL}/{path_or_repo}' "
                f"for available revisions."
            )
            raise EnvironmentError(replace_invalid_characters(error_msg)) from e
        except requests.HTTPError:
            # We return false for EntryNotFoundError (logical) as well as any connection error.
            return False

    @staticmethod
    def upload_folder(*args, **kwargs):
        return upload_folder(*args, **kwargs)

    @staticmethod
    def snapshot_download(*args, **kwargs):
        return snapshot_download(*args, **kwargs)

    @staticmethod
    def create_repo(*args, **kwargs):
        return create_repo(*args, **kwargs)

    @staticmethod
    def get_task_from_repo(repo_id, token=None):
        rsp = model_info(repo_id=repo_id, token=token)
        return rsp.pipeline_tag

    @staticmethod
    def get_model_info(*args, **kwargs):
        return model_info(*args, **kwargs)

    @staticmethod
    def get_model_ci_info(*args, **kwargs):
        return get_model_ci_info(*args, **kwargs)


class PushToHubMixin:
    """
    A Mixin containing the functionality to push a model or tokenizer to the hub.
    """

    def push_to_hub(
        self,
        repo_id: str,
        use_temp_dir: Optional[bool] = None,
        commit_message: Optional[str] = None,
        private: Optional[bool] = None,
        token: Optional[Union[bool, str]] = None,
        max_shard_size: Optional[Union[int, str]] = "5GB",
        safe_serialization: bool = True,
        revision: Optional[str] = None,
        commit_description: Optional[str] = None,
        **deprecated_kwargs,
    ) -> str:
        """
        Upload the {object_files} to the openMind Model Hub.

        Parameters:
            repo_id (`str`):
                The name of the repository you want to push your {object} to. It should contain your organization name
                when pushing to a given organization.
            use_temp_dir (`bool`, *optional*):
                Whether to use a temporary directory to store the files saved before they are pushed to the Hub.
                Will default to `True` if there is no directory named like `repo_id`, `False` otherwise.
            commit_message (`str`, *optional*):
                Message to commit while pushing. Will default to `"Upload {object}"`.
            private (`bool`, *optional*):
                Whether the repository created should be private.
            token (`bool` or `str`, *optional*):
                The token to use as HTTP bearer authorization for remote files.
                Will default to `True` if `repo_url` is not specified.
            max_shard_size (`int` or `str`, *optional*, defaults to `"5GB"`):
                Only applicable for models. The maximum size for a checkpoint before being sharded. Checkpoints shard
                will then be each of size lower than this size. If expressed as a string, needs to be digits followed
                by a unit (like `"5MB"`). We default it to `"5GB"`.
            safe_serialization (`bool`, *optional*, defaults to `True`):
                Whether or not to convert the model weights in safetensors format for safer serialization.
            revision (`str`, *optional*):
                Branch to push the uploaded files to.
            commit_description (`str`, *optional*):
                The description of the commit that will be created

        Examples:

        ```python
        >>> from openmind import object_class

        >>> object = object_class.from_pretrained("PyTorch-NPU/bert_base_cased")

        >>> # Push the {object} to your namespace with the name "my-finetuned-bert".
        >>> object.push_to_hub("my-finetuned-bert")

        >>> # Push the {object} to an organization with the name "my-finetuned-bert".
        >>> object.push_to_hub("PyTorch-NPU/my-finetuned-bert")
        ```
        """
        working_dir = repo_id.split("/")[-1]

        repo_id = self._create_repo(
            repo_id,
            private=private,
            token=token,
        )

        if use_temp_dir is None:
            use_temp_dir = not os.path.isdir(working_dir)

        with working_or_temp_dir(working_dir=working_dir, use_temp_dir=use_temp_dir) as work_dir:
            files_timestamps = self._get_files_timestamps(work_dir)

            # Save all files.
            self.save_pretrained(work_dir, max_shard_size=max_shard_size, safe_serialization=safe_serialization)

            rsp = self._upload_modified_files(
                work_dir,
                repo_id,
                files_timestamps,
                commit_message=commit_message,
                token=token,
                revision=revision,
                commit_description=commit_description,
            )

            del token
            gc.collect()

            return rsp

    def _create_repo(
        self,
        repo_id: str,
        private: Optional[bool] = None,
        token: Optional[Union[bool, str]] = None,
    ) -> str:
        """
        Create the repo if needed, cleans up repo_id with deprecated kwargs `repo_url` and `organization`, retrieves
        the token.
        """
        url = create_repo(repo_id=repo_id, token=token, private=private, exist_ok=True)

        del token
        gc.collect()

        return url.repo_id

    def _get_files_timestamps(self, working_dir: Union[str, os.PathLike]):
        """
        Returns the list of files with their last modification timestamp.
        """
        return {f: os.path.getmtime(os.path.join(working_dir, f)) for f in os.listdir(working_dir)}

    def _upload_modified_files(
        self,
        working_dir: Union[str, os.PathLike],
        repo_id: str,
        files_timestamps: Dict[str, float],
        commit_message: Optional[str] = None,
        token: Optional[Union[bool, str]] = None,
        revision: str = None,
        commit_description: str = None,
    ):
        """
        Uploads all modified files in `working_dir` to `repo_id`, based on `files_timestamps`.
        """
        if commit_message is None:
            if "Model" in self.__class__.__name__:
                commit_message = "Upload model"
            elif "Config" in self.__class__.__name__:
                commit_message = "Upload config"
            elif "Tokenizer" in self.__class__.__name__:
                commit_message = "Upload tokenizer"
            elif "FeatureExtractor" in self.__class__.__name__:
                commit_message = "Upload feature extractor"
            elif "Processor" in self.__class__.__name__:
                commit_message = "Upload processor"
            else:
                commit_message = f"Upload {self.__class__.__name__}"
        modified_files = [
            f
            for f in os.listdir(working_dir)
            if f not in files_timestamps or os.path.getmtime(os.path.join(working_dir, f)) > files_timestamps[f]
        ]

        # filter for actual files + folders at the root level
        modified_files = [
            f
            for f in modified_files
            if os.path.isfile(os.path.join(working_dir, f)) or os.path.isdir(os.path.join(working_dir, f))
        ]

        operations = []
        # upload standalone files
        for file in modified_files:
            if os.path.isdir(os.path.join(working_dir, file)):
                # go over individual files of folder
                for f in os.listdir(os.path.join(working_dir, file)):
                    operations.append(
                        CommitOperationAdd(
                            path_or_fileobj=os.path.join(working_dir, file, f), path_in_repo=os.path.join(file, f)
                        )
                    )
            else:
                operations.append(
                    CommitOperationAdd(path_or_fileobj=os.path.join(working_dir, file), path_in_repo=file)
                )

        if revision is not None:
            create_branch(repo_id=repo_id, branch=revision, token=token, exist_ok=True)

        logger.info(f"Uploading the following files to {repo_id}: {','.join(modified_files)}")

        rsp = create_commit(
            repo_id=repo_id,
            operations=operations,
            commit_message=commit_message,
            commit_description=commit_description,
            token=token,
        )

        del token
        gc.collect()

        return rsp


_HUB_MAPPING = {HubName.openmind_hub: OpenMindHub}


def extract_info_from_url(url, pattern=URL_PATTERN):
    """
    Extract repo_name, revision and filename from an url.
    """
    search = re.search(pattern, url)
    if search is None:
        return None
    owner, repo, revision, filename = search.groups()
    cache_repo = "--".join(["models"] + repo.split("/"))
    return {"owner": owner, "repo": cache_repo, "revision": revision, "filename": filename}


def extract_commit_hash(resolved_file: Optional[str], commit_hash: Optional[str]) -> Optional[str]:
    """
    Extracts the commit hash from a resolved filename toward a cache file.
    """
    if resolved_file is None or commit_hash is not None:
        return commit_hash
    resolved_file = str(Path(resolved_file).as_posix())
    search = re.search(r"snapshots/([^/]+)/", resolved_file)
    if search is None:
        return None
    commit_hash = search.groups()[0]
    return commit_hash if REGEX_COMMIT_HASH.match(commit_hash) else None


def get_hub_client(hub_name=HubName.openmind_hub):
    global _HUB_CLIENT
    hub_class = _HUB_MAPPING.get(hub_name, None)
    if not hub_class:
        raise KeyError("Unknown Hub client， please make sure it's in openMind support list")
    if _HUB_CLIENT is not None and isinstance(_HUB_CLIENT, hub_class):
        return _HUB_CLIENT
    _HUB_CLIENT = hub_class()
    return _HUB_CLIENT


om_hub = get_hub_client()
