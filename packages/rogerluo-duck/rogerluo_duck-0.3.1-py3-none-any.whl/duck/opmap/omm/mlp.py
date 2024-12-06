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

from typing import Callable

import jax
import equinox as eqx
import jax.numpy as jnp
import jax.random as jr

from duck import batch
from duck.ops import Const
from duck.ops.abc import Op
from duck.opmap.abc import OMM


class IsometricSharedMLP(OMM[jax.Array]):
    mlp: eqx.nn.MLP
    input_n_dim: int = eqx.field(static=True)
    output_n_dim: int = eqx.field(static=True)
    noise_n_dim: int = eqx.field(static=True)

    def __init__(
        self,
        grow_start: int,
        grow_step: int,
        noise_n_dim: int,
        depth: int,
        activation: Callable = jax.nn.relu,
        *,
        key: jax.Array,
    ):
        self.input_n_dim = 2**grow_start
        self.output_n_dim = 2 ** (grow_start - grow_step)
        self.noise_n_dim = noise_n_dim
        self.mlp = eqx.nn.MLP(
            in_size=self.input_n_dim * self.input_n_dim + noise_n_dim,
            out_size=self.input_n_dim * self.output_n_dim,
            width_size=self.input_n_dim * self.output_n_dim,
            depth=depth,
            activation=activation,
            key=key,
        )

    def initialize(self, key: jax.Array) -> tuple[jax.Array, jax.Array]:
        state, main_key = jr.split(key, 2)
        return state, main_key

    def map(self, op: Op, state: jax.Array) -> tuple[Op, jax.Array]:
        assert (
            self.input_n_dim == op.n_dim
        ), f"expect input_n_dim={self.input_n_dim}, got {op.n_dim}"
        batch_shape = op.batch_shape
        noise_state, state = jr.split(state, 2)
        noise = jr.normal(noise_state, batch_shape + (self.noise_n_dim,))
        input = jnp.concatenate(
            [op.as_array().reshape(batch_shape + (-1,)), noise], axis=-1
        )
        if batch_shape:
            output = jax.vmap(self.mlp)(input).reshape(
                batch_shape + (self.input_n_dim, self.output_n_dim)
            )
        else:
            output = self.mlp(input).reshape((self.input_n_dim, self.output_n_dim))
        proj = jnp.linalg.qr(output)[0]
        out = batch.mm(batch.mm(batch.dagger(proj), op.as_array()), proj)
        return Const(out, op.n_sites), state
