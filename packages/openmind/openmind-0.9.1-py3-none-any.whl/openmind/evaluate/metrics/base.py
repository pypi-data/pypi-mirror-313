# Copyright (c) Alibaba, Inc. and its affiliates.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# Modification: We added the compute method based on the original code,
#               which can be calculated directly through inputs.
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

from abc import ABC, abstractmethod


class Metric(ABC):
    """
    Base metric class for computing various metrics.

    This class serves as an abstract base class for all metric classes.
    Subclasses should implement the methods for adding predictions and labels,
    evaluating the metric, and computing the metric value.
    """

    @abstractmethod
    def add(self, preds, labels):
        """
        Abstract method to add predictions and their corresponding labels.

        Args:
            preds: Predictions made by the model.
            labels: True labels.

        Returns: None
        """
        return NotImplemented

    @abstractmethod
    def evaluate(self):
        """
        This method should calculate and return the metric value based on all the
        predictions and labels that have been added.

        Returns: The actual metric dict with standard names.
        """
        return NotImplemented

    @abstractmethod
    def compute(self, preds, labels):
        """
        This method should take predictions and labels as input and compute the
        metric value. This method does not add preds and labels to the class.

        Args:
            preds: Predictions made by the model.
            labels: True labels.

        Returns: The actual metric dict with standard names.
        """
        return NotImplemented
