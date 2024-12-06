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


class MSE(Metric):
    """
    Metric class for calculating the Mean Squared Error (MSE).
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
        return {"mse": self._mean_squared_error(preds, labels)}

    def _mean_squared_error(self, preds, labels):
        preds = list(preds)
        labels = list(labels)
        mse = sum((preds[i] - labels[i]) ** 2 for i in range(len(labels))) / len(labels) if len(labels) > 0 else 0
        return mse
