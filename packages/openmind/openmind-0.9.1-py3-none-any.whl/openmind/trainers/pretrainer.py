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

import dataclasses
import importlib
import importlib.util
import os
import time

from accelerate import Accelerator, init_empty_weights


try:
    import torch
except ImportError as e:
    raise ImportError("Please install torch package before using this PreTrainer.") from e
import torch.utils.data
from transformers import AutoConfig, AutoModelForCausalLM

from .pretrainer_utils import print_in_last_rank, print_in_main_process
from .pretraining_args import PreTrainingArguments


class _PreTrainerCommon:
    def __init__(
        self,
        pretrain_args: PreTrainingArguments,
        accelerator: Accelerator = None,
        model: torch.nn.Module = None,
        optimizer=None,
        lr_scheduler=None,
        train_dataloader: torch.utils.data.DataLoader = None,
        eval_dataloader: torch.utils.data.DataLoader = None,
        *args,
        **kwargs,
    ):
        self.model = model
        self.pretrain_args = pretrain_args
        self.train_dataloader = train_dataloader
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.accelerator = accelerator
        self.eval_dataloader = eval_dataloader
        self.completed_steps = 0

        self._post_init()

    def train(self):
        self._pre_training()

        batch_loss_sum = 0
        start_time = time.time()

        while self.completed_steps < self.pretrain_args.num_training_steps:
            for batch in self.train_dataloader:
                outputs = self._train_step(batch)
                loss_ = outputs.loss.detach().float()
                batch_loss_sum += loss_.item()
                if self.accelerator.sync_gradients:
                    self.completed_steps += 1
                else:
                    continue  # for accelerator's gradient_accumulation

                lr = self._get_lr()
                batch_loss_avg = self._get_batch_loss_avg(batch_loss_sum=batch_loss_sum)
                elapsed_time = (time.time() - start_time) * 1000  # ms
                self._train_step_log(step=self.completed_steps, loss=batch_loss_avg, lr=lr, elapsed_time=elapsed_time)
                batch_loss_sum = 0

                if (
                    self.pretrain_args.save_interval
                    and self.completed_steps % self.pretrain_args.save_interval == 0
                    and self.pretrain_args.save_dir
                ):
                    self._save_state(save_dir=self.pretrain_args.save_dir)

                if (
                    self.pretrain_args.eval_interval
                    and self.completed_steps % self.pretrain_args.eval_interval == 0
                    and self.eval_dataloader is not None
                ):
                    self._eval(eval_dataloader=self.eval_dataloader, completed_steps=self.completed_steps)

                start_time = time.time()

                if self.completed_steps >= self.pretrain_args.num_training_steps:
                    break

        self.accelerator.end_training()
        self.accelerator.wait_for_everyone()

        self._post_training()

    def _post_init(self):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _init_trackers(self):
        experiment_config = {}
        experiment_config.update(dataclasses.asdict(self.pretrain_args))
        self.accelerator.init_trackers(self.pretrain_args.project_name, experiment_config)

    def _get_gradient_accumulation_steps(self):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _get_batch_loss_avg(self, batch_loss_sum):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _get_lr(self):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _train_step(self, batch):
        self.model.train()
        with self.accelerator.accumulate(self.model):
            outputs = self.model(**batch)
            loss = outputs.loss
            self.accelerator.backward(loss)
            self.optimizer.step()
            self.lr_scheduler.step()
            self.optimizer.zero_grad()
        return outputs

    def _train_step_log(self, loss, lr, elapsed_time, step):
        log_str = (
            f"step: {step} | elapsed time per iteration (ms): {elapsed_time:.1f} | learning rate: {lr:.3E} | "
            f"lm loss: {loss:.6E}"
        )
        print_in_last_rank(log_str)
        # tracker
        self.accelerator.log(
            {
                "train_loss": loss,
                "learning_rate": lr,
            },
            step=step,
        )

    def _print_training_info(self):
        print_in_main_process("***** Running training *****")
        print_in_main_process(
            f"  Num examples = {self.pretrain_args.num_training_steps * self.pretrain_args.batch_size}"
        )
        print_in_main_process(f"  Instantaneous batch size per device = {self.pretrain_args.micro_batch_size}")
        print_in_main_process(
            f"  Total train batch size (w. parallel, distributed & accumulation) = {self.pretrain_args.batch_size}"
        )
        print_in_main_process(f"  Gradient Accumulation steps = {self._get_gradient_accumulation_steps()}")
        print_in_main_process(f"  Total steps = {self.pretrain_args.num_training_steps}")

    def _pre_training(self):
        self._print_training_info()
        print_in_main_process(f"[before the start of training step] datetime: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.completed_steps = 0

    def _post_training(self):
        print_in_main_process(f"[after training is done] datetime: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self._save(save_dir=self.pretrain_args.save_dir)

    def _get_eval_loss(self, loss):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _eval(self, eval_dataloader, completed_steps=None):
        if completed_steps is not None:
            self.completed_steps = completed_steps

        losses = []
        for _, batch in enumerate(eval_dataloader):
            outputs = self._eval_step(batch)
            loss = outputs.loss
            losses.append(self._get_eval_loss(loss))

        self._eval_log(losses=losses)

    def _eval_step(self, batch):
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**batch)
        return outputs

    def _handle_eval_losses(self, losses):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _eval_log(self, losses):
        losses = self._handle_eval_losses(losses)
        eval_loss = torch.mean(losses)
        print_in_last_rank(f"validation at step: {self.completed_steps} | eval_loss: {eval_loss}")
        self.accelerator.log(
            {
                "eval_loss": eval_loss,
            },
            step=self.completed_steps,
        )

    def _save_state(self, save_dir):
        self.accelerator.save_state(save_dir)

    def _save(self, save_dir):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _read_model(self):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _prepare(self):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")

    def _make_accelerator(self):
        raise NotImplementedError("_PreTrainerCommon : Not implemented!")


class _PreTrainerMegatron(_PreTrainerCommon):
    def _make_megatron_dataloader(self):
        from accelerate.utils import MegatronLMDummyDataLoader

        data_path = self.pretrain_args.data_path
        megatron_dataloader_config = {
            "data_path": data_path if isinstance(data_path, list) else [data_path],
            "seq_length": self.pretrain_args.seq_length,
            "micro_batch_size": self.pretrain_args.micro_batch_size,
            "eval_interval": self.pretrain_args.eval_interval,
        }
        if self.pretrain_args.dataloader_config:
            for key, value in self.pretrain_args.dataloader_config.items():
                if key in megatron_dataloader_config.keys():
                    print_in_main_process(
                        f"PreTrainerMegatron dataloader overriding arguments for "
                        f"{key}:{megatron_dataloader_config[key]} with {key}:{value}"
                    )
                megatron_dataloader_config[key] = value
        megatron_dataloader = MegatronLMDummyDataLoader(**megatron_dataloader_config)
        self.train_dataloader = megatron_dataloader
        self.accelerator.state.megatron_lm_plugin.megatron_dataset_flag = True

    def _get_megatron_lm_plugin(self):
        from accelerate.utils import MegatronLMPlugin

        plugin_args = {
            "train_iters": self.pretrain_args.num_training_steps,
            "seq_length": self.pretrain_args.seq_length,
            "num_micro_batches": self.pretrain_args.gradient_accumulation_steps,
            "megatron_dataset_flag": self.pretrain_args.megatron_dataset_flag,
            "eval_interval": self.pretrain_args.eval_interval,
        }
        if self.pretrain_args.plugin_args:
            for key, value in self.pretrain_args.plugin_args.items():
                if key in plugin_args.keys():
                    msg = (
                        f"WARNING: PreTrainerMegatron plugin overriding arguments for "
                        f"{key}:{plugin_args[key]} with {key}:{value}"
                    )
                    print_in_main_process(msg)
                plugin_args[key] = value

        return MegatronLMPlugin(**plugin_args)

    def _make_accelerator(self):
        accelerate_kwargs = {
            "log_with": self.pretrain_args.report_to,
            "project_dir": self.pretrain_args.save_dir,
            "mixed_precision": self.pretrain_args.get_mixed_precision(),
        }
        megatron_lm_plugin = self._get_megatron_lm_plugin()
        accelerate_kwargs["megatron_lm_plugin"] = megatron_lm_plugin
        self.accelerator = Accelerator(**accelerate_kwargs)

    def _post_init(self):
        if importlib.util.find_spec("megatron") is None or importlib.util.find_spec("megatron.data") is None:
            raise EnvironmentError("You must use '--no-use-pep517' to pip install nvidia's megatron from source.")
        if importlib.util.find_spec("openmind_accelerate") is None:
            raise EnvironmentError("You must pip install openmind_accelerate.")
        import openmind_accelerate  # noqa:F401

        if self.accelerator is None:
            self._make_accelerator()

        if self.accelerator.gradient_accumulation_steps != 1:
            raise ValueError(
                "When using Megatron, gradient accumulation is done in Megatron, "
                "so gradient_accumulation_steps in Accelerator needs to be set to 1."
            )

        if self.train_dataloader is None:
            if not self.pretrain_args.data_path:
                raise ValueError("`PreTrainer` requires either a `train_dataloader` or `args.data_path` argument")
            self._make_megatron_dataloader()

        self.accelerator.state.megatron_lm_plugin.megatron_lm_default_args["train_iters"] = (
            self.pretrain_args.num_training_steps
        )

        if self.model is None:
            if not self.pretrain_args.openmind_model_path:
                raise ValueError("`PreTrainer` requires either a `model` or `args.openmind_model_path` argument")
            self._read_model()

        self._prepare()
        self._init_trackers()

    def _pre_training(self):
        from megatron import get_args

        super()._pre_training()
        args = get_args()
        self.model.iteration = args.iteration
        self.completed_steps = args.iteration

    def _eval(self, eval_dataloader, completed_steps=None):
        from megatron import get_args

        if completed_steps is not None:
            self.completed_steps = completed_steps

        args = get_args()
        losses = []
        iteration = 0
        for _, batch in enumerate(eval_dataloader):
            outputs = self._eval_step(batch)
            loss = outputs.loss
            losses.append(self._get_eval_loss(loss))
            iteration += 1
            if iteration >= args.eval_iters:
                break
        self._eval_log(losses=losses)

    def _get_gradient_accumulation_steps(self):
        return self.accelerator.state.megatron_lm_plugin.num_micro_batches

    def _get_batch_loss_avg(self, batch_loss_sum):
        return batch_loss_sum

    def _get_lr(self):
        return self.lr_scheduler.get_lr()

    def _get_eval_loss(self, loss):
        return loss

    def _handle_eval_losses(self, losses):
        return torch.tensor(losses)

    def _save(self, save_dir):
        self.accelerator.save_state(save_dir)

    def _read_model(self):
        model_config = AutoConfig.from_pretrained(self.pretrain_args.openmind_model_path)
        with init_empty_weights():
            self.model = AutoModelForCausalLM.from_config(model_config)
        self.model.config.use_cache = False

    def _prepare(self):
        from accelerate.utils import MegatronLMOptimizerWrapper, MegatronLMSchedulerWrapper

        self.model, self.train_dataloader, self.eval_dataloader = self.accelerator.prepare(
            self.model, self.train_dataloader, self.train_dataloader
        )
        self.optimizer = MegatronLMOptimizerWrapper(self.model.optimizer)
        self.lr_scheduler = MegatronLMSchedulerWrapper(self.model.scheduler, self.model.optimizer)


class _PreTrainerOther(_PreTrainerCommon):
    def _make_accelerator(self):
        accelerate_kwargs = {
            "log_with": self.pretrain_args.report_to,
            "project_dir": self.pretrain_args.save_dir,
            "mixed_precision": self.pretrain_args.get_mixed_precision(),
        }
        self.accelerator = Accelerator(**accelerate_kwargs)

    def _post_init(self):
        if self.accelerator is None:
            self._make_accelerator()

        if self.train_dataloader is None:
            raise ValueError("When not using Megatron, `PreTrainer` requires `train_dataloader`")
        if self.optimizer is None:
            raise ValueError("When not using Megatron, `PreTrainer` requires `optimizer`")
        if self.lr_scheduler is None:
            raise ValueError("When not using Megatron, `PreTrainer` requires `lr_scheduler`")

        if self.model is None:
            if not self.pretrain_args.openmind_model_path:
                raise ValueError("`PreTrainer` requires either a `model` or `args.openmind_model_path` argument")
            self._read_model()

        self._prepare()
        self._init_trackers()

    def _get_gradient_accumulation_steps(self):
        return self.accelerator.gradient_accumulation_steps

    def _get_batch_loss_avg(self, batch_loss_sum):
        return batch_loss_sum / self._get_gradient_accumulation_steps()

    def _get_lr(self):
        return self.lr_scheduler.get_last_lr()[0]

    def _get_eval_loss(self, loss):
        return self.accelerator.gather_for_metrics(loss.repeat(self.pretrain_args.batch_size))

    def _handle_eval_losses(self, losses):
        return torch.cat(losses)

    def _save(self, save_dir):
        unwrapped_model = self.accelerator.unwrap_model(self.model)
        unwrapped_model.save_pretrained(
            save_dir, is_main_process=self.accelerator.is_main_process, save_function=self.accelerator.save
        )

    def _read_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            self.pretrain_args.openmind_model_path,
            torch_dtype=self.pretrain_args.get_torch_dtype(),
        )
        self.model.gradient_checkpointing_enable()
        self.model.config.use_cache = False

    def _prepare(self):
        if self.eval_dataloader:
            (
                self.model,
                self.train_dataloader,
                self.eval_dataloader,
                self.optimizer,
                self.lr_scheduler,
            ) = self.accelerator.prepare(
                self.model, self.train_dataloader, self.eval_dataloader, self.optimizer, self.lr_scheduler
            )
        else:
            self.model, self.train_dataloader, self.optimizer, self.lr_scheduler = self.accelerator.prepare(
                self.model, self.train_dataloader, self.optimizer, self.lr_scheduler
            )


class PreTrainer(_PreTrainerCommon):
    def __new__(cls, *args, **kwargs):
        if os.environ.get("ACCELERATE_USE_MEGATRON_LM", "false") == "true":
            return _PreTrainerMegatron(*args, **kwargs)
        return _PreTrainerOther(*args, **kwargs)
