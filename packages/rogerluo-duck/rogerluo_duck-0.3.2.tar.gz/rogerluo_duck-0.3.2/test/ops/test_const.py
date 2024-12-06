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

from duck import time, batch
from duck.ops.const import Const, Pauli


class TestConst:
    op = Pauli.X.batching(3)
    aa = op.kron(op)

    def test_init(self):
        assert self.op.shape == (3, 2, 2)
        assert self.op.n_dim == 2
        assert self.op.n_batch == 3
        assert self.op.n_sites == 1
        assert self.op.as_array().shape == (3, 2, 2)
        assert jnp.allclose(self.op.as_array()[0], jnp.asarray([[0, 1], [1, 0]]))

        with pytest.raises(AssertionError):
            Const(jnp.zeros((1, 2, 3)), 1)

        with pytest.raises(AssertionError):
            Const(jnp.zeros((1, 2, 2)), -2)

        assert self.op(0.0) is self.op
        assert jnp.allclose(
            self.op.scale_const(time.Const(2.0)).as_array(), 2.0 * self.op.as_array()
        )
        assert jnp.allclose((2.0 * self.op).as_array(), 2.0 * self.op.as_array())

    def test_kron(self):
        assert isinstance(self.aa, Const)
        assert jnp.allclose(
            self.aa.as_array(), batch.kron(self.op.as_array(), self.op.as_array())
        )
        assert self.aa.n_sites == 2

        assert self.aa.shape == (3, 4, 4)
        op2 = self.op.kron(Const(jnp.eye(2), 1).batching(3))
        assert isinstance(op2, Const)

    def test_map_const(self):
        def identity(X: Const, state):
            return Const(batch.eye(2, 3), X.n_sites), state

        op2_, state = self.aa.map_const(identity, None)
        assert op2_.shape == (3, 2, 2)
        assert jnp.allclose(op2_.as_array(), jnp.eye(2))

        def wrong_sites(X: Const, state):
            return Const(batch.eye(2, 3), 1), state

        with pytest.raises(AssertionError):
            self.aa.map_const(wrong_sites, None)

        def wrong_batch(X: Const, state):
            return Const(jnp.eye(2), X.n_sites), state

        with pytest.raises(AssertionError):
            self.aa.map_const(wrong_batch, None)
