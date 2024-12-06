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

import numpy as np

from .base import Metric


class ConfusionMatrix(Metric):
    """
    A class to compute the confusion matrix for a classification model.

    This class extends the Metric class and implements the methods
    to compute the confusion matrix, which is a table used to describe the
    performance of a classification model.
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
        return self._confusion_matrix(self.preds, self.labels)

    def compute(self, preds, labels):
        if len(preds) != len(labels):
            raise ValueError("Predictions and labels must have the same length.")
        return self._confusion_matrix(preds, labels)

    def _confusion_matrix(self, y_pred, y_true):
        classes = np.unique(np.concatenate((y_true, y_pred)))
        n_classes = len(classes)

        cm = np.zeros((n_classes, n_classes), dtype=int)
        label_to_index = {label: i for i, label in enumerate(classes)}

        for t, p in zip(y_true, y_pred):
            t_index = label_to_index[t]
            p_index = label_to_index[p]

            cm[t_index, p_index] += 1

        return {"confusion_matrix": cm}
