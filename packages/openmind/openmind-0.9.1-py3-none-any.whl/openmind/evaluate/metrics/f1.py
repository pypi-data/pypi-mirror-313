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


class F1(Metric):
    """
    A class for computing the F1 Score as a metric.

    The F1 Score is a measure of a model's accuracy considering both the precision
    and the recall of the model's predictions.
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
        return self.compute(self.preds, self.labels)

    def compute(self, preds, labels):
        return {"f1": self._f1_score(preds, labels)}

    def _f1_score(self, preds, labels):
        TP = sum([1 for t, p in zip(labels, preds) if t == p == 1])
        FP = sum([1 for t, p in zip(labels, preds) if t == 0 and p == 1])
        FN = sum([1 for t, p in zip(labels, preds) if t == 1 and p == 0])

        precision = TP / (TP + FP) if TP + FP > 0 else 0
        recall = TP / (TP + FN) if TP + FN > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

        return f1
