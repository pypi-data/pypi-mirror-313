# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Alibaba, Inc. and its affiliates.  All rights reserved.
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
#
# Adapted from
# https://github.com/modelscope/modelscope/blob/v1.14.0/modelscope/msdatasets/utils/hf_datasets_util.py
# https://github.com/huggingface/datasets/blob/2.18.0/src/datasets
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

import contextlib
import importlib
import os
import warnings
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Union, Optional
import requests

from datasets import (
    BuilderConfig,
    Dataset,
    DatasetBuilder,
    DatasetDict,
    DownloadMode,
    Features,
    IterableDataset,
    IterableDatasetDict,
    Split,
    VerificationMode,
    Version,
)
from datasets.data_files import (
    DataFilesDict,
    DataFilesList,
    EmptyDatasetError,
    get_metadata_patterns,
    sanitize_patterns,
)
from datasets.exceptions import DataFilesNotFoundError, DatasetNotFoundError
from datasets.info import DatasetInfosDict
from datasets.load import (
    ALL_ALLOWED_EXTENSIONS,
    BuilderConfigsParameters,
    CachedDatasetModuleFactory,
    DatasetModule,
    HubDatasetModuleFactoryWithoutScript,
    HubDatasetModuleFactoryWithParquetExport,
    HubDatasetModuleFactoryWithScript,
    LocalDatasetModuleFactoryWithoutScript,
    LocalDatasetModuleFactoryWithScript,
    PackagedDatasetModuleFactory,
    create_builder_configs_from_metadata_configs,
    get_dataset_builder_class,
    import_main_class,
    infer_module_for_data_files,
    _download_additional_modules,
    files_to_hash,
    _get_importable_file_path,
    resolve_trust_remote_code,
    _create_importable_file,
    _load_importable_file,
    init_dynamic_modules,
)
from datasets.naming import camelcase_to_snakecase
from datasets.packaged_modules import (
    _EXTENSION_TO_MODULE,
    _MODULE_SUPPORTS_METADATA,
    _MODULE_TO_EXTENSIONS,
    _PACKAGED_DATASETS_MODULES,
)

# `_datasets_server` is renamed to `_dataset_viewer` since datasets 2.19.0
try:
    from datasets.utils._datasets_server import DatasetsServerError
except ImportError:
    from datasets.utils._dataset_viewer import DatasetViewerError

    DatasetsServerError = DatasetViewerError
from datasets.utils.file_utils import (
    OfflineModeIsEnabled,
    _raise_if_offline_mode_is_enabled,
    cached_path,
    is_relative_path,
    relative_to_absolute_path,
)
from datasets.utils.py_utils import get_imports
from datasets.utils.info_utils import is_small_dataset
from datasets.utils.metadata import MetadataConfigs
from datasets import config
from datasets.download.download_config import DownloadConfig
from datasets.data_files import get_data_patterns

import huggingface_hub
from huggingface_hub import DatasetCard, DatasetCardData
import openmind_hub
from openmind_hub import OmApi as HubApi
from ..utils.constants import OPENMIND_URL, OPENMIND_DATASET_DOWNLOAD_URL, DEFAULT_TIMEOUT
from ..utils import replace_invalid_characters
from ..utils.logging import get_logger
from ..utils.hub import OM_DATASETS_CACHE


logger = get_logger()


def download_loading_script_with_script(name, revision=None, download_config=None) -> str:
    file_path = openmind_hub.om_hub_url(name, name.split("/")[-1] + ".py", revision=revision)
    download_config = download_config.copy()
    if download_config.download_desc is None:
        download_config.download_desc = "Download builder script"
    return cached_path(url_or_filename=file_path, download_config=download_config)


def download_dataset_infos_file_with_script() -> str:
    return None


def download_dataset_readme_file_with_script(name, revision=None, download_config=None) -> str:
    dataset_readme_url: str = openmind_hub.om_hub_url(name, "README.md", revision=revision)
    return cached_path(url_or_filename=dataset_readme_url, download_config=download_config)


