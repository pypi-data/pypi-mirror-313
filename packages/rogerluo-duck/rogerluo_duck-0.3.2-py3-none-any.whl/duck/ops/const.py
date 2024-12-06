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
from jax.typing import DTypeLike
from typing_extensions import Self

from duck import time, batch
from duck.types import RealScalarLike

from .abc import Op


@final
class Const(Op):
    op: jax.Array
    _n_sites: int = eqx.field(static=True)
    # NOTE: this is causing compile error somehow
    # name: str | None = eqx.field(default=None, static=True)

    def __post_init__(self):
        assert self._n_sites >= 1, "n_sites must be at least 1"
        assert (
            self.op.ndim >= 2
        ), f"op should at least have 2 dims (n_dim, n_dim), got {self.op.shape}"
        assert self.op.shape[-1] == self.op.shape[-2], "op must be square"

    def as_array(self) -> jax.Array:
        return self.op

    def as_const(self) -> "Const":
        return self

    def as_dtype(self, dtype: DTypeLike) -> Self:
        return type(self)(self.op.astype(dtype), self.n_sites)

    def __call__(self, t: RealScalarLike) -> Self:
        return self

    def scale_const(self, factor: time.Const) -> Op:
        return Const(self.op * factor.value, self.n_sites)

    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        ret, state = fn(self, state)
        assert (
            ret.n_sites == self.n_sites
        ), f"n_sites must be preserved, got {ret.n_sites} != {self.n_sites}"
        assert (
            ret.batch_shape == self.batch_shape
        ), f"batch_shape must be preserved, got {ret.batch_shape} != {self.batch_shape}"
        return ret, state

    def kron(self, other: Op) -> Op:
        from .sum import Sum
        from .time_dependent import TimeDependent

        if isinstance(other, TimeDependent):
            return TimeDependent(other.factor, self.kron(other.op))
        elif isinstance(other, Sum):
            return Sum(tuple(self.kron(op) for op in other.ops))
        else:
            return Const(
                batch.kron(self.op, other.as_array()), self.n_sites + other.n_sites
            )

    def dagger(self) -> Op:
        return Const(batch.dagger(self.op), self.n_sites)

    @property
    def n_sites(self) -> int:
        return self._n_sites

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        assert self.n_batch == 1, ValueError("cannot create batch on batched operators")

        return type(self)(
            batch.repeat_const(self.op, extra),
            self.n_sites,
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(jnp.squeeze(self.op, axes), self.n_sites)


class Pauli:
    X = Const(jnp.asarray([[0, 1], [1, 0]]), 1)
    Y = Const(jnp.asarray([[0, -1j], [1j, 0]]), 1)
    Z = Const(jnp.asarray([[1, 0], [0, -1]]), 1)
    I = Const(jnp.eye(2), 1)  # noqa: E741
    n = Const(jnp.array([[0, 0], [0, 1]]), 1)


class Spin:
    X = Const(0.5 * Pauli.X.op, 1)
    Y = Const(0.5 * Pauli.Y.op, 1)
    Z = Const(0.5 * Pauli.Z.op, 1)
    p = Const(jnp.asarray([[0, 1], [0, 0]]), 1)


class State:
    O = Const(jnp.asarray([[1, 0], [0, 0]]), 1)  # noqa: E741
