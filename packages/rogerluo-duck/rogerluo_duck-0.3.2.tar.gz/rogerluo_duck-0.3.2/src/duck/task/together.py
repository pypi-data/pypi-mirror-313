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
from tqdm import tqdm

from duck.loss import GradLoss
from duck.task.abc import Config, TaskABC, TrainState


@dataclass
class TrainTogether[State, Cfg: Config](TaskABC[State, Cfg]):
    """train all scales together.

    This training task trains by summing the loss over all scales
    and optimize them together.
    """

    def train_loop(
        self,
        logger: logging.Logger,
        grad_loss: GradLoss,
        train_state: TrainState[State],
    ) -> None:
        for epoch in tqdm(range(self.config.n_epochs), desc="Epochs"):
            train_state.epoch = epoch
            self.train_step(logger, grad_loss, train_state)
            self.info(logger, train_state)

    def train_step(
        self,
        logger: logging.Logger,
        grad_loss: GradLoss,
        train_state: TrainState[State],
    ) -> None:
        train_state.main_key, sample_key = jr.split(train_state.main_key, 2)
        (train_state.loss, train_state.opmap_state), grads = grad_loss(
            train_state.opmap,
            train_state.opmap_state,
            self.config.grow.target,
            sample_key,
        )
        updates, train_state.opt_state = self.optimizer.update(
            grads, train_state.opt_state
        )
        train_state.opmap = eqx.apply_updates(train_state.opmap, updates)
