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

from jax.numpy import dtype
from typing_extensions import Self

from duck import time, types
from duck.ops import Op
from duck.rescalable.abc import RescalableOp


@final
class OpStr(RescalableOp):

    @classmethod
    def new(
        cls,
        site_op: Op,
    ):
        return cls(
            site_op,
            site_op,
        )

    def as_dtype(self, dtype: dtype) -> Self:
        return type(self)(
            self.op.as_dtype(dtype),
            self.op_env.as_dtype(dtype),
        )

    def __call__(self, t: types.RealScalarLike) -> Op:
        return type(self)(
            self.op(t),
            self.op_env(t),
        )

    def enlarge(self) -> Self:
        return type(self)(
            self.op.kron(self.op_env),
            self.op_env,
        )

    def scale_const(self, factor: time.Const) -> Op:
        return type(self)(
            self.op.scale_const(factor),
            self.op_env,
        )

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(
            self.op.batching(extra),
            self.op_env.batching(extra),
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(
            self.op.squeeze(axes),
            self.op_env.squeeze(axes),
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
            ),
            state,
        )

    def boundaryops(self) -> tuple[Op, ...]:
        return ()
