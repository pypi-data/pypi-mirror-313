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
import jax.random as jr

from duck.ops import Pauli
from duck.opmap import hem
from duck.rescalable import chain
from duck.device.rydberg import Rydberg


def test_mlp_map():
    mlp = hem.MLPRydberg(2, 4, key=jr.PRNGKey(0), width=2, depth=2)
    h2, _ = mlp.map(chain.tfim(2), None)
    h3 = h2.enlarge()

    target = (
        Rydberg.chain(mlp.mlps[0], 2, 1.0).kron(Pauli.I)
        + Pauli.I.kron(Pauli.Z.kron(Pauli.Z))
        + Pauli.I.kron(Pauli.I.kron(Pauli.X))
    )
    assert jnp.allclose(h3(1.2).as_array(), target(1.2).as_array())
