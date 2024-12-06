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
import jax.random as jr

from duck import batch
from duck.ops import Const, Pauli, State
from duck.ros import RelevantOpSet
from duck.rescalable import OpStr, SiteOp, chain
from duck.opmap.omm.mps import MPS


def test_mps_init():
    mps = MPS(jr.PRNGKey(0), 2, (3, 5, 7), batch_shape=(2, 3))
    for i, bond in enumerate((3, 5, 7)):
        assert jnp.allclose(
            batch.mm(
                mps.isometries[i].conj().transpose((0, 1, -1, -2)), mps.isometries[i]
            ),
            batch.eye(bond, (2, 3)),
            atol=1e-5,
        )


def test_mps_call():
    key = jr.PRNGKey(0)
    mps = MPS(key, 2, (3, 6, 8), dtype=jnp.float32)
    op = Const(jnp.eye(4), 2)
    assert jnp.allclose(mps.map(op, None)[0].as_array(), jnp.eye(3), atol=1e-5)
    op = Const(jnp.eye(6), 3)
    assert jnp.allclose(mps.map(op, None)[0].as_array(), jnp.eye(6), atol=1e-5)
    op = Const(jnp.eye(12), 4)
    assert jnp.allclose(mps.map(op, None)[0].as_array(), jnp.eye(8), atol=1e-5)
    with pytest.raises(AssertionError):
        mps.map(Const(jnp.eye(16), 4), None)


def test_omm_mps():
    key = jr.PRNGKey(0)
    mps = MPS(key, 2, (3, 6, 8), dtype=jnp.float32)
    ros = RelevantOpSet.new(
        chain.tfim(1), OpStr.new(State.O), SiteOp.new({0: Pauli.Z, 1: Pauli.Z})
    )
    ros = ros.enlarge_to(2)
    ros_, _ = mps(ros, None)
    assert ros_.ham.n_dim == 3
    assert ros_.ham.batch_shape == ()
    assert ros_.ham.n_sites == 2
    ros3 = ros_.enlarge()
    assert ros3.ham.n_dim == 6
    assert ros3.ham.batch_shape == ()
    assert ros3.ham.n_sites == 3
    ros3_, _ = mps(ros3, None)
    assert ros3_.ham.n_dim == 6
    assert ros3_.ham.batch_shape == ()
    assert ros3_.ham.n_sites == 3
    ros4 = ros3_.enlarge()
    assert ros4.ham.n_dim == 12
    assert ros4.ham.batch_shape == ()
    assert ros4.ham.n_sites == 4
    ros4_, _ = mps(ros4, None)
    assert ros4_.ham.n_dim == 8
    assert ros4_.ham.batch_shape == ()
    assert ros4_.ham.n_sites == 4
    ros5 = ros4_.enlarge()
    assert ros5.ham.n_dim == 16
    assert ros5.ham.batch_shape == ()
    assert ros5.ham.n_sites == 5
    with pytest.raises(AssertionError):
        mps(ros5, None)
