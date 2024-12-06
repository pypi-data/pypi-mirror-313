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
from typing_extensions import Self

from duck import time, batch
from duck.ops import Op, Const, Pauli

from .abc import RescalableOp


@final
class OpA(RescalableOp):
    site_op: Const
    factors: time.Factors | None = eqx.field(converter=time.wrap_factors)

    @classmethod
    def new(
        cls,
        op: Const,
        factors: time.FactorsLike | None = None,
    ):
        return cls(
            op.scale(factors[0]) if factors is not None else op,
            Pauli.I.batching(op.batch_shape),
            op,
            factors,
        )

    @jax.named_scope("duck.rescalable.a.enlarge")
    def enlarge(self) -> Self:
        op = Const(batch.eye(self.n_dim, self.op.batch_shape), self.n_sites).kron(
            self.site_op
        )
        if self.factors is not None:
            assert self.n_sites < len(
                self.factors
            ), f"max n_sites {len(self.factors)} reached"
            op = op.scale(self.factors[self.n_sites])
        op += self.op.kron(self.op_env)
        return type(self)(
            op,
            self.op_env,
            self.site_op,
            self.factors,
        )

    def scale_const(self, factor: time.Const) -> Op:
        return type(self)(
            self.op.scale_const(factor),
            self.op_env,
            self.site_op,
            self.factors,
        )

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(
            self.op.batching(extra),
            self.op_env.batching(extra),
            self.site_op.batching(extra),
            self.factors,
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(
            self.op.squeeze(axes),
            self.op_env.squeeze(axes),
            self.site_op.squeeze(axes),
            self.factors,
        )

    def as_dtype(self, dtype: jax.numpy.dtype) -> Self:
        return type(self)(
            self.op.as_dtype(dtype),
            self.op_env.as_dtype(dtype),
            self.site_op.as_dtype(dtype),
            self.factors,
        )

    @jax.named_scope("duck.rescalable.a")
    def __call__(self, t: int | float | jax.Array) -> Op:
        if self.factors is not None:
            factors = tuple(f(t) for f in self.factors)
        else:
            factors = None

        return type(self)(
            self.op(t),
            self.op_env(t),
            self.site_op,
            factors,
        )

    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        op, state = self.op.map_const(fn, state)
        return (
            type(self)(
                op,
                self.op_env,
                self.site_op,
                self.factors,
            ),
            state,
        )

    def boundaryops(self) -> tuple[Op, ...]:
        return ()
