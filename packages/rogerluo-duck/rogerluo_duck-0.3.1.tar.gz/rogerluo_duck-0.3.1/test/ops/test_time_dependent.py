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

from duck import time
from duck.ops import Const, Pauli
from duck.ops.time_dependent import TimeDependent


def test_time_dependent():
    op = TimeDependent(time.Dependent(lambda t: jnp.sin(t)), Pauli.X) + Pauli.Y

    with pytest.raises(ValueError):
        op.as_array()

    assert jnp.allclose(
        op(2.0).as_array(),
        jnp.sin(2.0) * Pauli.X.as_array() + Pauli.Y.as_array(),
    )

    def identity(X: Const, state):
        return Const(jnp.eye(2), X.n_sites), state

    op1, _ = op.map_const(identity, None)

    assert jnp.allclose(
        op1(2.0).as_array(),
        jnp.sin(2.0) * Pauli.I.as_array() + Pauli.I.as_array(),
    )

    op2 = op.kron(op)
    A = TimeDependent(time.Dependent(lambda t: jnp.sin(t)), Pauli.X)
    B = Pauli.Y

    assert jnp.allclose(
        op2(2.0).as_array(),
        (A.kron(A) + A.kron(B) + B.kron(A) + B.kron(B))(2.0).as_array(),
    )
