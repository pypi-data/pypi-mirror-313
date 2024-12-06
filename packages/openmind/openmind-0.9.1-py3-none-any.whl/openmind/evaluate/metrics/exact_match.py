# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# Modification: We have added the add() and evaluate() methods on top of the compute() function,
#               enabling incremental computation.
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

import re
import string
import numpy as np

from .base import Metric


class ExactMatch(Metric):
    """
    Metric class for calculating the exact match between predictions and labels.

    This class extends the Metric class to provide functionality
    for assessing the exact match rate between the model's predictions and the true labels.
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

    def evaluate(self, regexes_to_ignore=None, ignore_case=False, ignore_punctuation=False, ignore_numbers=False):
        return self.compute(self.preds, self.labels, regexes_to_ignore, ignore_case, ignore_punctuation, ignore_numbers)

    def compute(
        self, preds, labels, regexes_to_ignore=None, ignore_case=False, ignore_punctuation=False, ignore_numbers=False
    ):
        if regexes_to_ignore is not None:
            for s in regexes_to_ignore:
                preds = np.array([re.sub(s, "", x) for x in preds])
                labels = np.array([re.sub(s, "", x) for x in labels])
        else:
            preds = np.asarray(preds)
            labels = np.asarray(labels)

        if ignore_case:
            preds = np.char.lower(preds)
            labels = np.char.lower(labels)

        if ignore_punctuation:
            repl_table = string.punctuation.maketrans("", "", string.punctuation)
            preds = np.char.translate(preds, table=repl_table)
            labels = np.char.translate(labels, table=repl_table)

        if ignore_numbers:
            repl_table = string.digits.maketrans("", "", string.digits)
            preds = np.char.translate(preds, table=repl_table)
            labels = np.char.translate(labels, table=repl_table)

        score_list = preds == labels

        return {"exact_match": np.mean(score_list)}
