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

from duck import time, batch
from duck.ops import Op, Const
from duck.types import RealScalarLike

from .abc import RescalableOp


@final
class SiteOp(RescalableOp):
    """Rescalable operator with single-site operators acting only on a subset of sites.
    For example, two-point correlators, where the operator acts on two sites.
    """

    sitemap: dict[int, Const]
    eye_op: Const

    @classmethod
    def new(cls, sitemap: dict[int, Const]) -> Self:
        assert all(
            site_op.n_sites == 1 for site_op in sitemap.values()
        ), "site_op must be a single-site operator"
        first_op = next(iter(sitemap.values()))
        assert all(
            first_op.shape == site_op.shape for site_op in sitemap.values()
        ), "all site operators must have the same shape"
        I_2 = Const(batch.eye(2, first_op.batch_shape), 1)
        op = sitemap[0] if 0 in sitemap else I_2
        op_env = sitemap[1] if 1 in sitemap else I_2
        return cls(op, op_env, sitemap, I_2)

    def enlarge(self) -> Self:
        op_env = (
            self.sitemap[self.n_sites + 1]
            if self.n_sites + 1 in self.sitemap
            else self.eye_op
        )
        return type(self)(
            self.op.kron(self.op_env),
            op_env,
            self.sitemap,
            self.eye_op,
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
                self.sitemap,
                self.eye_op,
            ),
            state,
        )

    def boundaryops(self) -> tuple[Op, ...]:
        return ()

    def __call__(self, t: RealScalarLike) -> Op:
        return type(self)(
            self.op(t),
            self.op_env(t),
            self.sitemap,
            self.eye_op,
        )

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(
            self.op.batching(extra),
            self.op_env.batching(extra),
            {site: site_op.batching(extra) for site, site_op in self.sitemap.items()},
            self.eye_op.batching(extra),
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(
            self.op.squeeze(axes),
            self.op_env.squeeze(axes),
            self.sitemap,
            self.eye_op,
        )

    def scale_const(self, factor: time.Const) -> Op:
        return type(self)(
            self.op.scale_const(factor),
            self.op_env,
            self.sitemap,
            self.eye_op,
        )

    def as_dtype(self, dtype: dtype) -> Self:
        return type(self)(
            self.op.as_dtype(dtype),
            self.op_env.as_dtype(dtype),
            {site: site_op.as_dtype(dtype) for site, site_op in self.sitemap.items()},
            self.eye_op.as_dtype(dtype),
        )
