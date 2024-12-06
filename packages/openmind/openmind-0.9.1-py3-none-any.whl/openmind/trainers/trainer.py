# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.
# Copyright 2020-present the HuggingFace Inc. team.
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
import gc
from pathlib import Path
from typing import Optional

from ..utils.hub import OpenMindHub
from ..utils import exceptions, get_framework
from .trainer_utils import PREFIX_CHECKPOINT_DIR

framework = get_framework()

if framework == "pt":
    from transformers import Trainer as BackendTrainer
elif framework == "ms":
    from mindformers import Trainer as BackendTrainer
else:
    raise exceptions.NotFoundAnyFrameworkError()


class Trainer(BackendTrainer):
    """
    Trainer is an interface for transformers.Trainer and Mindformers.Trainer,
    defines a uniform behavioral functions.
    common:
        model:
            a model instance to train, evaluate or use for predictions, If a 'model_init' is provided in Kwargs,
            it can be None in 'pt'; Others need to be passed in an instance.
            pt: (Optional[Union[PreTrainedModel, torch.nn.Module]])
            ms: (Optional[Union[str, Cell, BaseModel]])
        args:
            The task config which is used to configure the dataset, the hyper-parameter, optimizer, etc.
            It supports yaml path or config dict or ConfigArguments class.
            pt: (Optional[Union[str, dict, openmind.trainer_args.TrainingArguments]])
            ms: NOTE
        train_dataset:
            The training dataset. It supports real dataset path or BaseDateset class or MindSpore Dataset class.
            pt: (Optional[Union[str, BaseDataset]])
            ms: (Optional[Union[str, BaseDataset]])
        eval_dataset:
            The evaluate dataset. It supports real dataset path or BaseDateset class or MindSpore Dataset class.
            pt: (Optional[Union[str, BaseDataset]])
            ms: (Optional[Union[str, BaseDataset]])
        optimizers:
            A tuple containing the optimizer and the scheduler to use. Will default to an instance of [`AdamW`] on
            your model and a scheduler given by [`get_linear_schedule_with_warmup`] controlled by `args`
            pt: (Optional[Tuple[torch.optim.Optimizer, torch.optim.lr_scheduler.LambdaLR]])
            ms: NOTE
        callbacks (Optional[List[TrainerCallback]]):
            A list of callbacks to customize the training loop. Will add those to the list of default callbacks
            detailed in [here](callback).

            If you want to remove one of the default callbacks used, use the [`Trainer.remove_callback`] method.
    pytorch:
        data_collator (Optional[DataCollator]):
            The function to use to form a batch from a list of elements of `train_dataset` or `eval_dataset`.
            Will default to [`default_data_collator`] if no `tokenizer` is provided, an instance of
            [`DataCollatorWithPadding`] otherwise
        tokenizer (Optional[PreTrainedTokenizerBase]):
            The tokenizer used to preprocess the data. If provided, will be used to automatically pad the
            inputs to the maximum length when batching inputs, and it will be saved along the model to make it
            easier to rerun an interrupted training or reuse the fine-tuned model.
        model_init (Optional[Callable[[], PreTrainedModel]]):
            A function that instantiates the model to be used. If provided, each call to [`~Trainer.train`]
            will start from a new instance of the model as given by this function.

            The function may have zero argument, or a single one containing the optuna/Ray Tune/SigOpt trial
            object, to be able to choose different architectures according to hyper parameters (such as layer
            count, sizes of inner layers, dropout probabilities etc).
        compute_metrics (Optional[Callable[[EvalPrediction], Dict]]):
            The function that will be used to compute metrics at evaluation. Must take a [`EvalPrediction`]
            and return a dictionary string to metric values.

        preprocess_logits_for_metrics (Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]]:
            A function that preprocess the logits right before caching them at each evaluation step. Must take
            two tensors, the logits and the labels, and return the logits once processed as desired.
            The modifications made by this function will be reflected in the predictions received
            by `compute_metrics`.

            Note that the labels (second parameter) will be `None` if the dataset does not have them.
    mindspore: NOTE
    """

    def train(self, *args, **kwargs):
        """
        Perform a training step on a batch of inputs.

        Args:
            pt:
                resume_from_checkpoint (`str` or `bool`, *optional*):
                    If a `str`, local path to a saved checkpoint as saved by a previous instance of [`Trainer`]. If a
                    `bool` and equals `True`, load the last checkpoint in *args.output_dir* as saved by a previous
                    instance of [`Trainer`]. If present, training will resume from the model/optimizer/scheduler states
                     loaded here.
                trial (`optuna.Trial` or `Dict[str, Any]`, *optional*):
                    The trial run or the hyperparameter dictionary for hyperparameter search.
                ignore_keys_for_eval (`List[str]`, *optional*):
                    A list of keys in the output of your model (if it is a dictionary) that should be ignored when
                    gathering predictions for evaluation during the training.
            ms: NOTE
        Kwargs:
            pt:
                model_path(Optional[str]):
                    If not None, reuse the model under the path.
            ms: NOTE
        """
        return super().train(*args, **kwargs)

    def evaluate(self, *args, **kwargs):
        """
        Run evaluation and returns metrics.

        The calling script will be responsible for providing a method to compute metrics, as they are task-dependent
        (pass it to the init `compute_metrics` argument).

        You can also subclass and override this method to inject custom behavior.

        Args:
            pt:
                eval_dataset (Optional[Dataset]):
                    Pass a dataset if you wish to override `self.eval_dataset`. If it is a [`~datasets.Dataset`],
                    columns not accepted by the `model.forward()` method are automatically removed. It must implement
                    the `__len__` method.
                ignore_keys (Optional[List[str]]):
                    A list of keys in the output of your model (if it is a dictionary) that should be ignored when
                    gathering predictions.
                metric_key_prefix (Optional[str], defaults to `"eval"`):
                    An optional prefix to be used as the metrics key prefix. For example the metrics "bleu" will be
                    named "eval_bleu" if the prefix is "eval" (default)
            ms:
                NOTE
        Kwargs:
            pt: None
            ms: NOTE
        Returns:
            A dictionary containing the evaluation loss and the potential metrics computed from the predictions. The
            dictionary also contains the epoch number which comes from the training state.
        """
        return super().evaluate(*args, **kwargs)

    def predict(self, *args, **kwargs):
        """
        Run prediction and returns predictions and potential metrics.

        Depending on the dataset and your use case, your test dataset may contain labels. In that case, this method
        will also return metrics, like in `evaluate()`.

        Args:
            pt:
                test_dataset (`Dataset`):
                    Dataset to run the predictions on. If it is an `datasets.Dataset`, columns not accepted by the
                    `model.forward()` method are automatically removed. Has to implement the method `__len__`
                ignore_keys (Optional[List[str]]):
                    A list of keys in the output of your model (if it is a dictionary) that should be ignored when
                    gathering predictions.
                metric_key_prefix (Optional[str], defaults to `"test"`):
                    An optional prefix to be used as the metrics key prefix. For example the metrics "bleu" will be
                    named "test_bleu" if the prefix is "test" (default)

                <Tip>
                If your predictions or labels have different sequence length (for instance because you're doing dynamic
                padding in a token classification task) the predictions will be padded (on the right) to allow for
                concatenation into one array. The padding index is -100.
                </Tip>
            ms:
                NOTE
        Kwargs:
            pt: None
            ms: NOTE
        Returns:
            A dictionary containing the evaluation loss and the potential metrics computed from the predictions. The
            dictionary also contains the epoch number which comes from the training state.
        """
        return super().predict(*args, **kwargs)

    def add_callback(self, callback):
        """
        Add a callback to the current list of callbacks.

        callback:
           A class or an instance. In the first case, will instantiate a member of that class.
           pt: (Union[type, transformer.TrainerCallback])
           ms: NOTE
        """
        super().add_callback(callback)

    def pop_callback(self, callback):
        """
        Remove a callback from the current list of callbacks and returns it. If the callback is not found, returns
        `None` (and no error is raised).

        callback:
            A class or an instance. In the first case, will instantiate a member of that class.
            pt: (Union[type, transformer.TrainerCallback])
            ms: NOTE
        Returns:
            callback:
                The callback removed, if found.
                pt: (`transformer.TrainerCallback`)
                ms: NOTE
        """
        return super().pop_callback(callback)

    def remove_callback(self, callback):
        """
        Remove a callback from the current list of callbacks.

        callback:
            A class or an instance. In the first case, will instantiate a member of that class.
            pt: (Union[type, transformer.TrainerCallback])
            ms: NOTE
        """
        super().remove_callback(callback)

    def save_model(self, *args, **kwargs):
        """
        Will save the model, so you can reload it using `from_pretrained()`. Will only save from the main process.
        Args:
            common:
                output_dir(Optional[str]):
                    Model saved path, default is None, model will be saved under the args.output_dir if this is None.
            pt:
                _internal_call(bool):
                    When args.push_to_hub is True, whether push the model to hub when user call save_model method.
                    Default is False, push.
            ms:
                NOTE
        Kwargs:
            pt: None
            ms: NOTE
        """
        super().save_model(*args, **kwargs)

    def init_hf_repo(self):
        """
        Initializes a git repo in `self.args.hub_model_id`.
        """
        # Only on process zero
        if not self.is_world_process_zero():
            return

        if self.args.hub_model_id is None:
            repo_name = Path(self.args.output_dir).absolute().name
        else:
            repo_name = self.args.hub_model_id

        repo_url = OpenMindHub.create_repo(
            repo_name, token=self.args.hub_token, private=self.args.hub_private_repo, exist_ok=True
        )
        self.hub_model_id = repo_url.repo_id
        self.push_in_progress = None

    def push_to_hub(self, commit_message: Optional[str] = "End of training", blocking: bool = True, **kwargs) -> str:
        """
        Upload `self.model` and `self.tokenizer` to the model hub on the repo `self.args.hub_model_id`.

        commit_message (Optional[str]):
            Message to commit while pushing, defaults to "End of training".
        blocking (Optional[bool]):
            Whether the function should return only when the `git push` has finished, default is True
        kwargs (Optional[Dict[str, Any]]:
            model_name(Optional[str]): model name in the hub.

        Returns:
            The URL of the repository where the model was pushed if `blocking=False`, or a `Future` object tracking the
            progress of the commit if `blocking=True`.
        """
        if self.hub_model_id is None:
            self.init_hf_repo()

        # Only push from one node.
        if not self.is_world_process_zero():
            return ""

        # Wait for the current upload to be finished.
        self._finish_current_push()
        upload_rsp = OpenMindHub.upload_folder(
            repo_id=self.hub_model_id,
            folder_path=self.args.output_dir,
            commit_message=commit_message,
            token=self.args.hub_token,
            run_as_future=not blocking,
            ignore_patterns=["_*", f"{PREFIX_CHECKPOINT_DIR}-*"],
        )

        del self.args.hub_token
        gc.collect()

        return upload_rsp
