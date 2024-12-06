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
from functools import reduce

import jax
from jax.typing import DTypeLike
from typing_extensions import Self

from duck import time
from duck.types import RealScalarLike
from duck.ops.zero import Zero

from .abc import Op


@final
class Sum(Op):
    ops: tuple[Op, ...]

    def as_array(self) -> jax.Array:
        return reduce(lambda x, y: x + y, (op.as_array() for op in self.ops))

    def as_dtype(self, dtype: DTypeLike) -> Self:
        return type(self)(tuple(op.as_dtype(dtype) for op in self.ops))

    def __call__(self, t: RealScalarLike) -> Self:
        return type(self)(tuple(op(t) for op in self.ops))

    def __add__(self, other: Op) -> Op:
        if isinstance(other, Sum):
            return Sum(self.ops + other.ops)
        elif isinstance(other, Zero):
            return self
        return Sum(self.ops + (other,))

    # NOTE: overload this to propagate the function to the children
    def scale(self, factor: time.Factor) -> Op:
        return Sum(tuple(op.scale(factor) for op in self.ops))

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(tuple(op.batching(extra) for op in self.ops))

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(tuple(op.squeeze(axes) for op in self.ops))

    def scale_const(self, factor: time.Const) -> Op:
        return Sum(tuple(op.scale_const(factor) for op in self.ops))

    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        result = []
        for op in self.ops:
            op, state = op.map_const(fn, state)
            result.append(op)
        return type(self)(tuple(result)), state

    def kron(self, other: Op) -> Op:
        return Sum(tuple(op.kron(other) for op in self.ops))

    def dagger(self) -> Op:
        return Sum(tuple(op.dagger() for op in self.ops))

    def enlarge(self) -> Self:
        return type(self)(tuple(op.enlarge() for op in self.ops))

    def unwrap(self) -> Op:
        return Sum(tuple(op.unwrap() for op in self.ops))

    def boundaryops(self) -> tuple[Op, ...]:
        return reduce(lambda x, y: x + y, (op.boundaryops() for op in self.ops))

    @property
    def dtype(self) -> DTypeLike:
        """data type of the operator object."""
        return self.ops[0].dtype

    @property
    def shape(self) -> tuple[int, ...]:
        """shape of the operator object."""
        return self.ops[0].shape

    @property
    def n_sites(self) -> int:
        """number of sites of the current object."""
        return self.ops[0].n_sites

    @property
    def batch_shape(self) -> tuple[int, ...]:
        return self.ops[0].batch_shape
