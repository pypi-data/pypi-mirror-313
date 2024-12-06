# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.
# Copyright 2022 The HuggingFace Team. All rights reserved.
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
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Dict, List, Optional, Union

from ..trainers.trainer_utils import ExplicitEnum, HubStrategy, IntervalStrategy, SchedulerType
from ..utils import exceptions, get_framework

framework = get_framework()

if framework == "pt":
    from transformers import TrainingArguments as BackendTrainerArguments
elif framework == "ms":
    from mindformers import TrainingArguments as BackendTrainerArguments
else:
    raise exceptions.NotFoundAnyFrameworkError()


class OptimizerNames(ExplicitEnum):
    """
    Stores the acceptable string identifiers for optimizers.
    """

    # pt
    ADAMW_HF = "adamw_hf"
    ADAMW_TORCH = "adamw_torch"
    ADAMW_TORCH_FUSED = "adamw_torch_fused"
    ADAMW_TORCH_XLA = "adamw_torch_xla"
    ADAMW_TORCH_NPU_FUSED = "adamw_torch_npu_fused"
    ADAMW_APEX_FUSED = "adamw_apex_fused"
    ADAFACTOR = "adafactor"
    ADAMW_ANYPRECISION = "adamw_anyprecision"
    SGD = "sgd"
    ADAGRAD = "adagrad"
    ADAMW_BNB = "adamw_bnb_8bit"
    ADAMW_8BIT = "adamw_8bit"  # just an alias for adamw_bnb_8bit
    LION_8BIT = "lion_8bit"
    LION = "lion_32bit"
    PAGED_ADAMW = "paged_adamw_32bit"
    PAGED_ADAMW_8BIT = "paged_adamw_8bit"
    PAGED_LION = "paged_lion_32bit"
    PAGED_LION_8BIT = "paged_lion_8bit"
    RMSPROP = "rmsprop"

    # ms: NOTE


