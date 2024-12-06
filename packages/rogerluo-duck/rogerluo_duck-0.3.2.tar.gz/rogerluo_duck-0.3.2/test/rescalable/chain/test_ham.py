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

from duck.ops import const
from duck.rescalable import OpA, chain


def test_tfim():
    h = chain.tfim(3)
    target = (
        chain.OpAB.new(const.Pauli.Z, const.Pauli.Z) + OpA.new(const.Pauli.X)
    ).enlarge_to(3)

    assert h.n_sites == target.n_sites
    assert h.shape == target.shape
    assert h.dtype == target.dtype
    assert h.n_dim == target.n_dim
    assert jnp.allclose(h.as_array(), target.as_array())


def test_heisenberg():
    h = chain.heisenberg(3)
    target = (
        chain.OpAB.new(const.Spin.X, const.Spin.X)
        + chain.OpAB.new(const.Spin.Y, const.Spin.Y)
        + chain.OpAB.new(const.Spin.Z, const.Spin.Z)
    ).enlarge_to(3)

    assert h.n_sites == target.n_sites
    assert h.shape == target.shape
    assert h.dtype == target.dtype
    assert h.n_dim == target.n_dim
    assert jnp.allclose(h.as_array(), target.as_array())

    h = chain.heisenberg(3, (1.0, 2.0, 3.0))
    target = (
        chain.OpAB.new(const.Spin.X, const.Spin.X)
        + chain.OpAB.new(const.Spin.Y, const.Spin.Y)
        + chain.OpAB.new(const.Spin.Z, const.Spin.Z)
        + OpA.new(const.Spin.Z, (1.0, 2.0, 3.0))
    ).enlarge_to(3)

    assert h.n_sites == target.n_sites
    assert h.shape == target.shape
    assert h.dtype == target.dtype
    assert h.n_dim == target.n_dim
    assert jnp.allclose(h.as_array(), target.as_array())
