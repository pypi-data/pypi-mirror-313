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

import jax
import jax.numpy as jnp
import jax.random as jr

from duck.ops import Pauli, State
from duck.ros import RelevantOpSet
from duck.flow import Flow
from duck.opmap import HEM, OMM
from duck.ops.abc import Op
from duck.rescalable import OpStr, SiteOp, chain


class IdentityOMM(OMM[None]):

    def initialize(self, key: jax.Array) -> tuple[None, jax.Array]:
        return None, key

    def map(self, op: Op, state: None) -> tuple[Op, None]:
        return op, state


class IdentityHEM(HEM[None]):

    def initialize(self, key: jax.Array) -> tuple[None, jax.Array]:
        return None, key

    def map(self, op: Op, state: None) -> tuple[Op, None]:
        return op, state


def test_tobc_mse():
    ros = RelevantOpSet.new(
        chain.tfim(1), OpStr.new(State.O), SiteOp.new({0: Pauli.Z, 1: Pauli.Z})
    )
    flow, state = Flow.new(IdentityOMM(), None, ros, grow_step=1, grow_target=3)
    key = jr.PRNGKey(0)
    mse = flow.tobc_mse(
        0.0, 0.1, 1e-4, key=key, n_samples=10, order=2, ts=jnp.linspace(0.0, 0.1, 20)
    )
    assert jnp.allclose(mse, 0.0)
    assert state is None

    ros = RelevantOpSet.new(
        chain.tfim(1), OpStr.new(State.O), SiteOp.new({0: Pauli.Z, 1: Pauli.Z})
    ).enlarge_to(2)
    flow, state = Flow.new(IdentityHEM(), None, ros, grow_step=1, grow_target=4)
    mse = flow.tobc_mse(
        0.0,
        0.1,
        1e-4,
        key=jr.PRNGKey(0),
        n_samples=10,
        order=2,
        ts=jnp.linspace(0.0, 0.1, 20),
    )
    assert jnp.allclose(mse, 0.0)
    assert state is None
