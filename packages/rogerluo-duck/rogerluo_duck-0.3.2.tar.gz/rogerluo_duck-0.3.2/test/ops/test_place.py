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

from duck import batch
from duck.ops.const import Const, Pauli
from duck.ops.place import Place


def test_place():
    op = Place.from_pairs({1: Pauli.X, 3: Pauli.Y, 5: Pauli.Z})
    target = (
        Pauli.I.kron(Pauli.X)
        .kron(Pauli.I)
        .kron(Pauli.Y)
        .kron(Pauli.I)
        .kron(Pauli.Z)
        .as_array()
    )
    assert jnp.allclose(op.as_array(), target)
    assert op.n_sites == 6
    assert op.n_dim == 2**6
    assert op.shape == target.shape
    assert op(1.0) is op
    assert jnp.allclose((1.2 * op).as_array(), 1.2 * target)
    assert jnp.allclose(op.kron(op).as_array(), batch.kron(target, target))

    mapped, state = op.map(lambda x, state: (Const(batch.eye(2, ()), 1), state), None)
    assert isinstance(mapped, Const)

    with pytest.raises(AssertionError):
        op.map(lambda x, state: (Const(batch.eye(2, 1), 1), state), None)
