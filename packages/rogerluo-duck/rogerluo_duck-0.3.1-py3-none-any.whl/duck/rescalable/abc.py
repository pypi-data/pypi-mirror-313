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

from abc import abstractmethod

import jax
from typing_extensions import Self

from duck import batch
from duck.ops.abc import Op
from duck.ops.const import Const


class RescalableOp(Op):
    op: Op
    op_env: Op

    def as_array(self) -> jax.Array:
        return self.op.as_array()

    def as_const(self) -> Const:
        return self.op.as_const()

    @property
    def n_sites(self):
        return self.op.n_sites

    @property
    def dtype(self):
        return self.op.dtype

    @property
    def shape(self):
        return self.op.shape

    @property
    def n_dim(self):
        return self.op.n_dim

    @property
    def n_batch(self) -> int:
        return self.op.n_batch

    @property
    def batch_shape(self) -> tuple[int, ...]:
        return self.op.batch_shape

    @abstractmethod
    def enlarge(self) -> Self: ...

    @abstractmethod
    def boundaryops(self) -> tuple[Op, ...]: ...

    @jax.named_scope("duck.rescalable.a.kron")
    def kron(self, other: Op) -> Op:
        return Const(
            batch.kron(self.as_array(), other.as_array()), self.n_sites + other.n_sites
        )

    def dagger(self) -> Op:
        raise NotImplementedError

    # forward other methods to self.op
    def unwrap(self):
        return self.op
