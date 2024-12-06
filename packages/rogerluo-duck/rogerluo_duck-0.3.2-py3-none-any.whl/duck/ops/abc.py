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

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Sequence

import jax
import equinox as eqx
from jax.typing import DTypeLike
from typing_extensions import Self

from duck import time, batch
from duck.types import ScalarLike, RealScalarLike

if TYPE_CHECKING:
    from .const import Const


class Op(eqx.Module, ABC):

    @abstractmethod
    def __call__(self, t: RealScalarLike) -> "Op": ...

    def scale(self, factor: time.FactorLike) -> "Op":
        from .time_dependent import TimeDependent

        if isinstance(factor, time.Dependent):
            return TimeDependent(factor, self)
        elif isinstance(factor, time.Const):
            return self.scale_const(factor)
        elif callable(factor):
            return TimeDependent(factor, self)
        return self.scale_const(time.Const(factor))

    @abstractmethod
    def batching(self, extra: int | tuple[int, ...]) -> Self: ...

    @abstractmethod
    def scale_const(self, factor: time.Const) -> "Op": ...

    @abstractmethod
    def kron(self, other: "Op") -> "Op": ...

    @abstractmethod
    def dagger(self) -> "Op": ...

    def comm(self, other: "Op") -> "Const":
        from .const import Const

        assert (
            self.n_sites == other.n_sites
        ), f"expect same n_sites, got {self.n_sites} and {other.n_sites}"
        return Const(batch.comm(self.as_array(), other.as_array()), self.n_sites)

    def acomm(self, other: "Op") -> "Const":
        from .const import Const

        assert (
            self.n_sites == other.n_sites
        ), f"expect same n_sites, got {self.n_sites} and {other.n_sites}"
        return Const(batch.acomm(self.as_array(), other.as_array()), self.n_sites)

    def mm(self, other: "Op") -> "Op":
        from .const import Const

        return Const(batch.mm(self.as_array(), other.as_array()), self.n_sites)

    def mv(self, other: jax.Array) -> jax.Array:
        return batch.mv(self.as_array(), other)

    def trace(self) -> jax.Array:
        return batch.trace(self.as_array())

    def __mul__(self, other: ScalarLike) -> "Op":
        return self.scale_const(time.Const(other))

    def __rmul__(self, other: ScalarLike) -> "Op":
        return self.scale_const(time.Const(other))

    def __sub__(self, other: "Op") -> "Op":
        return self + other * -1

    def __add__(self, other: "Op") -> "Op":
        from .sum import Sum
        from .zero import Zero
        from .const import Const
        from .place import Place
        from .time_dependent import TimeDependent

        match (self, other):
            case (Zero(), _):
                return other
            case (_, Zero()):
                return self
            case (TimeDependent(), _) | (_, TimeDependent()):
                return Sum((self, other))
            case (Place(), _):
                return self.as_const() + other
            case (_, Place()):
                return self + other.as_const()
            case (Sum(), Sum()):
                return Sum(self.ops + other.ops)
            case (Sum(), _):
                return Sum(self.ops + (other,))
            case (_, Sum()):
                return Sum((self, *other.ops))
            case (Const(), Const()):
                return Const(self.as_array() + other.as_array(), self.n_sites)
            case _:
                return Sum((self, other))

    @abstractmethod
    def as_array(self) -> jax.Array:
        """matrix representation of the operator object."""
        ...

    @abstractmethod
    def as_dtype(self, dtype: DTypeLike) -> Self:
        """convert the operator to the given data type."""
        ...

    def as_const(self) -> "Const":
        """convert the operator to a constant operator."""
        from .const import Const

        return Const(self.as_array(), self.n_sites)

    def eye(self):
        """identity operator."""
        from .const import Const

        return Const(batch.eye(self.n_dim, self.batch_shape), self.n_sites)

    @property
    def dtype(self) -> DTypeLike:
        """data type of the operator object."""
        return self.as_array().dtype

    @property
    def shape(self) -> tuple[int, ...]:
        """shape of the operator object."""
        return self.as_array().shape

    @property
    def batch_shape(self) -> tuple[int, ...]:
        """shape of the batch dimension."""
        return self.shape[:-2]

    @property
    def n_batch(self) -> int:
        """size of the batch dimension."""
        return math.prod(self.batch_shape)

    @property
    def n_dim(self) -> int:
        """size of the space."""
        return self.shape[-1]

    @property
    @abstractmethod
    def n_sites(self) -> int:
        """number of sites of the current object."""
        ...

    @abstractmethod
    def map_const[
        State
    ](
        self,
        fn: Callable[["Op", State], tuple["Op", State]],
        state: State,
    ) -> tuple[
        "Op", State
    ]: ...

    def map[
        State
    ](self, fn: Callable[["Op", State], tuple["Op", State]], state: State) -> tuple[
        "Op", State
    ]:
        """apply an operator matrix map to the operator."""
        out, state = fn(self, state)
        assert out.batch_shape == self.batch_shape, "batch size must not change"
        return out, state

    # NOTE: rescalable interface, optional but
    #       required for RescalableOp
    def enlarge(self) -> Self:
        raise NotImplementedError

    def boundaryops(self) -> tuple["Op", ...]:
        """the set of boundary operators, ignore identity."""
        raise NotImplementedError

    def enlarge_to(self, n_sites: int):
        """enlarge the operator to the given number of sites."""
        op = self
        while op.n_sites < n_sites:
            op = op.enlarge()
        return op

    def enlarge_by(self, n_sites: int):
        """enlarge the operator by the given number of sites."""
        return self.enlarge_to(self.n_sites + n_sites)

    def unwrap(self) -> "Op":
        """unwrap the rescalable operator to the normal operator."""
        return self

    @abstractmethod
    def squeeze(self, axes: int | Sequence[int] | None = None) -> Self: ...
