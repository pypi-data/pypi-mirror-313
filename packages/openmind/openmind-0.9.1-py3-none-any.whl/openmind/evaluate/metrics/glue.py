# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
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

from scipy.stats import pearsonr, spearmanr

from .base import Metric
from ...utils import replace_invalid_characters


class Glue(Metric):
    """
    A class for computing GLUE metrics.
    """

    def __init__(self, config_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_name = config_name
        self.valid_config = [
            "sst2",
            "mnli",
            "mnli_mismatched",
            "mnli_matched",
            "cola",
            "stsb",
            "mrpc",
            "qqp",
            "qnli",
            "rte",
            "wnli",
            "hans",
        ]
        if self.config_name not in self.valid_config:
            err_msg = "You shoule supply a configuation name selected in " f"{self.valid_config}"
            raise KeyError(replace_invalid_characters(err_msg))
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
        if self.config_name == "cola":
            return {"matthews_correlation": self._matthews_corrcoef(preds, labels)}
        elif self.config_name == "stsb":
            return self._pearson_and_spearman(preds, labels)
        elif self.config_name in ["mrpc", "qqp"]:
            return self._acc_and_f1(preds, labels)
        elif self.config_name in ["sst2", "mnli", "mnli_mismatched", "mnli_matched", "qnli", "rte", "wnli", "hans"]:
            return {"accuracy": self._simple_accuracy(preds, labels)}
        else:
            err_msg = "You shoule supply a configuation name selected in " f"{self.valid_config}"
            raise KeyError(replace_invalid_characters(err_msg))

    def _matthews_corrcoef(self, preds, labels):
        TP = sum([1 for t, p in zip(labels, preds) if t == p == 1])
        FP = sum([1 for t, p in zip(labels, preds) if t == 0 and p == 1])
        TN = sum([1 for t, p in zip(labels, preds) if t == p == 0])
        FN = sum([1 for t, p in zip(labels, preds) if t == 1 and p == 0])

        numerator = TP * TN - FP * FN
        denominator = ((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) ** 0.5
        mcc = numerator / denominator if denominator > 0 else 0
        return mcc

    def _pearson_and_spearman(self, preds, labels):
        pearson_corr = float(pearsonr(preds, labels)[0])
        spearman_corr = float(spearmanr(preds, labels)[0])
        return {
            "pearsonr": pearson_corr,
            "spearmanr": spearman_corr,
        }

    def _simple_accuracy(self, preds, labels):
        correct_count = sum([1 for pred, label in zip(preds, labels) if pred == label])
        total = len(preds)
        return correct_count / total if total > 0 else 0

    def _f1_score(self, preds, labels):
        TP = sum([1 for t, p in zip(labels, preds) if t == p == 1])
        FP = sum([1 for t, p in zip(labels, preds) if t == 0 and p == 1])
        FN = sum([1 for t, p in zip(labels, preds) if t == 1 and p == 0])

        precision = TP / (TP + FP) if TP + FP > 0 else 0
        recall = TP / (TP + FN) if TP + FN > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

        return f1

    def _acc_and_f1(self, preds, labels):
        acc = self._simple_accuracy(preds, labels)
        f1 = self._f1_score(preds, labels)

        return {
            "accuracy": acc,
            "f1": f1,
        }
