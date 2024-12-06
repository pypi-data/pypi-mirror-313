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

from duck.ops.const import Pauli
from duck.rescalable.a import OpA


def test_op_a():
    op1 = OpA.new(Pauli.X).batching(3)
    op2 = op1.enlarge()
    target = Pauli.X.kron(Pauli.I) + Pauli.I.kron(Pauli.X)
    assert jnp.allclose(op2.as_array(), target.batching(3).as_array())
    op3 = op2.enlarge()
    target = (
        Pauli.X.kron(Pauli.I).kron(Pauli.I)
        + Pauli.I.kron(Pauli.X).kron(Pauli.I)
        + Pauli.I.kron(Pauli.I).kron(Pauli.X)
    )
    assert jnp.allclose(op3.as_array(), target.batching(3).as_array())


def test_a_scale():
    op1 = OpA.new(Pauli.Z, factors=(1.2, -2.0, 3.0))
    assert jnp.allclose(op1.as_array(), 1.2 * Pauli.Z.as_array())
    assert jnp.allclose(
        op1.batching(3).as_array(), 1.2 * Pauli.Z.batching(3).as_array()
    )

    op2 = op1.enlarge()
    target = 1.2 * Pauli.Z.kron(Pauli.I) - 2.0 * Pauli.I.kron(Pauli.Z)
    assert op2.shape == target.shape
    assert jnp.allclose(op2.as_array(), target.as_array())

    op3 = op2.enlarge()
    target = (
        1.2 * Pauli.Z.kron(Pauli.I).kron(Pauli.I)
        - 2.0 * Pauli.I.kron(Pauli.Z).kron(Pauli.I)
        + 3.0 * Pauli.I.kron(Pauli.I).kron(Pauli.Z)
    )
    assert op3.shape == target.shape
    assert jnp.allclose(op3.as_array(), target.as_array())

    with pytest.raises(AssertionError):
        op3.enlarge()
