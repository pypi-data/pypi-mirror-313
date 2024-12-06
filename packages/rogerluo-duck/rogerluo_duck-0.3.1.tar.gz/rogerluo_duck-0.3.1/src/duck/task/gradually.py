# Copyright 2024 Xiu-Zhe(Roger) Luo.
# Copyright 2024 duck contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from dataclasses import dataclass

import equinox as eqx
import jax.random as jr
from rich.progress import Progress, TimeElapsedColumn

from duck.loss import GradLoss
from duck.task.abc import Config, TaskABC, TrainState


@dataclass
class TrainGradually[State, Cfg: Config](TaskABC[State, Cfg]):
    """train scales gradually.

    This training task trains by optimizing the loss of

    L_1
    L_1 + L_2
    L_1 + L_2 + L_3
    ...
    L_1 + L_2 + ... + L_N

    where N is the number of scales
    """

    def train_step(
        self,
        logger: logging.Logger,
        grad_loss: GradLoss,
        train_state: TrainState[State],
    ) -> None:
        train_state.main_key, train_state.sample_key = jr.split(train_state.main_key, 2)
        (train_state.loss, train_state.opmap_state), grads = grad_loss(
            train_state.opmap,
            train_state.opmap_state,
            train_state.target_site,
            train_state.sample_key,
        )
        updates, train_state.opt_state = self.optimizer.update(
            grads, train_state.opt_state
        )
        train_state.opmap = eqx.apply_updates(train_state.opmap, updates)

    def train_loop(
        self,
        logger: logging.Logger,
        grad_loss: GradLoss,
        train_state: TrainState[State],
    ) -> None:
        with Progress(*Progress.get_default_columns(), TimeElapsedColumn()) as progress:
            scale_range = range(
                self.config.grow.start,
                self.config.grow.target + 1,
                self.config.grow.step,
            )
            site_task = progress.add_task("[cyan]Scale...", total=len(scale_range))
            training_epoch = progress.add_task(
                "[green]Epoch...", total=self.config.n_epochs
            )
            for epoch_target_site in scale_range:
                train_state.target_site = epoch_target_site
                train_state.opt_state = self.optimizer.init(
                    eqx.filter(train_state.opmap, eqx.is_inexact_array)
                )
                for epoch in range(self.config.n_epochs):
                    train_state.epoch = epoch
                    self.train_step(logger, grad_loss, train_state)
                    self.info(logger, train_state)
                    progress.update(training_epoch, advance=1)

                progress.update(site_task, advance=1)
                progress.reset(training_epoch)
