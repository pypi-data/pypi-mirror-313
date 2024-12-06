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

from typing import Mapping, Callable, Sequence, final

import jax
import equinox as eqx
from jax.typing import DTypeLike
from typing_extensions import Self

from duck import time, batch
from duck.types import RealScalarLike

from .abc import Op
from .const import Const


@final
class Place(Op):
    "place a few single-site operators at specific sites"
    ops: tuple[Op, ...]
    "operators to place"
    sites: tuple[int, ...] = eqx.field(static=True)
    "site indices to place the operators"
    _n_sites: int = eqx.field(static=True)
    "number of sites of the current object"

    @classmethod
    def from_pairs(cls, pairs: Mapping[int, Op], n_sites: int | None = None):
        ops, sites = tuple(pairs.values()), tuple(pairs.keys())
        return cls(ops, sites, max(sites) + 1 if n_sites is None else n_sites)

    def __post_init__(self):
        for op in self.ops:
            assert op.n_sites == 1, "only single-site operators are allowed"
            assert op.n_dim == 2, "only single-site operators are allowed"

        assert all(
            op.n_batch == self.ops[0].n_batch for op in self.ops[1:]
        ), "all operators must have the same batch size"

    @property
    def n_batch(self) -> int:
        "size of the batch dimension."
        return self.ops[0].n_batch

    @property
    def batch_shape(self) -> tuple[int, ...]:
        return self.ops[0].batch_shape

    @property
    def n_sites(self) -> int:
        "number of sites of the current object."
        return self._n_sites

    @property
    def shape(self) -> tuple[int, ...]:
        "shape of the operator object."
        return self.batch_shape + (self.n_dim, self.n_dim)

    @property
    def n_dim(self) -> int:
        "dimension of the operator object."
        return 2**self.n_sites

    def __call__(self, t: RealScalarLike) -> Self:
        return self

    def scale_const(self, factor: time.Const) -> Op:
        return type(self)(
            (self.ops[0].scale_const(factor), *self.ops[1:]), self.sites, self._n_sites
        )

    def batching(self, extra: int | tuple[int, ...]) -> Self:
        return type(self)(
            tuple(op.batching(extra) for op in self.ops), self.sites, self._n_sites
        )

    def kron(self, other: Op) -> Op:
        from .sum import Sum
        from .time_dependent import TimeDependent

        if isinstance(other, TimeDependent):
            return TimeDependent(other.factor, self.kron(other.op))
        elif isinstance(other, Sum):
            return Sum(tuple(self.kron(op) for op in other.ops))
        else:
            return Const(
                batch.kron(self.as_array(), other.as_array()),
                self.n_sites + other.n_sites,
            )

    def dagger(self) -> Op:
        return type(self)(
            tuple(op.dagger() for op in self.ops), self.sites, self._n_sites
        )

    def map_const[
        State
    ](self, fn: Callable[[Op, State], tuple[Op, State]], state: State) -> tuple[
        Op, State
    ]:
        return self.as_const().map_const(fn, state)

    def as_array(self) -> jax.Array:
        "matrix representation of the operator object."
        ret = batch.kron(
            batch.eye(2 ** self.sites[0], self.batch_shape),
            self.ops[0].as_array(),
        )
        prev = self.sites[0]
        for site, op in zip(self.sites[1:], self.ops[1:]):
            ret = batch.kron(
                ret,
                batch.kron(
                    batch.eye(2 ** (site - prev - 1), self.batch_shape),
                    op.as_array(),
                ),
            )
            prev = site
        ret = batch.kron(
            ret,
            batch.eye(2 ** (self._n_sites - prev - 1), self.batch_shape),
        )
        return ret

    def as_dtype(self, dtype: DTypeLike) -> Self:
        return type(self)(
            tuple(op.as_dtype(dtype) for op in self.ops), self.sites, self._n_sites
        )

    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self:
        return type(self)(
            tuple(op.squeeze(axes) for op in self.ops), self.sites, self._n_sites
        )