def get_module_with_script(self) -> DatasetModule:
    if config.HF_DATASETS_TRUST_REMOTE_CODE and self.trust_remote_code is None:
        warnings.warn(
            f"The repository for {self.name} contains custom code which must be executed to correctly load the dataset.\n"
            f"You can avoid this message in future by passing the argument `trust_remote_code=True`.\n"
            f"Passing `trust_remote_code=True` will be mandatory to load this dataset from the next major release of `datasets`.",
            FutureWarning,
        )
    # get script and other files
    local_path = download_loading_script_with_script(self.name, self.revision, self.download_config)
    dataset_infos_path = download_dataset_infos_file_with_script()
    dataset_readme_path = download_dataset_readme_file_with_script(self.name, self.revision, self.download_config)
    imports = get_imports(local_path)
    result = _download_additional_modules(
        name=self.name,
        base_path=openmind_hub.om_hub_url(self.name, "", revision=self.revision),
        imports=imports,
        download_config=self.download_config,
    )
    # from datasets 2.21.0, _download_additional_modules will return two values
    if isinstance(result, tuple) and len(result) == 2:
        local_imports, library_imports = result
    else:
        local_imports = result

    additional_files = []
    if dataset_infos_path:
        additional_files.append((config.DATASETDICT_INFOS_FILENAME, dataset_infos_path))
    if dataset_readme_path:
        additional_files.append((config.REPOCARD_FILENAME, dataset_readme_path))
    # copy the script and the files in an importable directory
    dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
    hash_info = files_to_hash([local_path] + [loc[1] for loc in local_imports])
    importable_file_path = _get_importable_file_path(
        dynamic_modules_path=dynamic_modules_path,
        module_namespace="datasets",
        subdirectory_name=hash_info,
        name=self.name,
    )
    if not os.path.exists(importable_file_path):
        trust_remote_code = resolve_trust_remote_code(self.trust_remote_code, self.name)
        if trust_remote_code:
            _create_importable_file(
                local_path=local_path,
                local_imports=local_imports,
                additional_files=additional_files,
                dynamic_modules_path=dynamic_modules_path,
                module_namespace="datasets",
                subdirectory_name=hash_info,
                name=self.name,
                download_mode=self.download_mode,
            )
        else:
            raise ValueError(
                f"Loading {self.name} requires you to execute the dataset script in that"
                " repo on your local machine. Make sure you have read the code there to avoid malicious use, then"
                " set the option `trust_remote_code=True` to remove this error."
            )
    module_path, hash_info = _load_importable_file(
        dynamic_modules_path=dynamic_modules_path,
        module_namespace="datasets",
        subdirectory_name=hash_info,
        name=self.name,
    )
    # make the new module to be noticed by the import system
    importlib.invalidate_caches()
    builder_kwargs = {
        "base_path": openmind_hub.om_hub_url(self.name, "", revision=self.revision).rstrip("/"),
        "repo_id": self.name,
    }
    return DatasetModule(module_path, hash_info, builder_kwargs)


