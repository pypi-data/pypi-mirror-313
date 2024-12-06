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
import equinox as eqx
import jax.numpy as jnp
import jax.random as jr

from duck.ops import Op, Sum, Zero
from duck.types import RealScalarLike
from duck.opmap.abc import HEM
from duck.rescalable import OpA, chain
from duck.device.rydberg import Rydberg


class MLPControl(eqx.Module):
    mlp: eqx.nn.MLP

    def __call__(self, t: RealScalarLike):
        t = jnp.asarray(t)
        return self.mlp(t.reshape((1,))).reshape(2, -1)


class MLPRydberg(HEM[None]):
    mlps: tuple[MLPControl, ...]
    strength: float = eqx.field(static=True)
    n_start: int = eqx.field(static=True)
    n_target: int = eqx.field(static=True)

    def __init__(
        self,
        n_start: int,
        n_target: int,
        strength: float = 1.0,
        *,
        key: jax.Array,
        width: int = 2,
        depth: int = 2,
    ):
        self.strength = strength
        self.n_start = n_start
        self.n_target = n_target

        mlps = []
        for n_sites in range(n_start, n_target + 1):
            key, init_key = jr.split(key, 2)
            mlp = eqx.nn.MLP(
                in_size=1,
                out_size=2 * n_sites,
                width_size=width,
                depth=depth,
                key=init_key,
            )
            mlps.append(MLPControl(mlp))
        self.mlps = tuple(mlps)

    def initialize(self, key: jax.Array) -> tuple[None, jax.Array]:
        return None, key

    def map(self, op: Op, state: None) -> tuple[Op, None]:
        if not isinstance(op, Sum):
            return op, state
        return Sum(tuple(self._map_each(op) for op in op.ops)), None

    def __getitem__(self, site: int):
        assert self.n_start <= site <= self.n_target, f"site={site} is out of range"
        return self.mlps[site - self.n_start]

    def _map_each(self, op: Op):
        if isinstance(op, chain.OpAB):
            ctrl = self[op.n_sites]
            return chain.OpAB(
                Rydberg.chain(ctrl, op.n_sites, 1.0, dtype=op.dtype),
                op.op_env,
                op.conn,
                op.site_op_a,
                op.site_op_b,
                op.factors,
            )
        elif isinstance(op, OpA):
            return OpA(
                Zero(op.shape, op.n_sites, op.dtype),
                op.op_env,
                op.site_op,
                op.factors,
            )
        else:
            raise ValueError(f"Unexpected operator: {op}")
