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
from duck.rescalable.site import SiteOp


def test_site_op():
    op = SiteOp.new({1: Pauli.X, 3: Pauli.Y})
    op3 = op.enlarge_to(3)
    assert jnp.allclose(op3.as_array(), Pauli.I.kron(Pauli.X).kron(Pauli.I).as_array())

    op4 = op3.enlarge()
    assert jnp.allclose(
        op4.as_array(), Pauli.I.kron(Pauli.X).kron(Pauli.I).kron(Pauli.Y).as_array()
    )

    op5 = op4.enlarge()
    assert jnp.allclose(
        op5.as_array(),
        Pauli.I.kron(Pauli.X).kron(Pauli.I).kron(Pauli.Y).kron(Pauli.I).as_array(),
    )

    cop = op.as_dtype(jnp.complex64)
    assert cop.op.dtype == jnp.complex64
    assert cop.op_env.dtype == jnp.complex64
    assert all(each.dtype == jnp.complex64 for each in cop.sitemap.values())