@dataclass
class TrainingArguments(BackendTrainerArguments):
    """
    TrainingArguments is the subset of the arguments we use in our example scripts **which relate to the training loop
    itself**.

    Using [`ArgumentParser`] we can turn this class into
    [argparse](https://docs.python.org/3/library/argparse#module-argparse) arguments that can be specified on the
    command line.

    Parameters:
        common:
            output_dir (`str`):
                The output directory where the model predictions and checkpoints will be written.
            overwrite_output_dir (`bool`, *optional*, defaults to `False`):
                If `True`, overwrite the content of the output directory. Use this to continue training if `output_dir`
                points to a checkpoint directory.
            do_train (`bool`, *optional*, defaults to `False`):
                Whether to run training or not. This argument is not directly used by [`Trainer`], it's intended to be
                used by your training/evaluation scripts instead.
            do_eval (`bool`, *optional*):
                Whether to run evaluation on the validation set or not. Will be set to `True` if `evaluation_strategy`
                is different from `"no"`. This argument is not directly used by [`Trainer`], it's intended to be used
                by your training/evaluation scripts instead.
            do_predict (`bool`, *optional*, defaults to `False`):
                Whether to run predictions on the test set or not. This argument is not directly used by [`Trainer`],
                it's intended to be used by your training/evaluation scripts instead.
            evaluation_strategy (`str` or [`~trainer_utils.IntervalStrategy`], *optional*, defaults to `"no"`):
                The evaluation strategy to adopt during training. Possible values are:

                    - `"no"`: No evaluation is done during training.
                    - `"steps"`: Evaluation is done (and logged) every `eval_steps`.
                    - `"epoch"`: Evaluation is done at the end of each epoch.
            per_device_train_batch_size (`int`, *optional*, defaults to 8):
                The batch size per GPU/XPU/TPU/MPS/NPU core/CPU for training.
            per_device_eval_batch_size (`int`, *optional*, defaults to 8):
                The batch size per GPU/XPU/TPU/MPS/NPU core/CPU for evaluation.
            gradient_accumulation_steps (`int`, *optional*, defaults to 1):
                Number of updates steps to accumulate the gradients for, before performing a backward/update pass.

                <Tip warning={true}>

                When using gradient accumulation, one step is counted as one step with backward pass. Therefore, logging
                , evaluation, save will be conducted every `gradient_accumulation_steps * xxx_step` training examples.

                </Tip>
            learning_rate (`float`, *optional*, defaults to 5e-5):
                The initial learning rate for [`AdamW`] optimizer.
            weight_decay (`float`, *optional*, defaults to 0):
                The weight decay to apply (if not zero) to all layers except all bias and LayerNorm weights in [`AdamW`]
                optimizer.
            adam_beta1 (`float`, *optional*, defaults to 0.9):
                The beta1 hyperparameter for the [`AdamW`] optimizer.
            adam_beta2 (`float`, *optional*, defaults to 0.999):
                The beta2 hyperparameter for the [`AdamW`] optimizer.
            adam_epsilon (`float`, *optional*, defaults to 1e-8):
                The epsilon hyperparameter for the [`AdamW`] optimizer.
            max_grad_norm (`float`, *optional*, defaults to 1.0):
                Maximum gradient norm (for gradient clipping).
            num_train_epochs(`float`, *optional*, defaults to 3.0):
                Total number of training epochs to perform (if not an integer, will perform the decimal part percents of
                the last epoch before stopping training).
            max_steps (`int`, *optional*, defaults to -1):
                If set to a positive number, the total number of training steps to perform. Overrides
                `num_train_epochs`. For a finite dataset, training is reiterated through the dataset
                (if all data is exhausted) until `max_steps` is reached.
            lr_scheduler_type (`str` or [`SchedulerType`], *optional*, defaults to `"linear"`):
                The scheduler type to use. See the documentation of [`SchedulerType`] for all possible values.
            warmup_ratio (`float`, *optional*, defaults to 0.0):
                Ratio of total training steps used for a linear warmup from 0 to `learning_rate`.
            warmup_steps (`int`, *optional*, defaults to 0):
                Number of steps used for a linear warmup from 0 to `learning_rate`. Overrides any effect of
                `warmup_ratio`.

            logging_strategy (`str` or [`~trainer_utils.IntervalStrategy`], *optional*, defaults to `"steps"`):
                The logging strategy to adopt during training. Possible values are:

                    - `"no"`: No logging is done during training.
                    - `"epoch"`: Logging is done at the end of each epoch.
                    - `"steps"`: Logging is done every `logging_steps`.
            logging_steps (`int` or `float`, *optional*, defaults to 500):
                Number of update steps between two logs if `logging_strategy="steps"`. Should be an integer or a float
                in range `[0,1)`. If smaller than 1, will be interpreted as ratio of total training steps.

            save_steps (`int` or `float`, *optional*, defaults to 500):
                Number of updates steps before two checkpoint saves if `save_strategy="steps"`. Should be an integer or
                a float in range `[0,1)`. If smaller than 1, will be interpreted as ratio of total training steps.
            save_total_limit (`int`, *optional*):
                If a value is passed, will limit the total amount of checkpoints. Deletes the older checkpoints in
                `output_dir`. When `load_best_model_at_end` is enabled, the "best" checkpoint according to
                `metric_for_best_model` will always be retained in addition to the most recent ones. For example, for
                `save_total_limit=5` and `load_best_model_at_end`, the four last checkpoints will always be retained
                alongside the best model. When `save_total_limit=1` and `load_best_model_at_end`, it is possible that
                two checkpoints are saved: the last one and the best one (if they are different).
            save_on_each_node (`bool`, *optional*, defaults to `False`):
                When doing multi-node distributed training, whether to save models and checkpoints on each node, or only
                on the main one.

                This should not be activated when the different nodes use the same storage as the files will be saved
                with the same names for each node.
            use_cpu (`bool`, *optional*, defaults to `False`):
                Whether to use cpu. If set to False, we will use cuda or mps device if available.
            seed (`int`, *optional*, defaults to 42):
                Random seed that will be set at the beginning of training. To ensure reproducibility across runs, use
                the [`~Trainer.model_init`] function to instantiate the model if it has some randomly initialized
                parameters.
            local_rank (`int`, *optional*, defaults to -1):
                Rank of the process during distributed training.

            dataloader_drop_last (`bool`, *optional*, defaults to `False`):
                Whether to drop the last incomplete batch (if the length of the dataset is not divisible by the batch
                size) or not.

            dataloader_num_workers (`int`, *optional*, defaults to 0):
                Number of subprocesses to use for data loading (PyTorch only). 0 means that the data will be loaded in
                the main process.

            label_names (`List[str]`, *optional*):
                The list of keys in your dictionary of inputs that correspond to the labels.

                Will eventually default to the list of argument names accepted by the model that contain the word
                "label", except if the model used is one of the `XxxForQuestionAnswering` in which case it will also
                include the `["start_positions", "end_positions"]` keys.
            load_best_model_at_end (`bool`, *optional*, defaults to `False`):
                Whether to load the best model found during training at the end of training. When this option is
                enabled, the best checkpoint will always be saved.

                <Tip>

                When set to `True`, the parameters `save_strategy` needs to be the same as `evaluation_strategy`, and in
                the case it is "steps", `save_steps` must be a round multiple of `eval_steps`.

                </Tip>

            metric_for_best_model (`str`, *optional*):
                Use in conjunction with `load_best_model_at_end` to specify the metric to use to compare two different
                models. Must be the name of a metric returned by the evaluation with or without the prefix `"eval_"`.
                Will default to `"loss"` if unspecified and `load_best_model_at_end=True` (to use the evaluation loss).

                If you set this value, `greater_is_better` will default to `True`. Don't forget to set it to `False` if
                your metric is better when lower.
            greater_is_better (`bool`, *optional*):
                Use in conjunction with `load_best_model_at_end` and `metric_for_best_model` to specify if better models
                should have a greater metric or not. Will default to:

                - `True` if `metric_for_best_model` is set to a value that isn't `"loss"` or `"eval_loss"`.
                - `False` if `metric_for_best_model` is not set, or set to `"loss"` or `"eval_loss"`.
            ignore_data_skip (`bool`, *optional*, defaults to `False`):
                When resuming training, Whether to skip the epochs and batches to get the data loading at the same
                stage as in the previous training. If set to `True`, the training will begin faster (as that skipping
                step can take a long time) but will not yield the same results as the interrupted training would have.
            label_smoothing_factor (`float`, *optional*, defaults to 0.0):
                The label smoothing factor to use. Zero means no label smoothing, otherwise the underlying
                onehot-encoded labels are changed from 0s and 1s to `label_smoothing_factor/num_labels` and
                `1 - label_smoothing_factor + label_smoothing_factor/num_labels` respectively.
            optim (`str` or [`training_args.OptimizerNames`], *optional*, defaults to `"adamw_torch"`):
                The optimizer to use: adamw_hf, adamw_torch, adamw_torch_fused, adamw_apex_fused, adamw_anyprecision or
                adafactor.
            optim_args (`str`, *optional*):
                Optional arguments that are supplied to AnyPrecisionAdamW.

            push_to_hub (`bool`, *optional*, defaults to `False`):
                Whether to push the model to the Hub every time the model is saved. If this is activated,
                `output_dir` will begin a git directory synced with the repo (determined by `hub_model_id`) and the
                content will be pushed each time a save is triggered (depending on your `save_strategy`). Calling
                [`~Trainer.save_model`] will also trigger a push.

                <Tip warning={true}>

                If `output_dir` exists, it needs to be a local clone of the repository to which the [`Trainer`] will be
                pushed.

                </Tip>

            resume_from_checkpoint (`str`, *optional*):
                The path to a folder with a valid checkpoint for your model. This argument is not directly used by
                [`Trainer`], it's intended to be used by your training/evaluation scripts instead.
            hub_model_id (`str`, *optional*):
                The name of the repository to keep in sync with the local *output_dir*. It can be a simple model ID in
                which case the model will be pushed in your namespace. Otherwise it should be the whole repository name,
                for instance `"user_name/model"`, which allows you to push to an organization you are a member of with
                `"organization_name/model"`. Will default to `user_name/output_dir_name` with *output_dir_name* being
                the name of `output_dir`.

                Will default to the name of `output_dir`.
            hub_strategy (`str` or [`~trainer_utils.HubStrategy`], *optional*, defaults to `"every_save"`):
                Defines the scope of what is pushed to the Hub and when. Possible values are:

                - `"end"`: push the model, its configuration, the tokenizer (if passed along to the [`Trainer`]) and a
                  draft of a model card when the [`~Trainer.save_model`] method is called.
                - `"every_save"`: push the model, its configuration, the tokenizer (if passed along to the [`Trainer`])
                and a draft of a model card each time there is a model save. The pushes are asynchronous to not block
                  training, and in case the save are very frequent, a new push is only attempted if the previous one is
                  finished. A last push is made with the final model at the end of training.
                - `"checkpoint"`: like `"every_save"` but the latest checkpoint is also pushed in a subfolder named
                  last-checkpoint, allowing you to resume training easily with
                  `trainer.train(resume_from_checkpoint="last-checkpoint")`.
                - `"all_checkpoints"`: like `"checkpoint"` but all checkpoints are pushed like they appear in the output
                  folder (so you will get one checkpoint folder per folder in your final repository)

            hub_token (`str`, *optional*):
                The token to use to push the model to the Hub.
            hub_private_repo (`bool`, *optional*, defaults to `False`):
                If True, the Hub repo will be set to private.
            hub_always_push (`bool`, *optional*, defaults to `False`):
                Unless this is `True`, the `Trainer` will skip pushing a checkpoint when the previous push is not
                finished.
            include_inputs_for_metrics (`bool`, *optional*, defaults to `False`):
                Whether the inputs will be passed to the `compute_metrics` function. This is intended for metrics
                that need inputs, predictions and references for scoring calculation in Metric class.

        pt:
            prediction_loss_only (`bool`, *optional*, defaults to `False`):
                When performing evaluation and generating predictions, only returns the loss.

            eval_accumulation_steps (`int`, *optional*):
                Number of predictions steps to accumulate the output tensors for, before moving the results to the CPU.
                If left unset, the whole predictions are accumulated on GPU/NPU/TPU before being moved to the CPU
                (faster but requires more memory).
            eval_delay (`float`, *optional*):
                Number of epochs or steps to wait for before the first evaluation can be performed, depending on the
                evaluation_strategy.
            log_level (`str`, *optional*, defaults to `passive`):
                Logger log level to use on the main process. Possible choices are the log levels as strings: 'debug',
                'info', 'warning', 'error' and 'critical', plus a 'passive' level which doesn't set anything and keeps
                the current log level for the Transformers library (which will be `"warning"` by default).
            log_level_replica (`str`, *optional*, defaults to `"warning"`):
                Logger log level to use on replicas. Same choices as `log_level`"
            log_on_each_node (`bool`, *optional*, defaults to `True`):
                In multinode distributed training, whether to log using `log_level` once per node, or only on the main
                node.
            logging_dir (`str`, *optional*):
                [TensorBoard](https://www.tensorflow.org/tensorboard) log directory. Will default to
                *output_dir/runs/**CURRENT_DATETIME_HOSTNAME***.
            logging_first_step (`bool`, *optional*, defaults to `False`):
                Whether to log and evaluate the first `global_step` or not.
            logging_nan_inf_filter (`bool`, *optional*, defaults to `True`):
                Whether to filter `nan` and `inf` losses for logging. If set to `True` the loss of every step that is
                `nan` or `inf` is filtered and the average loss of the current logging window is taken instead.

                <Tip>

                `logging_nan_inf_filter` only influences the logging of loss values, it does not change the behavior the
                gradient is computed or applied to the model.

                </Tip>
            save_strategy (`str` or [`~trainer_utils.IntervalStrategy`], *optional*, defaults to `"steps"`):
                The checkpoint save strategy to adopt during training. Possible values are:

                    - `"no"`: No save is done during training.
                    - `"epoch"`: Save is done at the end of each epoch.
                    - `"steps"`: Save is done every `save_steps`.
            save_safetensors (`bool`, *optional*, defaults to `True`):
                Use [safetensors](https://huggingface.co/docs/safetensors) saving and loading for state dicts instead of
                default `torch.load` and `torch.save`.
            data_seed (`int`, *optional*):
                Random seed to be used with data samplers. If not set, random generators for data sampling will use the
                same seed as `seed`. This can be used to ensure reproducibility of data sampling, independent of the
                model seed.
            jit_mode_eval (`bool`, *optional*, defaults to `False`):
                Whether to use PyTorch jit trace for inference.
            use_ipex (`bool`, *optional*, defaults to `False`):
                Use Intel extension for PyTorch when it is available. [IPEX
                installation](https://github.com/intel/intel-extension-for-pytorch).
            bf16 (`bool`, *optional*, defaults to `False`):
                Whether to use bf16 16-bit (mixed) precision training instead of 32-bit training. Requires Ampere or
                higher NVIDIA architecture or using CPU (use_cpu) or Ascend NPU. This is an experimental API and it may
                change.
            fp16 (`bool`, *optional*, defaults to `False`):
                Whether to use fp16 16-bit (mixed) precision training instead of 32-bit training.
            fp16_opt_level (`str`, *optional*, defaults to 'O1'):
                For `fp16` training, Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']. See details
                on the [Apex documentation](https://nvidia.github.io/apex/amp).
            fp16_backend (`str`, *optional*, defaults to `"auto"`):
                This argument is deprecated. Use `half_precision_backend` instead.
            half_precision_backend (`str`, *optional*, defaults to `"auto"`):
                The backend to use for mixed precision training. Must be one of `"auto", "apex", "cpu_amp"`. `"auto"`
                will use CPU/CUDA AMP or APEX depending on the PyTorch version detected, while the other choices will
                force the requested backend.
            bf16_full_eval (`bool`, *optional*, defaults to `False`):
                Whether to use full bfloat16 evaluation instead of 32-bit. This will be faster and save memory but can
                harm metric values. This is an experimental API and it may change.
            fp16_full_eval (`bool`, *optional*, defaults to `False`):
                Whether to use full float16 evaluation instead of 32-bit. This will be faster and save memory but can
                harm metric values.
            tf32 (`bool`, *optional*):
                Whether to enable the TF32 mode, available in Ampere and newer GPU architectures. The default value
                depends on PyTorch's version default of `torch.backends.cuda.matmul.allow_tf32`. For more details please
                refer to the [TF32](https://huggingface.co/docs/transformers/performance#tf32) documentation. This is an
                experimental API and it may change.
            ddp_backend (`str`, *optional*):
                The backend to use for distributed training. Must be one of `"nccl"`, `"mpi"`, `"ccl"`, `"gloo"`,
                `"hccl"`.
            tpu_num_cores (`int`, *optional*):
                When training on TPU, the number of TPU cores (automatically passed by launcher script).
            eval_steps (`int` or `float`, *optional*):
                Number of update steps between two evaluations if `evaluation_strategy="steps"`. Will default to the
                same value as `logging_steps` if not set. Should be an integer or a float in range `[0,1)`. If smaller
                than 1, will be interpreted as ratio of total training steps.
            past_index (`int`, *optional*, defaults to -1):
                Some models like [TransformerXL](../model_doc/transformerxl) or [XLNet](../model_doc/xlnet) can make
                use of the past hidden states for their predictions. If this argument is set to a positive int, the
                `Trainer` will use the corresponding output (usually index 2) as the past state and feed it to the model
                at the next training step under the keyword argument `mems`.
            run_name (`str`, *optional*):
                A descriptor for the run. Typically used for [wandb](https://www.wandb.com/) and
                [mlflow](https://www.mlflow.org/) logging.
            disable_tqdm (`bool`, *optional*):
                Whether to disable the tqdm progress bars and table of metrics produced by
                [`~notebook.NotebookTrainingTracker`] in Jupyter Notebooks. Will default to `True` if the logging level
                is set to warn or lower (default), `False` otherwise.
            remove_unused_columns (`bool`, *optional*, defaults to `True`):
                Whether to automatically remove the columns unused by the model forward method.

                (Note that this behavior is not implemented for [`TFTrainer`] yet.)
            fsdp (`bool`, `str` or list of [`~trainer_utils.FSDPOption`], *optional*, defaults to `''`):
                Use PyTorch Distributed Parallel Training (in distributed training only).

                A list of options along the following:

                - `"full_shard"`: Shard parameters, gradients and optimizer states.
                - `"shard_grad_op"`: Shard optimizer states and gradients.
                - `"hybrid_shard"`: Apply `FULL_SHARD` within a node, and replicate parameters across nodes.
                - `"hybrid_shard_zero2"`: Apply `SHARD_GRAD_OP` within a node, and replicate parameters across nodes.
                - `"offload"`: Offload parameters and gradients to CPUs (only compatible with `"full_shard"` and
                  `"shard_grad_op"`).
                - `"auto_wrap"`: Automatically recursively wrap layers with FSDP using `default_auto_wrap_policy`.
            fsdp_config (`str` or `dict`, *optional*):
                Config to be used with fsdp (Pytorch Distributed Parallel Training). The value is either a location of
                fsdp json config file (e.g., `fsdp_config.json`) or an already loaded json file as `dict`.

                A List of config and its options:
                - min_num_params (`int`, *optional*, defaults to `0`):
                    FSDP's minimum number of parameters for Default Auto Wrapping. (useful only when `fsdp` field is
                    passed).
                - transformer_layer_cls_to_wrap (`List[str]`, *optional*):
                    List of transformer layer class names (case-sensitive) to wrap, e.g, `BertLayer`, `GPTJBlock`,
                    `T5Block` .... (useful only when `fsdp` flag is passed).
                - backward_prefetch (`str`, *optional*)
                    FSDP's backward prefetch mode. Controls when to prefetch next set of parameters (useful only when
                    `fsdp` field is passed).

                    A list of options along the following:

                    - `"backward_pre"` : Prefetches the next set of parameters before the current set of parameter's
                      gradient
                        computation.
                    - `"backward_post"` : This prefetches the next set of parameters after the current set of
                      parameter’s
                        gradient computation.
                - forward_prefetch (`bool`, *optional*, defaults to `False`)
                    FSDP's forward prefetch mode (useful only when `fsdp` field is passed).
                     If `"True"`, then FSDP explicitly prefetches the next upcoming all-gather while executing in the
                     forward pass.
                - limit_all_gathers (`bool`, *optional*, defaults to `False`)
                    FSDP's limit_all_gathers (useful only when `fsdp` field is passed).
                     If `"True"`, FSDP explicitly synchronizes the CPU thread to prevent too many in-flight
                     all-gathers.
                - use_orig_params (`bool`, *optional*, defaults to `True`)
                    If `"True"`, allows non-uniform `requires_grad` during init, which means support for interspersed
                    frozen and trainable paramteres. Useful in cases such as parameter-efficient fine-tuning. Please
                    refer this
                    [blog](https://dev-discuss.pytorch.org/t/
                    rethinking-pytorch-fully-sharded-data-parallel-fsdp-from-first-principles/1019)
                - sync_module_states (`bool`, *optional*, defaults to `True`)
                    If `"True"`, each individually wrapped FSDP unit will broadcast module parameters from rank 0 to
                    ensure they are the same across all ranks after initialization
                - activation_checkpointing (`bool`, *optional*, defaults to `False`):
                    If `"True"`, activation checkpointing is a technique to reduce memory usage by clearing activations
                    of certain layers and recomputing them during a backward pass. Effectively, this trades extra
                    computation time for reduced memory usage.
                - xla (`bool`, *optional*, defaults to `False`):
                    Whether to use PyTorch/XLA Fully Sharded Data Parallel Training. This is an experimental feature
                    and its API may evolve in the future.
                - xla_fsdp_settings (`dict`, *optional*)
                    The value is a dictionary which stores the XLA FSDP wrapping parameters.

                    For a complete list of options, please see [here](
                    https://github.com/pytorch/xla/blob/master/torch_xla/distributed/fsdp/xla_fully_sharded_data_parallel.py).
                - xla_fsdp_grad_ckpt (`bool`, *optional*, defaults to `False`):
                    Will use gradient checkpointing over each nested XLA FSDP wrapped layer. This setting can only be
                    used when the xla flag is set to true, and an auto wrapping policy is specified through
                    fsdp_min_num_params or fsdp_transformer_layer_cls_to_wrap.

            deepspeed (`str` or `dict`, *optional*):
                Use [Deepspeed](https://github.com/microsoft/deepspeed). This is an experimental feature and its API may
                evolve in the future. The value is either the location of DeepSpeed json config file (e.g.,
                `ds_config.json`) or an already loaded json file as a `dict`"
            debug (`str` or list of [`~debug_utils.DebugOption`], *optional*, defaults to `""`):
                Enable one or more debug features. This is an experimental feature.

                Possible options are:

                - `"underflow_overflow"`: detects overflow in model's input/outputs and reports the last frames that led
                to the event
                - `"tpu_metrics_debug"`: print debug metrics on TPU

                The options should be separated by whitespaces.
            group_by_length (`bool`, *optional*, defaults to `False`):
                Whether to group together samples of roughly the same length in the training dataset (to minimize
                padding applied and be more efficient). Only useful if applying dynamic padding.
            length_column_name (`str`, *optional*, defaults to `"length"`):
                Column name for precomputed lengths. If the column exists, grouping by length will use these values
                rather than computing them on train startup. Ignored unless `group_by_length` is `True` and the dataset
                is an instance of `Dataset`.
            report_to (`str` or `List[str]`, *optional*, defaults to `"all"`):
                The list of integrations to report the results and logs to. Supported platforms are `"azure_ml"`,
                `"clearml"`, `"codecarbon"`, `"comet_ml"`, `"dagshub"`, "dvclive"`, `"flyte"`, `"mlflow"`, `"neptune"`,
                `"tensorboard"`, and `"wandb"`. Use `"all"` to report to all integrations installed, `"none"` for no
                integrations.
            ddp_find_unused_parameters (`bool`, *optional*):
                When using distributed training, the value of the flag `find_unused_parameters` passed to
                `DistributedDataParallel`. Will default to `False` if gradient checkpointing is used, `True` otherwise.
            ddp_bucket_cap_mb (`int`, *optional*):
                When using distributed training, the value of the flag `bucket_cap_mb` passed to
                `DistributedDataParallel`.
            ddp_broadcast_buffers (`bool`, *optional*):
                When using distributed training, the value of the flag `broadcast_buffers` passed to
                `DistributedDataParallel`. Will default to `False` if gradient checkpointing is used, `True` otherwise.
            dataloader_pin_memory (`bool`, *optional*, defaults to `True`):
                Whether you want to pin memory in data loaders or not. Will default to `True`.
            dataloader_persistent_workers (`bool`, *optional*, defaults to `False`):
                If True, the data loader will not shut down the worker processes after a dataset has been consumed once.
                This allows to maintain the workers Dataset instances alive. Can potentially speed up training, but will
                increase RAM usage. Will default to `False`.
            skip_memory_metrics (`bool`, *optional*, defaults to `True`):
                Whether to skip adding of memory profiler reports to metrics. This is skipped by default because it
                slows down the training and evaluation speed.
            gradient_checkpointing (`bool`, *optional*, defaults to `False`):
                If True, use gradient checkpointing to save memory at the expense of slower backward pass.
            gradient_checkpointing_kwargs (`dict`, *optional*, defaults to `None`):
            Key word arguments to be passed to the `gradient_checkpointing_enable` method.
            auto_find_batch_size (`bool`, *optional*, defaults to `False`)
                Whether to find a batch size that will fit into memory automatically through exponential decay, avoiding
                CUDA Out-of-Memory errors. Requires accelerate to be installed (`pip install accelerate`)
            full_determinism (`bool`, *optional*, defaults to `False`)
                If `True`, [`enable_full_determinism`] is called instead of [`set_seed`] to ensure reproducible results
                in distributed training. Important: this will negatively impact the performance, so only use it for
                debugging.
            torchdynamo (`str`, *optional*):
                If set, the backend compiler for TorchDynamo. Possible choices are `"eager"`, `"aot_eager"`,
                `"inductor"`, `"nvfuser"`, `"aot_nvfuser"`, `"aot_cudagraphs"`, `"ofi"`, `"fx2trt"`, `"onnxrt"` and
                `"ipex"`.
            ray_scope (`str`, *optional*, defaults to `"last"`):
                The scope to use when doing hyperparameter search with Ray. By default, `"last"` will be used. Ray will
                then use the last checkpoint of all trials, compare those, and select the best one. However, other
                options are also available. See the [Ray documentation](
                https://docs.ray.io/en/latest/tune/api_docs/analysis.html#ray.tune.ExperimentAnalysis.get_best_trial)
                for more options.
            ddp_timeout (`int`, *optional*, defaults to 1800):
                The timeout for `torch.distributed.init_process_group` calls, used to avoid GPU socket timeouts when
                performing slow operations in distributed runnings. Please refer the [PyTorch documentation]
                (https://pytorch.org/docs/stable/distributed.html#torch.distributed.init_process_group) for more
                information.
            use_mps_device (`bool`, *optional*, defaults to `False`):
                This argument is deprecated.`mps` device will be used if it is available similar to `cuda` device.
            torch_compile (`bool`, *optional*, defaults to `False`):
                Whether to compile the model using PyTorch 2.0
                [`torch.compile`](https://pytorch.org/get-started/pytorch-2.0/).

                This will use the best defaults for the [`torch.compile`API]
                (https://pytorch.org/docs/stable/generated/torch.compile.html?highlight=torch+compile#torch.compile).
                You can customize the defaults with the argument `torch_compile_backend` and `torch_compile_mode` but we
                don't guarantee any of them will work as the support is progressively rolled in in PyTorch.

                This flag and the whole compile API is experimental and subject to change in future releases.
            torch_compile_backend (`str`, *optional*):
                The backend to use in `torch.compile`. If set to any value, `torch_compile` will be set to `True`.

                Refer to the PyTorch doc for possible values and note that they may change across PyTorch versions.

                This flag is experimental and subject to change in future releases.
            torch_compile_mode (`str`, *optional*):
                The mode to use in `torch.compile`. If set to any value, `torch_compile` will be set to `True`.

                Refer to the PyTorch doc for possible values and note that they may change across PyTorch versions.

                This flag is experimental and subject to change in future releases.
            split_batches (`bool`, *optional*):
                Whether the accelerator should split the batches yielded by the dataloaders across the devices
                during distributed training. If

                set to `True`, the actual batch size used will be the same on any kind of distributed processes, but it
                must be a

                round multiple of the number of processes you are using (such as GPUs).
            include_tokens_per_second (`bool`, *optional*):
                Whether to compute the number of tokens per second per device for training speed metrics.

                This will iterate over the entire training dataloader once beforehand,

                and will slow down the entire process.

            include_num_input_tokens_seen (`bool`, *optional*):
                Whether to track the number of input tokens seen throughout training.

                May be slower in distributed training as gather operations must be called.

            neftune_noise_alpha (`Optional[float]`):
                If not `None`, this will activate NEFTune noise embeddings. This can drastically improve model
                performance for instruction fine-tuning. Check out the
                [original paper](https://arxiv.org/abs/2310.05914) and the
                [original code](https://github.com/neelsjain/NEFTune).
                Support transformers `PreTrainedModel` and also `PeftModel` from peft.
            lr_scheduler_kwargs ('dict', *optional*, defaults to {}):
                The extra arguments for the lr_scheduler. See the documentation of each scheduler for possible values.
            save_only_model (`bool`, *optional*, defaults to `False`):
                When checkpointing, whether to only save the model, or also the optimizer, scheduler & rng state.
                Note that when this is true, you won't be able to resume training from checkpoint.
                This enables you to save storage by not storing the optimizer, scheduler & rng state.
                You can only load the model using `from_pretrained` with this option set to `True`.
        ms:
            only_save_strategy (`bool`, *optional*, defaults to `False`):
                Whether only save the strategy file in `output_dir/strategy`. Only takes effect when `use_parallel` is
                True.
            auto_trans_ckpt (`bool`, *optional*, defaults to `False`):
                Whether to transform checkpoint according to parallel config. See the [Transform_Ckpt documentation](
                https://gitee.com/mindspore/mindformers/blob/dev/docs/feature_cards/Transform_Ckpt.md) for more details.
            src_strategy (`str`, *optional*):
                The strategy file or dir used for transforming checkpoint when auto_trans_ckpt is True.
            remote_save_url (`str`, *optional*):
                The OBS output dir when training on ModeArts.
            sink_mode (`bool`, defaults to `True`):
                Whether to directly sink data to the Device through a channel.
            sink_size (`int`, defaults to 2):
                The data sink number per step for training or evaluation.
            mode (`int`, defaults to 0):
                Indicates running in GRAPH_MODE(0) or PYNATIVE_MODE(1).
            device_id (`int`, defaults to 0):
                The default device id for execution.
            device_target (`str`, defaults to `"Ascend"`):
                The target device for execution, supporting 'Ascend', 'GPU', and 'CPU'.
            enable_graph_kernel (`bool`, defaults to `False`):
                Whether to enable graph fusion. Default: False.
            graph_kernel_flags (`str`, defaults to `"--disable_expand_ops=Softmax,Dropout --enable_parallel_fusion=true
                                --reduce_fuse_depth=8 --enable_auto_tensor_inplace=true"`):
                Graph fusion level.
            max_call_depth (`int`, defaults to 10000):
                Maximum depth of function calls.
            max_device_memory (`str`, defaults to `"31GB"`):
                Maximum available memory of the device.
            save_graphs (`bool`, defaults to `False`):
                Whether to save intermediate compilation graphs.
            save_graphs_path (`str`, defaults to `"./graph"`):
                Path to save intermediate compilation graphs.
            use_parallel (`bool`, defaults to `False`):
                Whether enable distribute parallel of the network.
            parallel_mode (`int`, defaults to 1):
                Indicates running with Data Parallel(0) or Semi-Auto Parallel(1) or Auto Parallel(2) or Hybrid
                Parallel(3).
            enable_alltoall (`bool`, defaults to `False`):
                Whether allow generation of AllToAll communication operators during communication.
                Typically only turned on in MOE scenarios, default is False.
            full_batch (`bool`, defaults to `True`):
                If the entire batch dataset is loaded in auto_parallel mode, then full_batch should be set to True.
                It is currently not recommended to use this interface, please replace it with dataset_strategy.
            dataset_strategy (`str` or `tuple`, defaults to `"full_batch"`):
                Dataset sharding strategy. Semi-auto parallel mode is usually set to 'full_batch',
                while data parallel mode must be set to 'data_parallel'. Possible choices are `"full_batch"`,
                `"data_parallel"`.
            search_mode (`str`, defaults to `"sharding_propagation"`):
                Strategy search mode, Only effective in Auto Parallel mode, experimental interface, use with caution.
                Possible choices are `"recursive_programming"`, `"dynamic_programming"`, `"sharding_propagation"`.
            enable_parallel_optimizer (`bool`, defaults to `True`):
                Whether enable optimizer parallel.
            gradient_accumulation_shard (`bool`, defaults to `True`):
                Whether the accumulated gradient variable is split along the data parallel dimension. It will reduce
                the memory usage of model, but will introduce additional communication operators (ReduceScatter) during
                the backward gradient calculation. It is only effective in pipeline parallel training and gradient
                accumulation mode.
            parallel_optimizer_threshold (`int`, defaults to 64):
                Set the threshold for parameter splitting.
            optimizer_weight_shard_size (`int`, defaults to -1):
                Set the size of the communication domain for the specified optimizer weight splitting. Effective only
                when optimizer parallelism is enabled. The numerical range can be (0, device_num], and if pipeline
                parallelism is also enabled, the range becomes (0, device_num/stage]. If the data parallel
                communication domain size of a parameter is not divisible by optimizer_weight_shard_size, then
                the specified optimizer weight splitting communication domain size will not be effective. Default: -1,
                which means the optimizer weight slice communication domain size is the data parallel communication
                domain size of each parameter.
            strategy_ckpt_save_file (`str`, defaults to `"./ckpt_strategy.ckpt"`)
                Path for saving distributed strategy file.
            data_parallel (`int`, defaults to 1):
                The split number of data parallel.
            model_parallel (`int`, defaults to 1):
                The split number of model parallel.
            pipeline_stage (`int`, defaults to 1):
                The number of pipeline stage.
            micro_batch_num (`int`, defaults to 1):
                The number of micro batch num. Only takes effect when `pipeline_stage` > 1.
            gradient_aggregation_group (`int`, defaults to 4):mup_ratio
                The size of the gradient communication operator fusion group.
            micro_batch_interleave_num (`int`, defaults to 1):
                Enable multi-replica parallel when `micro_batch_interleave_num` > 1, it is recommended set to 2 in
                model parallel. It is used for optimizing communication overhead incurred during model_parallel
                execution. However, it will incur additional memory overhead. It is not recommended for use in pure
                pipeline parallel.
            use_seq_parallel (`bool`, defaults to `False`):
                Whether enable seq parallel.
            vocab_emb_dp (`bool`, defaults to `True`):
                Whether to split the vocabulary only along the dp dimension.
            recompute (`bool`, defaults to `False`):
                Whether enable recompute mode.
            select_recompute (`bool`, defaults to `False`):
                Whether enable select recompute mode.
            parallel_optimizer_comm_recompute (`bool`, defaults to `False`):
                Whether to recompute the AllGather communication introduced by optimizer parallel.
            mp_comm_recompute (`bool`, defaults to `True`):
                Whether to recompute the communication operations introduced by model parallel.
            recompute_slice_activation (`bool`, defaults to `True`):
                Whether to slice the Cell outputs retained in memory.
            lr_end (`float`, defaults to `1.e-6`):
                The end learning rate.
            layer_scale (`bool`, defaults to `False`):
                Whether to enable layer decay.
            layer_decay (`float`, defaults to `0.65`):
                Layer decay coefficient.
            lr_scale (`bool`, defaults to `False`):
                Whether to enable learning rate scaling.
            lr_scale_factor (`int`, defaults to 256):
                Learning rate scaling factor.
            dataset_task (`str`, defaults to `"CausalLanguageModelDataset"`):
                Dataset task name.
            dataset_type (`str`, defaults to `"MindDataset"`):
                Dataset type.
            train_dataset (`str`, *optional*):
                Train dataset path.
            train_dataset_columns (`List[str]`, defaults to `[input_ids]`):
                Train dataset column names.
            shuffle (`bool`, defaults to `True`):
                Whether shuffle train dataset.
            repeat (`int`, defaults to 1):
                Repeat train dataset count times. If count is None or -1, iterate infinitely.
            eval_dataset (`str`, *optional*):
                Eval dataset path.
            eval_dataset_columns (`List[str]`, defaults to `[input_ids]`):
                Eval dataset column names.
            python_multiprocessing (`bool`, defaults to `False`):
                Whether to start Python multiprocessing mode to execute per_batch_map in parallel,
                where 'True' indicates Python multiprocessing mode, and 'False' indicates Python multithreading mode.
            numa_enable (`bool`, defaults to `False`):
                Set the default state of NUMA to the enabled state.
            prefetch_size (`int`, defaults to 1):
                Set the queue capacity of threads in the pipeline. A larger prefetch_size can reduce the overall
                processing latency when there is an imbalance in the throughput rate of adjacent operations,
                but it also consumes more system memory.
            wrapper_type (`str`, defaults to `"MFTrainOneStepCell"`):
                Class name of wrapper.
            scale_sense_type (`str`, defaults to `"DynamicLossScaleUpdateCell"`):
                Class name of scale sense.
            loss_scale_value (`int`, defaults to 65536):
                Initial loss scaling factor.
            loss_scale_factor (`int`, defaults to 2):
                Increment and decrement factor for loss scaling coefficient.
            loss_scale_window (`int`, defaults to 1000):
                Maximum consecutive training steps to increase the loss scaling coefficient when there is no overflow.
            use_clip_grad (`bool`, defaults to `False`):
                Whether enable gradient clipping.
            save_seconds (`int`, *Optional*):
                Save checkpoint every X updates seconds.
            eval_epochs (`int`, *Optional*):
                Num of epoch intervals between each eval, 1 means eval on every epoch end.
            profile (`bool`, defaults to `False`):
                Whether to enable the profile performance analysis tool.
            profile_start_step (`int`, defaults to 1):
                Start step for performance analysis.
            profile_end_step (`int`, defaults to 10):
                End step for performance analysis.
            init_start_profile (`bool`, defaults to `False`):
                Whether to enable data collection at the time of Profiler initialization.
                Once enabled, profile_start_step will not be effective. It must be enabled
                if multi-device communication data needs to be collected.
            profile_communication (`bool`, defaults to `False`):
                Whether to collect communication performance data in multi-device training.
            profile_memory (`bool`, defaults to `True`):
                Whether to collect Tensor memory data.
            auto_tune (`bool`, defaults to `False`):
                Whether to enable automatic data acceleration.
            filepath_prefix (`str`, defaults to `"./autotune"`):
                The save path and file prefix for the optimized global configuration.
            autotune_per_step (`int`, defaults to 10):
                Set the step interval for adjusting the configuration of automatic data acceleration.
    """

    def __post_init__(self):
        super().__post_init__()

    def __str__(self):
        return super().__str__()

    __repr__ = __str__

    @property
    def train_batch_size(self) -> int:
        return super().train_batch_size

    @property
    def eval_batch_size(self) -> int:
        return super().eval_batch_size

    @property
    def world_size(self):
        """
        The number of processes used in parallel.
        """
        return super().world_size

    @property
    def process_index(self):
        """
        The index of the current process used.
        """
        return super().process_index

    @property
    def local_process_index(self):
        """
        The index of the local process used.
        """
        return super().local_process_index

    @property
    def should_log(self):
        """
        Whether the current process should produce log.
        """
        return super().should_log

    @property
    def should_save(self):
        """
        Whether the current process should write to disk, e.g., to save models and checkpoints.
        """
        return super().should_save

    @property
    def device(self):
        """
        The device used by this process.
        """
        return super().device

    @cached_property
    def _setup_devices(self):
        return super()._setup_devices

    def get_process_log_level(self):
        return super().get_process_log_level()

    def main_process_first(self, local=True, desc="work"):
        """
        A context manager for torch distributed environment where on needs to do something on the main process, while
        blocking replicas, and when it's finished releasing the replicas.

        One such use is for `datasets`'s `map` feature which to be efficient should be run once on the main process,
        which upon completion saves a cached version of results and which then automatically gets loaded by the
        replicas.

        Args:
            local (`bool`, *optional*, defaults to `True`):
                if `True` first means process of rank 0 of each node if `False` first means process of rank 0 of node
                rank 0 In multi-node environment with a shared filesystem you most likely will want to use
                `local=False` so that only the main process of the first node will do the processing. If however, the
                filesystem is not shared, then the main process of each node will need to do the processing, which is
                the default behavior.
            desc (`str`, *optional*, defaults to `"work"`):
                a work description to be used in debug logs

        """
        return super().main_process_first(local, desc)

    def get_warmup_steps(self, num_training_steps: int):
        """
        Get number of steps used for a linear warmup.
        """

        return super().get_warmup_steps(num_training_steps)

    def to_dict(self):
        """
        Serializes this instance while replace `Enum` by their values (for JSON serialization support). It obfuscates
        the token values by removing their value.
        """
        return super().to_dict()

    def to_json_string(self):
        """
        Serializes this instance to a JSON string.
        """
        return super().to_json_string()

    def to_sanitized_dict(self) -> Dict[str, Any]:
        """
        Sanitized serialization to use with TensorBoard's hparams
        """

        return super().to_sanitized_dict()

    def set_training(
        self,
        learning_rate: float = 5e-5,
        batch_size: int = 8,
        weight_decay: float = 0,
        num_epochs: float = 3,
        max_steps: int = -1,
        gradient_accumulation_steps: int = 1,
        seed: int = 42,
        **kwargs,
    ):
        """
        A method that regroups all basic arguments linked to the training.

        <Tip>

        Calling this method will automatically set `self.do_train` to `True`.

        </Tip>

        Args:
            learning_rate (`float`, *optional*, defaults to 5e-5):
                The initial learning rate for the optimizer.
            batch_size (`int` *optional*, defaults to 8):
                The batch size per device (GPU/TPU core/CPU...) used for training.
            weight_decay (`float`, *optional*, defaults to 0):
                The weight decay to apply (if not zero) to all layers except all bias and LayerNorm weights in the
                optimizer.
            num_epochs(`float`, *optional*, defaults to 3.0):
                Total number of training epochs to perform (if not an integer, will perform the decimal part percents
                of the last epoch before stopping training).
            max_steps (`int`, *optional*, defaults to -1):
                If set to a positive number, the total number of training steps to perform.
                Overrides `num_train_epochs`. For a finite dataset, training is reiterated through the dataset
                (if all data is exhausted) until `max_steps` is reached.
            gradient_accumulation_steps (`int`, *optional*, defaults to 1):
                Number of updates steps to accumulate the gradients for, before performing a backward/update pass.

                <Tip warning={true}>

                When using gradient accumulation, one step is counted as one step with backward pass. Therefore,
                logging, evaluation, save will be conducted every `gradient_accumulation_steps * xxx_step` training
                examples.

                </Tip>

            seed (`int`, *optional*, defaults to 42):
                Random seed that will be set at the beginning of training. To ensure reproducibility across runs, use
                the [`~Trainer.model_init`] function to instantiate the model if it has some randomly initialized
                parameters.
            kwargs:
                pt:
                    gradient_checkpointing (`bool`, *optional*, defaults to `False`):
                        If True, use gradient checkpointing to save memory at the expense of slower backward pass.
                ms: NOTE

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_training(learning_rate=1e-4, batch_size=32)
        >>> args.learning_rate
        1e-4
        ```
        """
        return super().set_training(
            learning_rate=learning_rate,
            batch_size=batch_size,
            weight_decay=weight_decay,
            num_epochs=num_epochs,
            max_steps=max_steps,
            gradient_accumulation_steps=gradient_accumulation_steps,
            seed=seed,
            **kwargs,
        )

    def set_evaluate(
        self, strategy: Union[str, IntervalStrategy] = "no", steps: int = 500, batch_size: int = 8, **kwargs
    ):
        """
        A method that regroups all arguments linked to evaluation.

        Args:
            strategy (`str` or [`~trainer_utils.IntervalStrategy`], *optional*, defaults to `"no"`):
                The evaluation strategy to adopt during training. Possible values are:

                    - `"no"`: No evaluation is done during training.
                    - `"steps"`: Evaluation is done (and logged) every `steps`.
                    - `"epoch"`: Evaluation is done at the end of each epoch.

                Setting a `strategy` different from `"no"` will set `self.do_eval` to `True`.
            steps (`int`, *optional*, defaults to 500):
                Number of update steps between two evaluations if `strategy="steps"`.
            batch_size (`int` *optional*, defaults to 8):
                The batch size per device (GPU/TPU core/CPU...) used for evaluation.
            kwargs:
                pt:
                    accumulation_steps (`int`, *optional*):
                        Number of predictions steps to accumulate the output tensors for, before moving the results to
                        the CPU. If left unset, the whole predictions are accumulated on GPU/TPU before being moved to
                        the CPU (faster but requires more memory).
                    delay (`float`, *optional*):
                        Number of epochs or steps to wait for before the first evaluation can be performed, depending
                        on the evaluation_strategy.
                    loss_only (`bool`, *optional*, defaults to `False`):
                        Ignores all outputs except the loss.
                    jit_mode (`bool`, *optional*):
                        Whether to use PyTorch jit trace for inference.
                ms: NOTE
        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_evaluate(strategy="steps", steps=100)
        >>> args.eval_steps
        100
        ```
        """
        return super().set_evaluate(strategy=strategy, steps=steps, batch_size=batch_size, **kwargs)

    def set_testing(self, batch_size: int = 8, **kwargs):
        """
        A method that regroups all basic arguments linked to testing on a held-out dataset.

        <Tip>

        Calling this method will automatically set `self.do_predict` to `True`.

        </Tip>

        Args:
            batch_size (`int` *optional*, defaults to 8):
                The batch size per device (GPU/TPU core/CPU...) used for testing.
            kwargs:
                pt:
                    loss_only (`bool`, *optional*, defaults to `False`):
                        Ignores all outputs except the loss.
                    jit_mode (`bool`, *optional*):
                        Whether to use PyTorch jit trace for inference.

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_testing(batch_size=32)
        >>> args.per_device_eval_batch_size
        32
        ```
        """

        return super().set_testing(batch_size=batch_size, **kwargs)

    def set_save(
        self,
        strategy: Union[str, IntervalStrategy] = "steps",
        steps: int = 500,
        total_limit: Optional[int] = None,
        on_each_node: bool = False,
    ):
        """
        A method that regroups all arguments linked to checkpoint saving.

        Args:
            strategy (`str` or [`~trainer_utils.IntervalStrategy`], *optional*, defaults to `"steps"`):
                The checkpoint save strategy to adopt during training. Possible values are:

                    - `"no"`: No save is done during training.
                    - `"epoch"`: Save is done at the end of each epoch.
                    - `"steps"`: Save is done every `save_steps`.

            steps (`int`, *optional*, defaults to 500):
                Number of updates steps before two checkpoint saves if `strategy="steps"`.
            total_limit (`int`, *optional*):
                If a value is passed, will limit the total amount of checkpoints. Deletes the older checkpoints in
                `output_dir`.
            on_each_node (`bool`, *optional*, defaults to `False`):
                When doing multi-node distributed training, whether to save models and checkpoints on each node, or
                only on the main one.

                This should not be activated when the different nodes use the same storage as the files will be saved
                with the same names for each node.

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_save(strategy="steps", steps=100)
        >>> args.save_steps
        100
        ```
        """
        return super().set_save(strategy=strategy, steps=steps, total_limit=total_limit, on_each_node=on_each_node)

    def set_logging(
        self,
        strategy: Union[str, IntervalStrategy] = "steps",
        steps: int = 500,
        report_to: Union[str, List[str]] = "none",
        level: str = "passive",
        first_step: bool = False,
        nan_inf_filter: bool = False,
        on_each_node: bool = False,
        replica_level: str = "passive",
    ):
        """
        A method that regroups all arguments linked to logging.

        Args:
            strategy (`str` or [`~trainer_utils.IntervalStrategy`], *optional*, defaults to `"steps"`):
                The logging strategy to adopt during training. Possible values are:

                    - `"no"`: No save is done during training.
                    - `"epoch"`: Save is done at the end of each epoch.
                    - `"steps"`: Save is done every `save_steps`.

            steps (`int`, *optional*, defaults to 500):
                Number of update steps between two logs if `strategy="steps"`.
            level (`str`, *optional*, defaults to `"passive"`):
                Logger log level to use on the main process. Possible choices are the log levels as strings: `"debug"`,
                `"info"`, `"warning"`, `"error"` and `"critical"`, plus a `"passive"` level which doesn't set anything
                and lets the application set the level.
            report_to (`str` or `List[str]`, *optional*, defaults to `"all"`):
                The list of integrations to report the results and logs to. Supported platforms are `"azure_ml"`,
                `"clearml"`, `"codecarbon"`, `"comet_ml"`, `"dagshub"`, `"dvclive"`, `"flyte"`, `"mlflow"`,
                `"neptune"`, `"tensorboard"`, and `"wandb"`. Use `"all"` to report to all integrations installed,
                `"none"` for no integrations.
            first_step (`bool`, *optional*, defaults to `False`):
                Whether to log and evaluate the first `global_step` or not.
            nan_inf_filter (`bool`, *optional*, defaults to `True`):
                Whether to filter `nan` and `inf` losses for logging. If set to `True` the loss of every step that is
                `nan` or `inf` is filtered and the average loss of the current logging window is taken instead.

                <Tip>

                `nan_inf_filter` only influences the logging of loss values, it does not change the behavior the
                gradient is computed or applied to the model.

                </Tip>

            on_each_node (`bool`, *optional*, defaults to `True`):
                In multinode distributed training, whether to log using `log_level` once per node, or only on the main
                node.
            replica_level (`str`, *optional*, defaults to `"passive"`):
                Logger log level to use on replicas. Same choices as `log_level`

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_logging(strategy="steps", steps=100)
        >>> args.logging_steps
        100
        ```
        """
        return super().set_logging(
            strategy=strategy,
            steps=steps,
            report_to=report_to,
            level=level,
            first_step=first_step,
            nan_inf_filter=nan_inf_filter,
            on_each_node=on_each_node,
            replica_level=replica_level,
        )

    def set_push_to_hub(
        self,
        model_id: str,
        strategy: Union[str, HubStrategy] = "every_save",
        token: Optional[str] = None,
        private_repo: bool = False,
        always_push: bool = False,
    ):
        """
        A method that regroups all arguments linked to synchronizing checkpoints with the Hub.

        <Tip>

        Calling this method will set `self.push_to_hub` to `True`, which means the `output_dir` will begin a git
        directory synced with the repo (determined by `model_id`) and the content will be pushed each time a save is
        triggered (depending on`self.save_strategy`). Calling [`~Trainer.save_model`] will also trigger a push.

        </Tip>

        Args:
            model_id (`str`):
                The name of the repository to keep in sync with the local *output_dir*. It can be a simple model ID in
                which case the model will be pushed in your namespace. Otherwise, it should be the whole repository
                name, for instance `"user_name/model"`, which allows you to push to an organization you are a member of
                with `"organization_name/model"`.
            strategy (`str` or [`~trainer_utils.HubStrategy`], *optional*, defaults to `"every_save"`):
                Defines the scope of what is pushed to the Hub and when. Possible values are:

                - `"end"`: push the model, its configuration, the tokenizer (if passed along to the [`Trainer`]) and a
                draft of a model card when the [`~Trainer.save_model`] method is called.
                - `"every_save"`: push the model, its configuration, the tokenizer (if passed along to the [`Trainer`])
                  and
                a draft of a model card each time there is a model save. The pushes are asynchronous to not block
                training, and in case the save are very frequent, a new push is only attempted if the previous one is
                finished. A last push is made with the final model at the end of training.
                - `"checkpoint"`: like `"every_save"` but the latest checkpoint is also pushed in a subfolder named
                last-checkpoint, allowing you to resume training easily with
                `trainer.train(resume_from_checkpoint="last-checkpoint")`.
                - `"all_checkpoints"`: like `"checkpoint"` but all checkpoints are pushed like they appear in the
                  output
                folder (so you will get one checkpoint folder per folder in your final repository)

            token (`str`, *optional*):
                The token to use to push the model to the Hub.
            private_repo (`bool`, *optional*, defaults to `False`):
                If True, the Hub repo will be set to private.
            always_push (`bool`, *optional*, defaults to `False`):
                Unless this is `True`, the `Trainer` will skip pushing a checkpoint when the previous push is not
                finished.

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_push_to_hub("me/awesome-model")
        >>> args.hub_model_id
        'me/awesome-model'
        ```
        """

        rsp = super().set_push_to_hub(
            model_id=model_id, strategy=strategy, token=token, private_repo=private_repo, always_push=always_push
        )

        del token
        gc.collect()

        return rsp

    def set_optimizer(
        self,
        name: Union[str, OptimizerNames],
        learning_rate: float = 5e-5,
        weight_decay: float = 0,
        beta1: float = 0.9,
        beta2: float = 0.999,
        epsilon: float = 1e-8,
        **kwargs,
    ):
        """
        A method that regroups all arguments linked to the optimizer and its hyperparameters.

        Args:
            name (`str` or [`training_args.OptimizerNames`]`):
                The optimizer name.
            learning_rate (`float`, *optional*, defaults to 5e-5):
                The initial learning rate.
            weight_decay (`float`, *optional*, defaults to 0):
                The weight decay to apply (if not zero) to all layers except all bias and LayerNorm weights.
            beta1 (`float`, *optional*, defaults to 0.9):
                The beta1 hyperparameter for the adam optimizer or its variants.
            beta2 (`float`, *optional*, defaults to 0.999):
                The beta2 hyperparameter for the adam optimizer or its variants.
            epsilon (`float`, *optional*, defaults to 1e-8):
                The epsilon hyperparameter for the adam optimizer or its variants.
            kwargs:
                pt:
                    args (`str`, *optional*):
                        Optional arguments that are supplied to AnyPrecisionAdamW (only useful when
                        `optim="adamw_anyprecision"`).
        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_optimizer(name="adamw_torch",beta1=0.8)
        >>> args.optim
        'adamw_torch'
        ```
        """
        return super().set_optimizer(
            name=name,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            beta1=beta1,
            beta2=beta2,
            epsilon=epsilon,
            **kwargs,
        )

    def set_lr_scheduler(
        self,
        name: Union[str, SchedulerType] = "linear",
        num_epochs: float = 3.0,
        max_steps: int = -1,
        warmup_ratio: float = 0,
        warmup_steps: int = 0,
    ):
        """
        A method that regroups all arguments linked to the learning rate scheduler and its hyperparameters.

        Args:
            name (`str` or [`SchedulerType`], *optional*, defaults to `"linear"`):
                The scheduler type to use. See the documentation of [`SchedulerType`] for all possible values.
            num_epochs(`float`, *optional*, defaults to 3.0):
                Total number of training epochs to perform (if not an integer, will perform the decimal part percents
                of the last epoch before stopping training).
            max_steps (`int`, *optional*, defaults to -1):
                If set to a positive number, the total number of training steps to perform.
                Overrides `num_train_epochs`.
                For a finite dataset, training is reiterated through the dataset (if all data is exhausted) until
                `max_steps` is reached.
            warmup_ratio (`float`, *optional*, defaults to 0.0):
                Ratio of total training steps used for a linear warmup from 0 to `learning_rate`.
            warmup_steps (`int`, *optional*, defaults to 0):
                Number of steps used for a linear warmup from 0 to `learning_rate`. Overrides any effect of
                `warmup_ratio`.

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_lr_scheduler(name="cosine", warmup_ratio=0.05)
        >>> args.warmup_ratio
        0.05
        ```
        """

        return super().set_lr_scheduler(
            name=name, num_epochs=num_epochs, max_steps=max_steps, warmup_ratio=warmup_ratio, warmup_steps=warmup_steps
        )

    def set_dataloader(
        self,
        train_batch_size: int = 8,
        eval_batch_size: int = 8,
        drop_last: bool = False,
        num_workers: int = 0,
        ignore_data_skip: bool = False,
        sampler_seed: Optional[int] = None,
        **kwargs,
    ):
        """
        A method that regroups all arguments linked to the dataloaders creation.

        Args:
            train_batch_size (`int`, defaults to 8):
                The batch size for training.
            eval_batch_size (`int`, defaults to 8):
                The batch size for evaluting.
            drop_last (`bool`, *optional*, defaults to `False`):
                Whether to drop the last incomplete batch (if the length of the dataset is not divisible by the batch
                size) or not.
            num_workers (`int`, *optional*, defaults to 0):
                Number of subprocesses to use for data loading (PyTorch only). 0 means that the data will be loaded in
                the main process.

            ignore_data_skip (`bool`, *optional*, defaults to `False`):
                When resuming training, Whether to skip the epochs and batches to get the data loading at the
                same stage as in the previous training. If set to `True`, the training will begin faster (as that
                skipping step can take a long time) but will not yield the same results as the interrupted training
                would have.
            sampler_seed (`int`, *optional*):
                Random seed to be used with data samplers. If not set, random generators for data sampling will use the
                same seed as `self.seed`. This can be used to ensure reproducibility of data sampling, independent of
                the model seed.
            kwargs:
                pt:
                    pin_memory (`bool`, *optional*, defaults to `True`):
                        Whether you want to pin memory in data loaders or not. Will default to `True`.
                    persistent_workers (`bool`, *optional*, defaults to `False`):
                        If True, the data loader will not shut down the worker processes after a dataset has been
                        consumed once. This allows to maintain the workers Dataset instances alive. Can potentially
                        speed up training, but will increase RAM usage. Will default to `False`.
                    auto_find_batch_size (`bool`, *optional*, defaults to `False`)
                        Whether to find a batch size that will fit into memory automatically through exponential decay,
                        avoiding CUDA Out-of-Memory errors. Requires accelerate to be installed
                        (`pip install accelerate`)

        Example:

        ```py
        >>> from openmind.trainers.training_args import TrainingArguments

        >>> args = TrainingArguments("working_dir")
        >>> args = args.set_dataloader(train_batch_size=16, eval_batch_size=64)
        >>> args.per_device_train_batch_size
        16
        ```
        """

        return super().set_dataloader(
            train_batch_size=train_batch_size,
            eval_batch_size=eval_batch_size,
            drop_last=drop_last,
            num_workers=num_workers,
            ignore_data_skip=ignore_data_skip,
            sampler_seed=sampler_seed,
            **kwargs,
        )
