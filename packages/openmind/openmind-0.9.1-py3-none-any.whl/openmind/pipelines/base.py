# Copyright (c) 2024 Huawei Technologies Co., Ltd.
# Copyright (c) Lepton AI, Inc. All rights reserved.
#
# Adapted from
# https://github.com/leptonai/leptonai/blob/main/leptonai/photon/hf/hf.py
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

from typing import Iterator, List, Optional, Type

from ..utils.constants import Backends, Frameworks, Tasks
from ..utils.version import require_version


class BasePipeline:
    task: Optional[Tasks] = None
    framework: Optional[Frameworks] = None
    backend: Optional[Backends] = None
    requirement_dependency: Optional[List[str]] = None

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def _iter_ancestors(cls) -> Iterator[Type["BasePipeline"]]:
        yield cls
        for base in cls.__bases__:
            if base == BasePipeline:
                yield base
            elif not issubclass(base, BasePipeline):
                continue
            else:
                yield from base._iter_ancestors()

    @property
    def _requirement_dependency(self) -> List[str]:
        deps = []
        # We add dependencies from ancestor classes to derived classes
        # and keep the order. We do nont remove redundant dependencies
        # automatically.
        for base in reversed(list(self._iter_ancestors())):
            if base.requirement_dependency:
                deps.extend(base.requirement_dependency)
        # Do not sort or uniq pip deps line, as order matters
        return deps

    def check_dependency(self):
        for dep in self._requirement_dependency:
            require_version(dep)


class PTBasePipeline(BasePipeline):
    framework = Frameworks.pt
    # please override this in your derived class
    requirement_dependency = [
        # "torch-npu>=2.1.0",
        "torch>=2.1.0",
    ]


class MSBasePipeline(BasePipeline):
    framework = Frameworks.ms
    # please override this in your derived class
    requirement_dependency = ["mindspore==2.4.0"]
