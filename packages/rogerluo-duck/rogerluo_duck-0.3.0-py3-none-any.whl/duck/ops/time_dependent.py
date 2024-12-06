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
from jax.typing import DTypeLike
from typing_extensions import Self

from duck import time
from duck.types import RealScalarLike

from .abc import Op


@final
class TimeDependent(Op):
    factor: time.Dependent
    op: Op

    def __init__(
        self, factor: time.Dependent | Callable[[RealScalarLike], jax.Array], op: Op
    ):
        if isinstance(factor, time.Dependent):
            self.factor = factor
        else:
            self.factor = time.Dependent(factor)
        self.op = op

    def as_array(self) -> jax.Array:
        raise ValueError("cannot convert time-dependent operator to array")

    def as_dtype(self, dtype: DTypeLike) -> Self:
        return type(self)(self.factor, self.op.as_dtype(dtype))

    def __call__(self, t: RealScalarLike):
        return self.op(t).scale_const(self.factor(t))

    def scale_const(self, factor: time.Const) -> Op:
        return TimeDependent(self.factor, self.op.scale_const(factor))

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(self.factor, self.op.batching(extra))

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(self.factor, self.op.squeeze(axes))

    def kron(self, other: Op) -> Op:
        return TimeDependent(self.factor, self.op.kron(other))

    def dagger(self) -> Op:
        return TimeDependent(self.factor.conj(), self.op.dagger())

    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        op, state = self.op.map_const(fn, state)
        return TimeDependent(self.factor, op), state

    @property
    def n_sites(self) -> int:
        return self.op.n_sites

    @property
    def dtype(self) -> DTypeLike:
        return self.op.dtype

    @property
    def shape(self):
        return self.op.shape

    @property
    def batch_shape(self) -> tuple[int, ...]:
        return self.op.batch_shape
