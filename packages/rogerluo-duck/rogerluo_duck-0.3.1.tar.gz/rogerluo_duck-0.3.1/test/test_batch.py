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
import jax.random as jr

from duck import batch

key = jr.PRNGKey(0)


def test_mm():
    A = jr.normal(key, (2, 3, 3))
    B = jr.normal(key, (2, 3, 3))
    C = batch.mm(A, B)
    assert jnp.allclose(C[0], A[0] @ B[0])
    assert jnp.allclose(C[1], A[1] @ B[1])

    A = jr.normal(key, (2, 2, 3, 3))
    B = jr.normal(key, (2, 2, 3, 3))
    C = batch.mm(A, B)
    for i in range(2):
        for j in range(2):
            assert jnp.allclose(C[i, j], A[i, j] @ B[i, j])


def test_mv():
    A = jr.normal(key, (2, 3, 3))
    v = jr.normal(key, (2, 3))
    w = batch.mv(A, v)
    assert jnp.allclose(w[0], A[0] @ v[0])
    assert jnp.allclose(w[1], A[1] @ v[1])

    A = jr.normal(key, (2, 2, 3, 3))
    v = jr.normal(key, (2, 2, 3))
    w = batch.mv(A, v)
    for i in range(2):
        for j in range(2):
            assert jnp.allclose(w[i, j], A[i, j] @ v[i, j])


def test_kron():
    A = jr.normal(key, (2, 3, 3))
    B = jr.normal(key, (2, 3, 3))
    C = batch.kron(A, B)
    assert jnp.allclose(C[0], jnp.kron(A[0], B[0]))
    assert jnp.allclose(C[1], jnp.kron(A[1], B[1]))

    A = jr.normal(key, (2, 2, 3, 3))
    B = jr.normal(key, (2, 2, 3, 3))
    C = batch.kron(A, B)
    for i in range(2):
        for j in range(2):
            assert jnp.allclose(C[i, j], jnp.kron(A[i, j], B[i, j]))


def test_repeat_const():
    a = jr.normal(key, (3,))
    b = batch.repeat_const(a, (2, 3))
    assert jnp.allclose(b[0], a)
    assert jnp.allclose(b[1], a)
    assert jnp.allclose(b[2], a)

    a = jr.normal(key, (3,))
    b = batch.repeat_const(a, 2)
    assert jnp.allclose(b[0], a)
    assert jnp.allclose(b[1], a)


def test_eye():
    a = batch.eye(3, (2, 3))
    assert jnp.allclose(a[0], jnp.eye(3))
    assert jnp.allclose(a[1], jnp.eye(3))


def test_ad():
    A = jr.normal(key, (2, 3, 3))
    B = jr.normal(key, (2, 3, 3))
    sign = jr.choice(key, jnp.asarray([-1, 1]), (2,))
    C = batch.ad(A, B, sign)
    assert jnp.allclose(C[0], A[0] @ B[0] + sign[0] * B[0] @ A[0])
    assert jnp.allclose(C[1], A[1] @ B[1] + sign[1] * B[1] @ A[1])

    A = jr.normal(key, (2, 2, 3, 3))
    B = jr.normal(key, (2, 2, 3, 3))
    sign = jr.choice(key, jnp.asarray([-1, 1]), (2, 2))
    C = batch.ad(A, B, sign)
    for i in range(2):
        for j in range(2):
            assert jnp.allclose(
                C[i, j], A[i, j] @ B[i, j] + sign[i, j] * B[i, j] @ A[i, j]
            )


def test_comm():
    A = jr.normal(key, (2, 3, 3))
    B = jr.normal(key, (2, 3, 3))
    C = batch.comm(A, B)
    assert jnp.allclose(C[0], A[0] @ B[0] - B[0] @ A[0])
    assert jnp.allclose(C[1], A[1] @ B[1] - B[1] @ A[1])

    A = jr.normal(key, (2, 2, 3, 3))
    B = jr.normal(key, (2, 2, 3, 3))
    C = batch.comm(A, B)
    for i in range(2):
        for j in range(2):
            assert jnp.allclose(C[i, j], A[i, j] @ B[i, j] - B[i, j] @ A[i, j])


