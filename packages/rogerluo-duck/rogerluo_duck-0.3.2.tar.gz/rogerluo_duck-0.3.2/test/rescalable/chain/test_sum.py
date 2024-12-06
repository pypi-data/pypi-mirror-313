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

import jax.numpy as jnp

from duck.ops import Pauli
from duck.rescalable import OpA, chain


def test_op_sum():
    op1 = chain.OpAB.new(Pauli.X, Pauli.Y) + OpA.new(Pauli.Z)
    op2 = op1.enlarge()
    target = Pauli.X.kron(Pauli.Y) + Pauli.Z.kron(Pauli.I) + Pauli.I.kron(Pauli.Z)
    assert op2.shape == target.shape
    assert jnp.allclose(op2.as_array(), target.as_array())
    assert jnp.allclose(op2.batching(3).as_array(), target.batching(3).as_array())
    assert op2.shape == target.shape

    op3 = op2.enlarge()
    target = (
        Pauli.X.kron(Pauli.Y).kron(Pauli.I)
        + Pauli.I.kron(Pauli.X).kron(Pauli.Y)
        + Pauli.Z.kron(Pauli.I).kron(Pauli.I)
        + Pauli.I.kron(Pauli.Z).kron(Pauli.I)
        + Pauli.I.kron(Pauli.I).kron(Pauli.Z)
    )
    assert op3.shape == target.shape
    assert jnp.allclose(op3.as_array(), target.as_array())
    assert jnp.allclose(op3.batching(3).as_array(), target.batching(3).as_array())
