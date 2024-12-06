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

from typing import Callable, TypeAlias, TypeGuard, final, overload

import jax
import equinox as eqx
import jax.numpy as jnp

from duck.types import ScalarLike, RealScalarLike


@final
class Dependent(eqx.Module):
    fn: Callable[[RealScalarLike], jax.Array]

    def __call__(self, t: RealScalarLike) -> "Const":
        return Const(self.fn(jnp.asarray(t)))

    def conj(self):
        return Dependent(lambda t: self.fn(t).conj())


@final
class Const(eqx.Module):
    value: jax.Array

    def __init__(self, value: ScalarLike):
        self.value = jax.numpy.asarray(value)

    def __call__(self, t: RealScalarLike) -> "Const":
        return self


Factor: TypeAlias = Const | Dependent
FactorLike: TypeAlias = ScalarLike | Callable[[RealScalarLike], jax.Array] | Factor
Factors: TypeAlias = tuple[Const, ...] | tuple[Dependent, ...]
ConstFactorsLike: TypeAlias = tuple[ScalarLike, ...] | tuple[Const, ...]
DependentFactorsLike: TypeAlias = (
    tuple[Callable[[RealScalarLike], jax.Array], ...] | tuple[Dependent, ...]
)
FactorsLike: TypeAlias = ConstFactorsLike | DependentFactorsLike


def is_all(typ_or_types, xs: tuple):
    return all(isinstance(x, typ_or_types) for x in xs)


def is_all_const(factors: tuple) -> TypeGuard[tuple[Const, ...]]:
    return is_all(Const, factors)


def is_all_time_dependent(factors: tuple) -> TypeGuard[tuple[Dependent, ...]]:
    return is_all(Dependent, factors)


def is_all_scalar(factors: tuple) -> TypeGuard[tuple[ScalarLike, ...]]:
    return is_all((int, float, complex, jax.Array), factors)


def is_all_callable(
    factors: tuple,
) -> TypeGuard[tuple[Callable[[RealScalarLike], jax.Array], ...]]:
    return all(callable(f) for f in factors)


@overload
def wrap_factors(factors: ConstFactorsLike) -> tuple[Const, ...]: ...


@overload
def wrap_factors(factors: DependentFactorsLike) -> tuple[Dependent, ...]: ...


@overload
def wrap_factors(factors: None) -> None: ...


def wrap_factors(factors: FactorsLike | None) -> Factors | None:
    if factors is None:
        return None

    if is_all_const(factors) or is_all_time_dependent(factors):
        return factors
    elif is_all_scalar(factors):
        return tuple(Const(f) for f in factors)
    elif is_all_callable(factors):
        return tuple(Dependent(f) for f in factors)
    raise TypeError(f"Invalid factors: {factors}")
