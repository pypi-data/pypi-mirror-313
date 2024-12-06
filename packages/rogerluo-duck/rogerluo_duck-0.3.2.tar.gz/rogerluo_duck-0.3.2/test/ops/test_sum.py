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

from duck import time
from duck.ops.sum import Sum
from duck.ops.const import Const, Pauli
from duck.ops.place import Place
from duck.ops.time_dependent import TimeDependent


def test_sum():
    result = Pauli.X + Pauli.X
    assert isinstance(result, Const)
    assert jnp.allclose(result.as_array(), Pauli.X.as_array() + Pauli.X.as_array())
    op = Place.from_pairs({1: Pauli.X, 3: Pauli.Y})
    result = op + Place.from_pairs({1: Pauli.X}, n_sites=4)
    assert result.n_sites == 4
    assert jnp.allclose(
        result.as_array(),
        op.as_array() + Place.from_pairs({1: Pauli.X}, n_sites=4).as_array(),
    )

    op = TimeDependent(time.Dependent(lambda t: jnp.sin(t)), Pauli.X)
    result = op + Pauli.Y
    assert isinstance(result, Sum)
    assert jnp.allclose(result(2.0).as_array(), op(2.0).as_array() + Pauli.Y.as_array())

    result2 = result + result
    assert isinstance(result2, Sum)
    assert len(result2.ops) == 4
    assert jnp.allclose(result2(2.0).as_array(), 2 * result(2.0).as_array())
