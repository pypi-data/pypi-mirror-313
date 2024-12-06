import json
import inspect
import os
import re
from pathlib import Path
from typing import Optional

from ..utils.hub import OpenMindHub
from ..utils.logging import get_logger, set_verbosity_info


logger = get_logger()
set_verbosity_info()


def get_pipeline_config():
    local_path = Path(inspect.getfile(inspect.currentframe())).resolve()
    local_dir = local_path.parents[0]
    native_json_path = local_dir / "native_pipelines.json"
    with open(native_json_path, "r") as file:
        config = json.load(file)
    return config


SUPPORTED_TASK_MAPPING = get_pipeline_config()


def download_from_repo(repo_id, revision=None, cache_dir=None, force_download=False):
    if not os.path.exists(repo_id):
        local_path = OpenMindHub.snapshot_download(
            repo_id=repo_id,
            revision=revision,
            cache_dir=cache_dir,
            force_download=force_download,
        )
    else:
        local_path = repo_id
    return local_path


def get_task_from_readme(model: str) -> Optional[str]:
    """
    Get the task of the model by reading the README.md file.
    """
    task = None
    if not os.path.exists(model):
        task = OpenMindHub.get_task_from_repo(model)
    else:
        readme_file = os.path.join(model, "README.md")
        if os.path.exists(readme_file):
            with open(readme_file, "r") as file:
                content = file.read()
                pipeline_tag = re.search(r"pipeline_tag:\s?(([a-z]*-)*[a-z]*)", content)
                if pipeline_tag:
                    task = pipeline_tag.group(1)
    if task is None:
        logger.warning("Cannot infer the task from the provided model, please provide the task explicitly.")

    return task
