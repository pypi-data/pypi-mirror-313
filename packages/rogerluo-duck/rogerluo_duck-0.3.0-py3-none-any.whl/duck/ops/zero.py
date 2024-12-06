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

from duck import time
from duck.types import RealScalarLike

from .abc import Op
from .const import Const


def default_dtype():
    return jax.dtypes.canonicalize_dtype(jax.numpy.float_)


@final
class Zero(Op):
    _shape: tuple[int, ...] = eqx.field(static=True)
    _n_sites: int = eqx.field(static=True)
    _dtype: DTypeLike = eqx.field(default_factory=default_dtype, static=True)

    @property
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @property
    def n_sites(self) -> int:
        return self._n_sites

    @property
    def dtype(self) -> DTypeLike:
        return self._dtype

    def __post_init__(self):
        assert self._n_sites >= 1, "n_sites must be at least 1"
        assert (
            len(self._shape) >= 2
        ), f"op should at least have 2 dims (n_dim, n_dim), got {self._shape}"
        assert self._shape[-1] == self._shape[-2], "op must be square"

    def as_array(self) -> jax.Array:
        return jnp.zeros(self._shape, dtype=self._dtype)

    def as_const(self) -> Const:
        return Const(self.as_array(), self.n_sites)

    def as_dtype(self, dtype: DTypeLike) -> Self:
        return type(self)(self._shape, self.n_sites, dtype)

    def __call__(self, t: RealScalarLike) -> Self:
        return self

    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        return self, state

    def kron(self, other: Op) -> Op:
        # assert batch size
        assert self.batch_shape == other.batch_shape
        n_dim = self.n_dim * other.n_dim
        return type(self)(
            self.batch_shape + (n_dim, n_dim),
            self.n_sites + other.n_sites,
            self.dtype,
        )

    def comm(self, other: Op) -> Const:
        return Const(self.as_array(), self.n_sites)

    def acomm(self, other: Op) -> Const:
        return Const(self.as_array(), self.n_sites)

    def mm(self, other: Op) -> Op:
        return self

    def mv(self, other: jax.Array) -> jax.Array:
        return jnp.zeros_like(other)

    def trace(self) -> jax.Array:
        return jnp.zeros(self.batch_shape)

    def scale(self, factor: time.FactorLike) -> Op:
        return self

    def scale_const(self, factor: time.Const) -> Op:
        return self

    def __add__(self, other: Op) -> Op:
        return other

    def dagger(self) -> Op:
        return self

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        assert self.n_batch == 1, ValueError("cannot create batch on batched operators")
        if isinstance(extra, int):
            extra = (extra,)

        return type(self)(
            self.batch_shape + extra + (self.n_dim, self.n_dim),
            self.n_sites,
            self.dtype,
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        if isinstance(axes, int):
            axes = (axes,)
        elif axes is None:
            axes = tuple(i for i, dim in enumerate(self._shape) if dim == 1)

        return type(self)(
            tuple(
                dim
                for i, dim in enumerate(self._shape)
                if axes is None or i not in axes
            ),
            self.n_sites,
            self.dtype,
        )
