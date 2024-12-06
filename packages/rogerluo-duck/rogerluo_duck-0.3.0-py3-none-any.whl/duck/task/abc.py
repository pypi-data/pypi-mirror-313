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
from abc import ABC, abstractmethod
from typing import ClassVar
from datetime import datetime
from dataclasses import field, dataclass

import jax
import optax
import equinox as eqx
import jax.numpy as jnp
import jax.random as jr

from duck.ros import RelevantOpSet
from duck.flow import Flow
from duck.loss import GradLoss, tobc_mse_loss
from duck.opmap import OpMap
from duck.task.config import Config
from duck.task.logging import TOMLFormatter


@dataclass
class TrainState[State]:
    main_key: jax.Array
    sample_key: jax.Array
    loss: jax.Array
    epoch: int
    target_site: int
    opt_state: optax.OptState
    opmap: OpMap[State]
    opmap_state: State


@dataclass
class TaskABC[State, Cfg: Config](ABC):
    name: ClassVar[str]
    config: Cfg
    ros: RelevantOpSet
    optimizer: optax.GradientTransformation
    key: jax.Array = field(init=False)
    saveat: jax.Array = field(init=False)

    def __post_init__(self):
        self.ros = self.ros.enlarge_to(self.config.grow.start)
        self.key = jr.PRNGKey(self.config.seed)
        self.saveat = jnp.linspace(
            self.config.evolution.t0,
            self.config.evolution.t1,
            self.config.evolution.n_timesteps,
        )

    def logger(self):
        logger = logging.getLogger("train")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(TOMLFormatter())
        logger.addHandler(ch)

        if self.config.logging.file:
            data_dir = self.config.logging.data_dir / self.config.name
            if not data_dir.is_dir():
                data_dir.mkdir(parents=True)
            file = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            fh = logging.FileHandler(data_dir / f"{file}.toml")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(TOMLFormatter())
            logger.addHandler(fh)

        # NOTE: we want to make sure we don't have import errors
        # when self.config.logging.wandb is False and wandb is not installed
        if self.config.logging.wandb:
            import wandb

            from duck.task.logging.wandb import WandbHandler

            run = wandb.init(project=self.config.name, config=self.config.dump())
            logger.addHandler(WandbHandler(run))

        return logger

    def initialize(self) -> TrainState[State]:
        opmap = self.opmap()
        opmap_state, key = opmap.initialize(self.key)
        opt_state = self.optimizer.init(eqx.filter(opmap, eqx.is_inexact_array))
        main_key, sample_key = jax.random.split(key, 2)
        return TrainState(
            main_key=main_key,
            sample_key=sample_key,
            loss=jax.numpy.asarray(0.0),
            epoch=0,
            target_site=self.config.grow.start,
            opt_state=opt_state,
            opmap=opmap,
            opmap_state=opmap_state,
        )

    def run(self):
        logger = self.logger()
        logger.info(
            {
                "__meta__": self.config.dump(),
            }
        )
        train_state = self.initialize()
        grad_loss = tobc_mse_loss(
            self.ros,
            self.config.evolution.t0,
            self.config.evolution.t1,
            self.config.evolution.dt0,
            self.config.grow.step,
            n_samples=self.config.loss.n_samples,
            order=self.config.loss.order,
            ts=self.saveat,
        )
        try:
            self.train_loop(logger, grad_loss, train_state)
        except KeyboardInterrupt:
            logger.info({"err": "Interrupted"})

    def info(
        self,
        logger: logging.Logger,
        train_state: TrainState[State],
    ):
        if train_state.epoch % self.config.logging.every != 0:
            return

        logger.info(
            {
                "epoch": train_state.epoch,
                "loss": train_state.loss,
                "sqrt(loss)": jax.numpy.sqrt(train_state.loss),
                "summary": self.summarize(train_state),
            }
        )

    def summarize(self, train_state: TrainState[State]):
        flow, state_ = Flow.new(
            train_state.opmap,
            train_state.opmap_state,
            self.ros,
            self.config.grow.step,
            train_state.target_site,
        )
        return flow.summarize_tobc_mse(
            self.config.evolution.t0,
            self.config.evolution.t1,
            self.config.evolution.dt0,
            key=train_state.sample_key,
            n_samples=self.config.loss.n_samples,
            order=self.config.loss.order,
            ts=self.saveat,
        )

    @abstractmethod
    def opmap(self) -> OpMap[State]: ...

    @abstractmethod
    def train_step(
        self,
        logger: logging.Logger,
        grad_loss: GradLoss,
        train_state: TrainState[State],
    ) -> None: ...

    @abstractmethod
    def train_loop(
        self,
        logger: logging.Logger,
        grad_loss: GradLoss[State],
        train_state: TrainState[State],
    ) -> None: ...
