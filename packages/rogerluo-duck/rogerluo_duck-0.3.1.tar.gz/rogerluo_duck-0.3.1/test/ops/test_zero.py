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

import jax
import pytest
import jax.numpy as jnp

from duck.ops import Zero, Pauli


def test_basic():
    x = Zero((2, 2), 1)
    assert jnp.allclose(x.as_array(), jnp.zeros((2, 2), dtype=jnp.float32))
    x = Zero((4, 4), 2)
    assert jnp.allclose(x.as_array(), jnp.zeros((4, 4), dtype=jnp.float32))
    assert x.batch_shape == ()
    assert x.shape == (4, 4)
    assert x.as_array().dtype == jax.dtypes.canonicalize_dtype(jnp.float_)
    assert x.n_dim == 4
    assert x.n_sites == 2
    assert x.as_dtype(jnp.complex64).as_array().dtype == jnp.complex64
    assert x(1.0) is x
    assert x.dagger() is x

    def map_fn(op, state):
        return op, state

    new_x, state = x.map_const(map_fn, 1)
    assert state == 1
    assert new_x is x

    with pytest.raises(AssertionError):
        Zero((2, 3), 1)

    with pytest.raises(AssertionError):
        Zero((2,), 1)

    with pytest.raises(AssertionError):
        Zero((2, 2), 0)


def test_linalg():
    x = Zero((2, 2), 1)
    assert jnp.allclose(
        x.kron(Pauli.X).as_array(), jnp.kron(jnp.zeros((2, 2)), Pauli.X.as_array())
    )
    assert jnp.allclose(x.comm(Pauli.X).as_array(), x.as_array())
    assert jnp.allclose(x.acomm(Pauli.X).as_array(), x.as_array())
    assert jnp.allclose(
        x.mm(Pauli.X).as_array(), jnp.matmul(x.as_array(), Pauli.X.as_array())
    )
    assert jnp.allclose(x.mv(Pauli.X.as_array()), jnp.zeros((2, 2)))
    assert jnp.allclose(x.trace(), jnp.asarray(0.0))
    assert jnp.allclose((x + Pauli.X).as_array(), Pauli.X.as_array())
    assert jnp.allclose((x - Pauli.X).as_array(), -Pauli.X.as_array())


def test_batching():
    x = Zero((2, 2), 1)
    new_x = x.batching((3, 4))
    assert new_x.batch_shape == (3, 4)
    assert jnp.allclose(new_x.as_array(), jnp.zeros((3, 4, 2, 2)))
    assert new_x.kron(Pauli.X.batching((3, 4))).shape == (3, 4, 4, 4)


def test_squeeze():
    x = Zero((1, 2, 2), 1)
    squeezed = x.squeeze()
    assert squeezed.shape == (2, 2)
    assert squeezed.batch_shape == ()
