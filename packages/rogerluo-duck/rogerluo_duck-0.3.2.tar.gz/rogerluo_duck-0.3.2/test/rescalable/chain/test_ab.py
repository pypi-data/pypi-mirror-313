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

import pytest
import jax.numpy as jnp

from duck.ops import Pauli
from duck.rescalable import chain


def test_op_ab():
    op1 = chain.OpAB.new(Pauli.X, Pauli.Y)
    op2 = op1.enlarge()
    target = Pauli.X.kron(Pauli.Y)
    assert jnp.allclose(op2.as_array(), target.as_array())
    assert jnp.allclose(op2.batching(3).as_array(), target.batching(3).as_array())

    op3 = op2.enlarge()
    target = Pauli.X.kron(Pauli.Y).kron(Pauli.I) + Pauli.I.kron(Pauli.X).kron(Pauli.Y)
    assert jnp.allclose(op3.as_array(), target.as_array())
    assert jnp.allclose(op3.batching(3).as_array(), target.batching(3).as_array())


def test_ab_scale():
    op1 = chain.OpAB.new(Pauli.X, Pauli.Y, factors=(1.2, -2.0))
    op2 = op1.enlarge()
    target = 1.2 * Pauli.X.kron(Pauli.Y)
    assert jnp.allclose(op2.as_array(), target.as_array())
    assert jnp.allclose(op2.batching(3).as_array(), target.batching(3).as_array())

    op3 = op2.enlarge()
    target = 1.2 * Pauli.X.kron(Pauli.Y).kron(Pauli.I) - 2.0 * Pauli.I.kron(
        Pauli.X
    ).kron(Pauli.Y)
    assert jnp.allclose(op3.as_array(), target.as_array())
    assert jnp.allclose(op3.batching(3).as_array(), target.batching(3).as_array())

    with pytest.raises(AssertionError):
        op3.enlarge()
