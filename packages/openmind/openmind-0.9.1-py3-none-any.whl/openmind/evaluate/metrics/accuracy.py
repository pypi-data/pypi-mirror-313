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

from .base import Metric


class Accuracy(Metric):
    """
    A concrete implementation of the Metric class for calculating accuracy.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preds = []
        self.labels = []

    def add(self, preds, labels):
        if len(preds) != len(labels):
            raise ValueError("Predictions and labels must have the same length.")
        self.preds.extend(preds)
        self.labels.extend(labels)

    def evaluate(self):
        return self._compute_accuracy(self.preds, self.labels)

    def compute(self, preds, labels):
        if len(preds) != len(labels):
            raise ValueError("Predictions and labels must have the same length.")
        return self._compute_accuracy(preds, labels)

    def _compute_accuracy(self, preds, labels):
        correct_count = sum([1 for pred, label in zip(preds, labels) if pred == label])
        total = len(preds)
        return {"accuracy": correct_count / total if total > 0 else 0}