def get_module_without_script(self) -> DatasetModule:
    revision = self.revision or "main"
    base_path = f"{OPENMIND_DATASET_DOWNLOAD_URL}/{self.name}@{revision}/{self.data_dir or ''}".rstrip("/")

    download_config = self.download_config.copy()
    if download_config.download_desc is None:
        download_config.download_desc = "Downloading readme"
    try:
        dataset_readme_path = cached_path(
            url_or_filename=openmind_hub.om_hub_url(self.name, "README.md", revision=revision),
            download_config=download_config,
        )
        dataset_card_data = DatasetCard.load(Path(dataset_readme_path)).data
    except FileNotFoundError:
        dataset_card_data = DatasetCardData()

    subset_name: str = download_config.storage_options.get("name", None)

    metadata_configs = MetadataConfigs.from_dataset_card_data(dataset_card_data)
    dataset_infos = DatasetInfosDict.from_dataset_card_data(dataset_card_data)

    if self.data_files is not None:
        patterns = sanitize_patterns(self.data_files)
    elif metadata_configs and not self.data_dir and "data_files" in next(iter(metadata_configs.values())):
        if subset_name is not None:
            subset_data_files = metadata_configs[subset_name]["data_files"]
        else:
            subset_data_files = next(iter(metadata_configs.values()))["data_files"]
        patterns = sanitize_patterns(subset_data_files)
    else:
        patterns = get_data_patterns(base_path, download_config=self.download_config)

    data_files = DataFilesDict.from_patterns(
        patterns,
        base_path=base_path,
        allowed_extensions=ALL_ALLOWED_EXTENSIONS,
        download_config=self.download_config,
    )

    module_name, default_builder_kwargs = infer_module_for_data_files(
        data_files=data_files,
        path=self.name,
        download_config=self.download_config,
    )
    data_files = data_files.filter_extensions(_MODULE_TO_EXTENSIONS[module_name])

    # Collect metadata files if the module supports them
    supports_metadata = module_name in _MODULE_SUPPORTS_METADATA
    if self.data_files is None and supports_metadata:
        try:
            metadata_patterns = get_metadata_patterns(base_path, download_config=self.download_config)
        except FileNotFoundError:
            metadata_patterns = None
        if metadata_patterns is not None:
            metadata_data_files_list = DataFilesList.from_patterns(
                metadata_patterns, download_config=self.download_config, base_path=base_path
            )
            if metadata_data_files_list:
                data_files = DataFilesDict(
                    {split: data_files_list + metadata_data_files_list for split, data_files_list in data_files.items()}
                )

    module_path, _ = _PACKAGED_DATASETS_MODULES[module_name]

    if metadata_configs:
        builder_configs, default_config_name = create_builder_configs_from_metadata_configs(
            module_path,
            metadata_configs,
            base_path=base_path,
            supports_metadata=supports_metadata,
            default_builder_kwargs=default_builder_kwargs,
            download_config=self.download_config,
        )
    else:
        builder_configs: List[BuilderConfig] = [
            import_main_class(module_path).BUILDER_CONFIG_CLASS(
                data_files=data_files,
                **default_builder_kwargs,
            )
        ]
        default_config_name = None

    builder_kwargs = {
        "base_path": openmind_hub.om_hub_url(self.name, "", revision=revision).rstrip("/"),
        "repo_id": self.name,
        "dataset_name": camelcase_to_snakecase(Path(self.name).name),
        "data_files": data_files,
    }
    download_config = self.download_config.copy()
    if download_config.download_desc is None:
        download_config.download_desc = "Downloading metadata"

    # Note: `dataset_infos.json` is deprecated and can cause an error during loading if it exists

    if default_config_name is None and len(dataset_infos) == 1:
        default_config_name = next(iter(dataset_infos))

    hash_info = revision
    return DatasetModule(
        module_path,
        hash_info,
        builder_kwargs,
        dataset_infos=dataset_infos,
        builder_configs_parameters=BuilderConfigsParameters(
            metadata_configs=metadata_configs,
            builder_configs=builder_configs,
            default_config_name=default_config_name,
        ),
    )


