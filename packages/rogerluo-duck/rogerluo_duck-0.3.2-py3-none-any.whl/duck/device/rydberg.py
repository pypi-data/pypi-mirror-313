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
import jax.numpy as jnp
from jax.typing import DTypeLike
from typing_extensions import Self

from duck import ops, time, rescalable
from duck.types import RealScalarLike


@final
class Rydberg(ops.Op):
    control: Callable[[RealScalarLike], jax.Array]
    "control model t -> omega[..., #term],delta[..., #term]"
    interact: ops.Op
    "interaction term, [..., #dim, #dim]"
    rabi: tuple[ops.Op, ...]
    "rabi term, [..., #dim, #dim]"
    detuning: tuple[ops.Op, ...]
    "detuning term, [..., #dim, #dim]"

    @classmethod
    def chain(
        cls,
        control: Callable[[RealScalarLike], jax.Array],
        n: int,
        strength: float,
        dtype: DTypeLike = jnp.float32,
    ) -> Self:
        interact = (
            rescalable.chain.OpAB.new(
                ops.const.Pauli.n.as_dtype(dtype), ops.const.Pauli.n.as_dtype(dtype)
            )
            .enlarge_to(n)
            .as_const()
        )
        rabi = tuple(
            ops.Place.from_pairs({i: ops.const.Pauli.X.as_dtype(dtype)}, n)
            for i in range(n)
        )
        detuning = tuple(
            ops.Place.from_pairs({i: ops.const.Pauli.n.as_dtype(dtype)}, n)
            for i in range(n)
        )
        return cls(
            control,
            strength * interact,
            rabi,
            detuning,
        )

    @property
    def dtype(self):
        return self.interact.dtype

    @property
    def shape(self) -> tuple[int, ...]:
        return self.interact.shape

    @property
    def batch_shape(self) -> tuple[int, ...]:
        return self.interact.batch_shape

    @property
    def n_sites(self) -> int:
        return self.interact.n_sites

    def __call__(self, t: RealScalarLike) -> ops.Op:
        fac = self.control(t)
        omega, delta = fac[0], fac[1]
        ret = self.interact.as_array()
        for omega_, rabi in zip(omega, self.rabi):
            ret += omega_ * rabi.as_array()

        for delta_, detuning in zip(delta, self.detuning):
            ret += delta_ * detuning.as_array()
        return ops.Const(ret, self.n_sites)

    def scale_const(self, factor: time.Const) -> ops.Op:
        return type(self)(
            self.control,
            self.interact.scale_const(factor),
            tuple(op.scale_const(factor) for op in self.rabi),
            tuple(op.scale_const(factor) for op in self.detuning),
        )

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        raise NotImplementedError("batching not implemented for Rydberg")

    def kron(self, other: ops.Op) -> ops.Op:
        return Rydberg(
            self.control,
            self.interact.kron(other),
            tuple(op.kron(other) for op in self.rabi),
            tuple(op.kron(other) for op in self.detuning),
        )

    def dagger(self) -> ops.Op:
        return Rydberg(
            self.control,
            self.interact.dagger(),
            tuple(op.dagger() for op in self.rabi),
            tuple(op.dagger() for op in self.detuning),
        )

    def as_array(self) -> jax.Array:
        raise ValueError("Rydberg operator cannot be represented as an array")

    def as_dtype(self, dtype: jax.numpy.dtype) -> Self:
        return type(self)(
            self.control,
            self.interact.as_dtype(dtype),
            tuple(op.as_dtype(dtype) for op in self.rabi),
            tuple(op.as_dtype(dtype) for op in self.detuning),
        )

    def map_const[
        State
    ](self, fn: Callable[[ops.Op, State], tuple[ops.Op, State]], state: State) -> tuple[
        ops.Op, State
    ]:
        interact, state = self.interact.map_const(fn, state)

        rabi: list[ops.Op] = []
        for op in self.rabi:
            op, state = op.map_const(fn, state)
            rabi.append(op)

        detuning: list[ops.Op] = []
        for op in self.detuning:
            op, state = op.map_const(fn, state)
            detuning.append(op)

        return Rydberg(self.control, interact, tuple(rabi), tuple(detuning)), state

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(
            self.control,
            self.interact.squeeze(axes),
            tuple(op.squeeze(axes) for op in self.rabi),
            tuple(op.squeeze(axes) for op in self.detuning),
        )
