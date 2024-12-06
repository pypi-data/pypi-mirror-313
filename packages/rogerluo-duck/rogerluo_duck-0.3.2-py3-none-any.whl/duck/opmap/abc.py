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

from abc import ABC, abstractmethod

import jax
import equinox as eqx

from duck.ops import Op
from duck.ros import RelevantOpSet


class OpMap[State](eqx.Module, ABC):

    @abstractmethod
    def initialize(self, key: jax.Array) -> tuple[State, jax.Array]:
        """Initialize the state of the operator map.

        Args:
            key(jax.Array): The random key.

        Returns:
            tuple[State, jax.Array]: The initial state and the updated key.
        """
        ...

    @abstractmethod
    def __call__(
        self, ros: RelevantOpSet, state: State
    ) -> tuple[RelevantOpSet, State]: ...

    @abstractmethod
    def map(self, op: Op, state: State) -> tuple[Op, State]: ...


class OMM[State](OpMap[State]):

    def __call__(self, ros: RelevantOpSet, state: State) -> tuple[RelevantOpSet, State]:
        ham, state = ros.ham.map_const(self.map, state)
        rho, state = ros.rho.map_const(self.map, state)
        obs, state = ros.obs.map_const(self.map, state)
        return RelevantOpSet(ham, rho, obs), state


class HEM[State](OpMap[State]):

    def __call__(self, ros: RelevantOpSet, state: State) -> tuple[RelevantOpSet, State]:
        ham, state = ros.ham.map(self.map, state)
        return RelevantOpSet(ham, ros.rho, ros.obs), state
