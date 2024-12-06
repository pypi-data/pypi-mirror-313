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

import warnings

import diffrax
import jax.numpy as jnp

from duck import batch
from duck.ops import Pauli
from duck.rescalable import chain
from duck.solve.realtime import op_t


def test_op_t():
    ham = chain.tfim(3).as_dtype(jnp.complex64)
    obs = (
        chain.OpAB.new(Pauli.Z, Pauli.Z)
        .enlarge_to(3)
        .as_const()
        .as_dtype(jnp.complex64)
    )
    obs_t = op_t(ham, obs, 0.0, 0.2, 1e-4, ts=(0.1, 0.15, 0.2))

    h = ham.as_array()
    obs0 = obs.as_array()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        sol = diffrax.diffeqsolve(
            diffrax.ODETerm(lambda t, y, args: 1.0j * batch.comm(h, y)),
            diffrax.Tsit5(),
            t0=0.0,
            t1=0.2,
            dt0=1e-4,
            y0=obs0,
            saveat=diffrax.SaveAt(ts=(0.1, 0.15, 0.2)),
        )

    assert sol.ys is not None
    assert jnp.allclose(sol.ys, obs_t.as_array())