@pytest.mark.parametrize("batch_shape", [(), (10,), (10, 5)])
def test_tobc(batch_shape):
    # no batch version
    rho0 = jr.normal(key, batch_shape + (2, 2))
    obs_t = jr.normal(key, batch_shape + (2, 2))

    Bt = tuple(jr.normal(key, (10,) + batch_shape + (2, 2)) for _ in range(0))
    results = batch.tobc(rho0, Bt, obs_t)
    assert results == ()

    Bt = tuple(jr.normal(key, (10,) + batch_shape + (2, 2)) for _ in range(1))
    results = batch.tobc(rho0, Bt, obs_t)
    assert len(results) == 2
    BA = jax.vmap(lambda B: batch.mm(B, obs_t))(Bt[0])
    AB = jax.vmap(lambda B: batch.mm(obs_t, B))(Bt[0])
    assert jnp.allclose(results[0], batch.expect(rho0, BA + AB))
    assert jnp.allclose(results[1], batch.expect(rho0, BA - AB))

    Bt = tuple(jr.normal(key, (10,) + batch_shape + (2, 2)) for _ in range(2))
    results = batch.tobc(rho0, Bt, obs_t)
    assert len(results) == 6
    BA = jax.vmap(lambda B: batch.mm(B, obs_t))(Bt[0])
    AB = jax.vmap(lambda B: batch.mm(obs_t, B))(Bt[0])
    p = BA + AB
    m = BA - AB
    pp = batch.mm(Bt[1], p) + batch.mm(p, Bt[1])
    pm = batch.mm(Bt[1], p) - batch.mm(p, Bt[1])
    mp = batch.mm(Bt[1], m) + batch.mm(m, Bt[1])
    mm = batch.mm(Bt[1], m) - batch.mm(m, Bt[1])
    assert jnp.allclose(results[2], batch.expect(rho0, pp))
    assert jnp.allclose(results[3], batch.expect(rho0, pm))
    assert jnp.allclose(results[4], batch.expect(rho0, mp))
    assert jnp.allclose(results[5], batch.expect(rho0, mm))

    Bt = tuple(jr.normal(key, (10,) + batch_shape + (2, 2)) for _ in range(3))
    results = batch.tobc(rho0, Bt, obs_t)
    assert len(results) == 14
    BA = jax.vmap(lambda B: batch.mm(B, obs_t))(Bt[0])
    AB = jax.vmap(lambda B: batch.mm(obs_t, B))(Bt[0])
    p = BA + AB
    m = BA - AB
    pp = batch.mm(Bt[1], p) + batch.mm(p, Bt[1])
    pm = batch.mm(Bt[1], p) - batch.mm(p, Bt[1])
    mp = batch.mm(Bt[1], m) + batch.mm(m, Bt[1])
    mm = batch.mm(Bt[1], m) - batch.mm(m, Bt[1])
    ppp = batch.mm(Bt[2], pp) + batch.mm(pp, Bt[2])
    ppm = batch.mm(Bt[2], pp) - batch.mm(pp, Bt[2])
    pmp = batch.mm(Bt[2], pm) + batch.mm(pm, Bt[2])
    pmm = batch.mm(Bt[2], pm) - batch.mm(pm, Bt[2])
    mpp = batch.mm(Bt[2], mp) + batch.mm(mp, Bt[2])
    mpm = batch.mm(Bt[2], mp) - batch.mm(mp, Bt[2])
    mmp = batch.mm(Bt[2], mm) + batch.mm(mm, Bt[2])
    mmm = batch.mm(Bt[2], mm) - batch.mm(mm, Bt[2])
    assert batch.expect(rho0, ppp).shape == (10,) + batch_shape
    assert jnp.allclose(results[6], batch.expect(rho0, ppp))
    assert jnp.allclose(results[7], batch.expect(rho0, ppm))
    assert jnp.allclose(results[8], batch.expect(rho0, pmp))
    assert jnp.allclose(results[9], batch.expect(rho0, pmm))
    assert jnp.allclose(results[10], batch.expect(rho0, mpp))
    assert jnp.allclose(results[11], batch.expect(rho0, mpm))
    assert jnp.allclose(results[12], batch.expect(rho0, mmp))
    assert jnp.allclose(results[13], batch.expect(rho0, mmm))
