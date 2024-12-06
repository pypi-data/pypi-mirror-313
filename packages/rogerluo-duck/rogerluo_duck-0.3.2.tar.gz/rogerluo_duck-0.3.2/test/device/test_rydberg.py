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
from duck.solve import realtime
from duck.device.rydberg import Rydberg


def test_chain_rydberg():
    def control(t):
        return jnp.asarray([[1.2, 2.1], [0.1, 0.2]])

    h = Rydberg.chain(control, 2, 1.0)

    assert jnp.allclose(h.interact.as_array(), Pauli.n.kron(Pauli.n).as_array())
    assert jnp.allclose(
        h.rabi[0].as_array(),
        Pauli.X.kron(Pauli.I).as_array(),
    )
    assert jnp.allclose(
        h.rabi[1].as_array(),
        Pauli.I.kron(Pauli.X).as_array(),
    )
    assert jnp.allclose(h.detuning[0].as_array(), Pauli.n.kron(Pauli.I).as_array())
    assert jnp.allclose(h.detuning[1].as_array(), Pauli.I.kron(Pauli.n).as_array())

    assert jnp.allclose(
        h(1.15).as_array(),
        (
            h.interact
            + 1.2 * Pauli.X.kron(Pauli.I)
            + 2.1 * Pauli.I.kron(Pauli.X)
            + 0.1 * Pauli.n.kron(Pauli.I)
            + 0.2 * Pauli.I.kron(Pauli.n)
        ).as_array(),
    )


def test_device_solve():
    def control(t):
        return jnp.asarray([[1.2, 2.1], [0.1, 0.2]])

    h = Rydberg.chain(control, 2, 1.0)
    answer = realtime.op_t(
        h.as_dtype(jnp.complex64),
        Pauli.X.kron(Pauli.I).as_const().as_dtype(jnp.complex64),
        0.0,
        0.1,
        1e-4,
    )

    target = realtime.op_t(
        h(1.0).as_const().as_dtype(jnp.complex64),
        Pauli.X.kron(Pauli.I).as_const().as_dtype(jnp.complex64),
        0.0,
        0.1,
        1e-4,
    )

    assert jnp.allclose(answer.as_array(), target.as_array())
