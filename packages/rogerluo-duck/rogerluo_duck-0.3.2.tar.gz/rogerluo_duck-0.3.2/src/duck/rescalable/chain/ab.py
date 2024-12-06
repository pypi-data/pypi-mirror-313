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

from typing import Callable, Sequence, final

import jax
import equinox as eqx
import jax.numpy as jnp
from jax.numpy import dtype
from typing_extensions import Self

from duck import time, batch
from duck.ops import Op, Const
from duck.rescalable.abc import RescalableOp


@final
class OpAB(RescalableOp):
    op: Op
    op_env: Op
    conn: Op
    site_op_a: Op
    site_op_b: Op
    factors: time.Factors | None = eqx.field(converter=time.wrap_factors)

    @classmethod
    def new(
        cls,
        op_a: Const,
        op_b: Const,
        factors: time.FactorsLike | None = None,
    ):
        return cls(
            Const(jnp.zeros(op_a.batch_shape + (op_a.n_dim, op_a.n_dim)), 1),
            Const(batch.eye(2, op_a.batch_shape), 1),
            op_a,
            op_a,
            op_b,
            factors,
        )

    def as_dtype(self, dtype: dtype) -> Self:
        return type(self)(
            self.op.as_dtype(dtype),
            self.op_env.as_dtype(dtype),
            self.conn.as_dtype(dtype),
            self.site_op_a.as_dtype(dtype),
            self.site_op_b.as_dtype(dtype),
            self.factors,
        )

    @jax.named_scope("duck.rescalable.chain.ab.OpAB")
    def __call__(self, t: int | float | jax.Array) -> Op:
        if self.factors is not None:
            factors = tuple(f(t) if callable(f) else f for f in self.factors)
        else:
            factors = None

        return type(self)(
            self.op(t),
            self.op_env(t),
            self.conn(t),
            self.site_op_a(t),
            self.site_op_b(t),
            factors,
        )

    def scale_const(self, factor: time.Const) -> Op:
        return type(self)(
            self.op.scale_const(factor),
            self.op_env,
            self.conn,
            self.site_op_a,
            self.site_op_b,
            self.factors,
        )

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(
            self.op.batching(extra),
            self.op_env.batching(extra),
            self.conn.batching(extra),
            self.site_op_a.batching(extra),
            self.site_op_b.batching(extra),
            self.factors,
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(
            self.op.squeeze(axes),
            self.op_env.squeeze(axes),
            self.conn.squeeze(axes),
            self.site_op_a.squeeze(axes),
            self.site_op_b.squeeze(axes),
            self.factors,
        )

    @jax.named_scope("duck.rescalable.chain.ab.OpAB.enlarge")
    def enlarge(self) -> Self:
        op = self.conn.kron(self.site_op_b)
        if self.factors is not None:
            assert self.n_sites - 1 < len(
                self.factors
            ), f"max n_sites {len(self.factors)} reached"
            op = op.scale(self.factors[self.n_sites - 1])
        op += self.op.kron(self.op_env)
        return type(self)(
            op,
            self.op_env,
            Const(batch.eye(self.n_dim, self.op.batch_shape), self.n_sites).kron(
                self.site_op_a
            ),
            self.site_op_a,
            self.site_op_b,
            self.factors,
        )

    @jax.named_scope("duck.rescalable.chain.ab.map")
    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        op, state = self.op.map_const(fn, state)
        conn, state = self.conn.map_const(fn, state)
        return (
            type(self)(
                op,
                self.op_env,
                conn,
                self.site_op_a,
                self.site_op_b,
                self.factors,
            ),
            state,
        )

    def boundaryops(self) -> tuple[Op, ...]:
        return (self.conn,)
