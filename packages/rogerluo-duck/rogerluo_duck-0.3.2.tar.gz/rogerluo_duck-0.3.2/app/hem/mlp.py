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

from dataclasses import dataclass

import tyro
import optax

from duck import OpStr, Pauli, State, SiteOp, RelevantOpSet, task, chain, opmap


@dataclass
class Config(task.Config):
    depth: int = 8
    width_size: int = 4


@dataclass
class Task(task.TrainGradually[None, Config]):

    def __init__(self, config: Config):
        super().__init__(
            config,
            ros=RelevantOpSet.new(
                chain.tfim(1), OpStr.new(State.O), SiteOp.new({0: Pauli.Z, 1: Pauli.Z})
            ),
            optimizer=optax.adam(3e-3),
        )

    def opmap(self) -> opmap.OpMap[None]:
        return opmap.hem.MLPRydberg(
            self.config.grow.start,
            self.config.grow.target,
            key=self.key,
            width=self.config.width_size,
            depth=self.config.depth,
        )


if __name__ == "__main__":
    Task(tyro.cli(Config)).run()