class HfDatasetsWrapper:
    @staticmethod
    def load_dataset(
        path: str,
        name: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
        split: Optional[Union[str, Split]] = None,
        cache_dir: Optional[str] = None,
        features: Optional[Features] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[Union[DownloadMode, str]] = None,
        verification_mode: Optional[Union[VerificationMode, str]] = None,
        ignore_verifications="deprecated",
        keep_in_memory: Optional[bool] = None,
        save_infos: bool = False,
        revision: Optional[Union[str, Version]] = None,
        token: Optional[Union[bool, str]] = None,
        use_auth_token="deprecated",
        task="deprecated",
        streaming: bool = False,
        num_proc: Optional[int] = None,
        storage_options: Optional[Dict] = None,
        trust_remote_code: bool = None,
        dataset_info_only: Optional[bool] = False,
        **config_kwargs,
    ) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset, dict]:
        if use_auth_token != "deprecated":
            warnings.warn(
                "'use_auth_token' was deprecated in favor of 'token' in version 2.14.0 and will be removed in 3.0.0.\n"
                "You can remove this warning by passing 'token=<use_auth_token>' instead.",
                FutureWarning,
            )
            token = use_auth_token
        if ignore_verifications != "deprecated":
            verification_mode = VerificationMode.NO_CHECKS if ignore_verifications else VerificationMode.ALL_CHECKS
            warnings.warn(
                "'ignore_verifications' was deprecated in favor of 'verification_mode' "
                "in version 2.9.1 and will be removed in 3.0.0.\n"
                f"You can remove this warning by passing 'verification_mode={verification_mode.value}' instead.",
                FutureWarning,
            )
        if task != "deprecated":
            warnings.warn(
                "'task' was deprecated in version 2.13.0 and will be removed in 3.0.0.\n",
                FutureWarning,
            )
        else:
            task = None
        if data_files is not None and not data_files:
            raise ValueError(
                replace_invalid_characters(
                    f"Empty 'data_files': '{data_files}'. It should be either non-empty or None (default)."
                )
            )
        if Path(path, config.DATASET_STATE_JSON_FILENAME).exists():
            raise ValueError(
                "You are trying to load a dataset that was saved using `save_to_disk`. "
                "Please use `load_from_disk` instead."
            )

        if streaming and num_proc is not None:
            raise NotImplementedError(
                "Loading a streaming dataset in parallel with `num_proc` is not implemented. "
                "To parallelize streaming, you can wrap the dataset with a PyTorch DataLoader "
                "using `num_workers` > 1 instead."
            )

        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
        verification_mode = VerificationMode(
            (verification_mode or VerificationMode.BASIC_CHECKS) if not save_infos else VerificationMode.ALL_CHECKS
        )

        # Create a dataset builder
        builder_instance = HfDatasetsWrapper.load_dataset_builder(
            path=path,
            name=name,
            data_dir=data_dir,
            data_files=data_files,
            cache_dir=cache_dir,
            features=features,
            download_config=download_config,
            download_mode=download_mode,
            revision=revision,
            token=token,
            storage_options=storage_options,
            trust_remote_code=trust_remote_code,
            _require_default_config_name=name is None,
            **config_kwargs,
        )

        # Note: Only for preview mode
        if dataset_info_only:
            ret_dict = {}
            # Get dataset config info from python script
            if isinstance(path, str) and path.endswith(".py") and os.path.exists(path):
                from datasets import get_dataset_config_names

                subset_list = get_dataset_config_names(path)
                ret_dict = {_subset: [] for _subset in subset_list}
                return ret_dict

            if builder_instance is None or not hasattr(builder_instance, "builder_configs"):
                logger.error(f"No builder_configs found for {path} dataset.")
                return ret_dict

            _tmp_builder_configs = builder_instance.builder_configs
            for tmp_config_name, tmp_builder_config in _tmp_builder_configs.items():
                tmp_config_name = str(tmp_config_name)
                if hasattr(tmp_builder_config, "data_files") and tmp_builder_config.data_files is not None:
                    ret_dict[tmp_config_name] = [str(item) for item in list(tmp_builder_config.data_files.keys())]
                else:
                    ret_dict[tmp_config_name] = []
            return ret_dict

        # Return iterable dataset in case of streaming
        if streaming:
            return builder_instance.as_streaming_dataset(split=split)

        # Download and prepare data
        builder_instance.download_and_prepare(
            download_config=download_config,
            download_mode=download_mode,
            verification_mode=verification_mode,
            try_from_hf_gcs=False,
            num_proc=num_proc,
            storage_options=storage_options,
        )

        # Build dataset for splits
        keep_in_memory = (
            keep_in_memory if keep_in_memory is not None else is_small_dataset(builder_instance.info.dataset_size)
        )
        ds = builder_instance.as_dataset(split=split, verification_mode=verification_mode, in_memory=keep_in_memory)
        # Rename and cast features to match task schema
        if task is not None:
            # To avoid issuing the same warning twice
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                ds = ds.prepare_for_task(task)
        if save_infos:
            builder_instance._save_infos()

        return ds

    @staticmethod
    def load_dataset_builder(
        path: str,
        name: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
        cache_dir: Optional[str] = None,
        features: Optional[Features] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[Union[DownloadMode, str]] = None,
        revision: Optional[Union[str, Version]] = None,
        token: Optional[Union[bool, str]] = None,
        use_auth_token="deprecated",
        storage_options: Optional[Dict] = None,
        trust_remote_code: Optional[bool] = None,
        _require_default_config_name=True,
        **config_kwargs,
    ) -> DatasetBuilder:
        if use_auth_token != "deprecated":
            warnings.warn(
                "'use_auth_token' was deprecated in favor of 'token' in version 2.14.0 and will be removed in 3.0.0.\n"
                "You can remove this warning by passing 'token=<use_auth_token>' instead.",
                FutureWarning,
            )
            token = use_auth_token
        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
        if token is not None:
            download_config = download_config.copy() if download_config else DownloadConfig()
            download_config.token = token
        if storage_options is not None:
            download_config = download_config.copy() if download_config else DownloadConfig()
            download_config.storage_options.update(storage_options)
        dataset_module = HfDatasetsWrapper.dataset_module_factory(
            path=path,
            name=name,
            revision=revision,
            download_config=download_config,
            download_mode=download_mode,
            data_dir=data_dir,
            data_files=data_files,
            cache_dir=cache_dir,
            trust_remote_code=trust_remote_code,
            _require_default_config_name=_require_default_config_name,
            _require_custom_configs=bool(config_kwargs),
        )

        # Get dataset builder class from the processing script
        builder_kwargs = dataset_module.builder_kwargs
        data_dir = builder_kwargs.pop("data_dir", data_dir)
        data_files = builder_kwargs.pop("data_files", data_files)
        dataset_name = builder_kwargs.pop("dataset_name", None)
        config_name = config_kwargs.pop(
            "config_name", name or dataset_module.builder_configs_parameters.default_config_name
        )
        info = dataset_module.dataset_infos.get(config_name) if dataset_module.dataset_infos else None

        if (
            path in _PACKAGED_DATASETS_MODULES
            and data_files is None
            and dataset_module.builder_configs_parameters.builder_configs[0].data_files is None
        ):
            error_msg = f"Please specify the data files or data directory to load for the {path} dataset builder."
            example_extensions = [
                extension for extension in _EXTENSION_TO_MODULE if _EXTENSION_TO_MODULE[extension] == path
            ]
            if example_extensions:
                error_msg += f'\nFor example `data_files={{"train": "path/to/data/train/*.{example_extensions[0]}"}}`'
            raise ValueError(replace_invalid_characters(error_msg))

        builder_cls = get_dataset_builder_class(dataset_module, dataset_name=dataset_name)
        builder_instance: DatasetBuilder = builder_cls(
            cache_dir=cache_dir,
            dataset_name=dataset_name,
            config_name=config_name,
            data_dir=data_dir,
            data_files=data_files,
            hash=dataset_module.hash,
            info=info,
            features=features,
            token=token,
            storage_options=storage_options,
            **builder_kwargs,  # contains base_path
            **config_kwargs,
        )
        builder_instance._use_legacy_cache_dir_if_possible(dataset_module)

        return builder_instance

    @staticmethod
    def dataset_module_factory(
        path: str,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[Union[DownloadMode, str]] = None,
        dynamic_modules_path: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[Dict, List, str, DataFilesDict]] = None,
        cache_dir: Optional[str] = None,
        trust_remote_code: Optional[bool] = None,
        _require_default_config_name=True,
        _require_custom_configs=False,
        **download_kwargs,
    ) -> DatasetModule:
        subset_name: str = download_kwargs.pop("name", None)
        if download_config is None:
            download_config = DownloadConfig(**download_kwargs)
        download_config.storage_options.update({"name": subset_name})

        if download_config and download_config.cache_dir is None:
            download_config.cache_dir = cache_dir if cache_dir else OM_DATASETS_CACHE

        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
        download_config.extract_compressed_file = True
        download_config.force_extract = True
        download_config.force_download = download_mode == DownloadMode.FORCE_REDOWNLOAD

        filename = list(filter(lambda x: x, path.replace(os.sep, "/").split("/")))[-1]
        if not filename.endswith(".py"):
            filename = filename + ".py"
        combined_path = os.path.join(path, filename)

        # Try packaged
        if path in _PACKAGED_DATASETS_MODULES:
            return PackagedDatasetModuleFactory(
                path,
                data_dir=data_dir,
                data_files=data_files,
                download_config=download_config,
                download_mode=download_mode,
            ).get_module()
        # Try locally
        elif path.endswith(filename):
            if os.path.isfile(path):
                return LocalDatasetModuleFactoryWithScript(
                    path,
                    download_mode=download_mode,
                    dynamic_modules_path=dynamic_modules_path,
                    trust_remote_code=trust_remote_code,
                ).get_module()
            else:
                raise FileNotFoundError(
                    replace_invalid_characters(f"Couldn't find a dataset script at {relative_to_absolute_path(path)}")
                )
        elif os.path.isfile(combined_path):
            return LocalDatasetModuleFactoryWithScript(
                combined_path,
                download_mode=download_mode,
                dynamic_modules_path=dynamic_modules_path,
                trust_remote_code=trust_remote_code,
            ).get_module()
        elif os.path.isdir(path):
            return LocalDatasetModuleFactoryWithoutScript(
                path, data_dir=data_dir, data_files=data_files, download_mode=download_mode
            ).get_module()
        # Try remotely
        elif is_relative_path(path) and path.count("/") <= 1:
            try:
                _raise_if_offline_mode_is_enabled()
                try:
                    dataset_info = HubApi().dataset_info(
                        repo_id=path,
                        timeout=DEFAULT_TIMEOUT,
                        token=download_config.token,
                    )
                except Exception as e:  # noqa catch any exception of hf_hub and consider that the dataset doesn't exist
                    if isinstance(
                        e,
                        (  # noqa: E131
                            OfflineModeIsEnabled,  # noqa: E131
                            requests.exceptions.ConnectTimeout,  # noqa: E131, E261
                            requests.exceptions.ConnectionError,  # noqa: E131
                        ),  # noqa: E131
                    ):
                        raise ConnectionError(
                            replace_invalid_characters(f"Couldn't reach '{path}' on the Hub ({type(e).__name__})")
                        ) from e
                    elif "404" in str(e):
                        msg = f"Dataset '{path}' doesn't exist on the Hub"
                        raise DatasetNotFoundError(
                            replace_invalid_characters(msg + f" at revision '{revision}'" if revision else msg)
                        ) from e
                    elif "401" in str(e):
                        msg = f"Dataset '{path}' doesn't exist on the Hub"
                        msg = msg + f" at revision '{revision}'" if revision else msg
                        raise DatasetNotFoundError(
                            replace_invalid_characters(
                                msg + ". If the repo is private or gated, " "make sure to load with token."
                            )
                        ) from e
                    else:
                        raise e
                if filename in [sibling.rfilename for sibling in dataset_info.siblings]:
                    can_load_config_from_parquet_export = False
                    if config.USE_PARQUET_EXPORT and can_load_config_from_parquet_export:
                        try:
                            return HubDatasetModuleFactoryWithParquetExport(
                                path, download_config=download_config, revision=dataset_info.sha
                            ).get_module()
                        except DatasetsServerError:
                            pass
                    # Otherwise we must use the dataset script if the user trusts it
                    return HubDatasetModuleFactoryWithScript(
                        path,
                        revision=revision,
                        download_config=download_config,
                        download_mode=download_mode,
                        dynamic_modules_path=dynamic_modules_path,
                        trust_remote_code=trust_remote_code,
                    ).get_module()
                else:
                    return HubDatasetModuleFactoryWithoutScript(
                        path,
                        revision=revision,
                        data_dir=data_dir,
                        data_files=data_files,
                        download_config=download_config,
                        download_mode=download_mode,
                    ).get_module()
            except Exception as e1:
                # All the attempts failed, before raising the error we should check if the module is already cached
                try:
                    return CachedDatasetModuleFactory(
                        path, dynamic_modules_path=dynamic_modules_path, cache_dir=cache_dir
                    ).get_module()
                except Exception:
                    # If it's not in the cache, then it doesn't exist.
                    if isinstance(e1, OfflineModeIsEnabled):
                        raise ConnectionError(
                            replace_invalid_characters(f"Couldn't reach the Hub for dataset '{path}': {e1}")
                        ) from None
                    if isinstance(e1, (DataFilesNotFoundError, DatasetNotFoundError, EmptyDatasetError)):
                        raise e1 from None
                    if isinstance(e1, FileNotFoundError):
                        raise FileNotFoundError(
                            replace_invalid_characters(
                                f"Couldn't find a dataset script at {relative_to_absolute_path(combined_path)} or "
                                f"any data file in the same directory. "
                                f"Couldn't find '{path}' on the Hugging Face Hub either: {type(e1).__name__}: {e1}"
                            )
                        ) from None
                    raise e1 from None
        else:
            raise FileNotFoundError(
                replace_invalid_characters(
                    f"Couldn't find a dataset script at {relative_to_absolute_path(combined_path)} or "
                    f"any data file in the same directory."
                )
            )


