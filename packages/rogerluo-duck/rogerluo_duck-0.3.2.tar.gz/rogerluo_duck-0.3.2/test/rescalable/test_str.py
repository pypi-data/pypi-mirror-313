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

from duck.ops import Pauli, State
from duck.rescalable import OpStr


def test_op_str():
    op1 = OpStr.new(Pauli.X)
    op2 = op1.enlarge()
    target = Pauli.X.kron(Pauli.X)
    assert op2.shape == target.shape
    assert jnp.allclose(op2.as_array(), target.as_array())

    op3 = op2.enlarge()
    target = Pauli.X.kron(Pauli.X).kron(Pauli.X)
    assert op3.shape == target.shape
    assert jnp.allclose(op3.as_array(), target.as_array())

    state = OpStr.new(State.O)
    state3 = state.enlarge_to(3)
    assert jnp.allclose(
        state3.as_array(), State.O.kron(State.O).kron(State.O).as_array()
    )
    assert state3.shape == (8, 8)
