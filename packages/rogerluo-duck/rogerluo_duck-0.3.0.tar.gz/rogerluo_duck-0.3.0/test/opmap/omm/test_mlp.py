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

from duck.ops import Pauli, State
from duck.ros import RelevantOpSet
from duck.opmap.omm import IsometricSharedMLP
from duck.rescalable import OpStr, SiteOp, chain


def test_mlp_basic():
    key = jr.PRNGKey(123)
    init_key, state, key = jr.split(key, 3)
    mlp = IsometricSharedMLP(grow_start=3, grow_step=1, noise_n_dim=3, depth=2, key=key)
    op = Pauli.X.kron(Pauli.X).kron(Pauli.X).as_const()
    out, state = mlp.map(op, state)
    assert jnp.allclose(out.dagger().as_array(), out.as_array())

    ros = RelevantOpSet.new(
        chain.tfim(1), OpStr.new(State.O), SiteOp.new({0: Pauli.Z, 1: Pauli.Z})
    )

    with pytest.raises(AssertionError):
        mlp(ros, state)

    ros = ros.enlarge_to(3)
    ros_, state = mlp(ros, state)
    assert ros_.ham.n_dim == 4
    assert ros_.ham.batch_shape == ()
    assert ros_.ham.n_sites == 3
    ros = ros_.enlarge()
    ros_, state = mlp(ros, state)
    assert ros_.ham.n_dim == 4
    assert ros_.ham.batch_shape == ()
    assert ros_.ham.n_sites == 4