@contextlib.contextmanager
def load_dataset_with_ctx(*args, **kwargs):
    # origin
    origin_HF_ENDPOINT = config.HF_ENDPOINT
    origin_get_module_without_script = HubDatasetModuleFactoryWithoutScript.get_module
    origin_get_module_with_script = HubDatasetModuleFactoryWithScript.get_module

    origi_RepoFile = huggingface_hub.hf_api.RepoFile
    origin_DatasetInfo = huggingface_hub.hf_api.DatasetInfo
    origin_HfFileSystem = huggingface_hub.HfFileSystem
    origin_build_hf_headers = huggingface_hub.utils.build_hf_headers

    # patch
    config.HF_ENDPOINT = os.environ.get("OPENMIND_HUB_ENDPOINT", OPENMIND_URL)
    HubDatasetModuleFactoryWithoutScript.get_module = get_module_without_script
    HubDatasetModuleFactoryWithScript.get_module = get_module_with_script
    huggingface_hub.hf_api.RepoFile = openmind_hub.RepoFile
    huggingface_hub.hf_api.DatasetInfo = openmind_hub.DatasetInfo
    huggingface_hub.HfFileSystem = openmind_hub.OmFileSystem
    huggingface_hub.utils.build_hf_headers = openmind_hub.build_om_headers

    try:
        dataset_res = HfDatasetsWrapper.load_dataset(*args, **kwargs)
        yield dataset_res
    finally:
        # recover patch
        config.HF_ENDPOINT = origin_HF_ENDPOINT
        HubDatasetModuleFactoryWithoutScript.get_module = origin_get_module_without_script
        HubDatasetModuleFactoryWithoutScript.get_module = origin_get_module_with_script
        huggingface_hub.hf_api.RepoFile = origi_RepoFile
        huggingface_hub.hf_api.DatasetInfo = origin_DatasetInfo
        huggingface_hub.HfFileSystem = origin_HfFileSystem
        huggingface_hub.utils.build_hf_headers = origin_build_hf_headers

        logger.info("Context manager of om-dataset exited.")
