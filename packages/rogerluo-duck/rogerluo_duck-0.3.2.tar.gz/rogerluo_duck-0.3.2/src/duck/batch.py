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
import jax.numpy as jnp


def dagger(X: jax.Array) -> jax.Array:
    """Performs conjugate transpose on a batch of input matrices.

    Args:

        X(jax.Array[..., m, n]): input matrices.

    Returns:

        out(jax.Array[..., n, m]): output matrices.
    """
    return jnp.matrix_transpose(X.conj())


def combine_batch(X: jax.Array, n_dims: int) -> tuple[tuple[int, ...], jax.Array]:
    if n_dims == 0:
        return X.shape, X.reshape(-1)
    return X.shape[:-n_dims], X.reshape((-1,) + X.shape[-n_dims:])


@jax.named_scope("batch.mm")
def mm(A: jax.Array, B: jax.Array) -> jax.Array:
    assert (
        A.shape[-1] == B.shape[-2]
    ), f"expect last dim of A and 2nd last dim of B to match, got {A.shape} and {B.shape}"
    assert A.ndim == B.ndim, f"expect same ndim, got {A.ndim} and {B.ndim}"
    A_batch, A_ = combine_batch(A, 2)
    B_batch, B_ = combine_batch(B, 2)
    assert A_batch == B_batch, f"expect same batch shape, got {A.shape} and {B.shape}"
    # reshape A to (n_batch, m, n), B to (n_batch, n, p)
    ret = A_ @ B_
    # reshape back to (..., m, p)
    return ret.reshape(A_batch + ret.shape[-2:])


@jax.named_scope("batch.mv")
def mv(A: jax.Array, v: jax.Array) -> jax.Array:
    assert (
        A.shape[-1] == v.shape[-1]
    ), f"expect same last dimension, got {A.shape} and {v.shape}"
    A_batch, A_ = combine_batch(A, 2)
    v_batch, v_ = combine_batch(v, 1)
    assert A_batch == v_batch, f"expect same batch shape, got {A.shape} and {v.shape}"
    ret = jax.vmap(jnp.dot)(A_, v_)
    return ret.reshape(A_batch + ret.shape[-1:])


@jax.named_scope("batch.kron")
def kron(A: jax.Array, B: jax.Array) -> jax.Array:
    A_batch, A_ = combine_batch(A, 2)
    B_batch, B_ = combine_batch(B, 2)
    assert A_batch == B_batch, f"expect same batch shape, got {A.shape} and {B.shape}"
    ret = jax.vmap(jnp.kron)(A_, B_)
    return ret.reshape(A_batch + ret.shape[-2:])


@jax.named_scope("batch.trace")
def trace(A: jax.Array) -> jax.Array:
    batch, A_ = combine_batch(A, 2)
    return jax.vmap(jnp.trace)(A_).reshape(batch)


@jax.named_scope("batch.repeat_const")
def repeat_const(a: jax.Array, extra: int | tuple[int, ...]) -> jax.Array:
    if isinstance(extra, int):
        batch = (extra,)
    else:
        batch = extra
    return jnp.broadcast_to(a, batch + a.shape)


@jax.named_scope("batch.eye")
def eye(n: int, extra: int | tuple[int, ...]) -> jax.Array:
    return repeat_const(jnp.eye(n), extra)


@jax.named_scope("batch.ad")
def ad(A: jax.Array, B: jax.Array, sign: jax.Array) -> jax.Array:
    """adjoint of A with respect to B

    $$
    ad_{A,c}(B) = AB + c BA
    $$

    Args:
        A(jax.Array[..., n, n]): operator A
        B(jax.Array[..., n, n]): operator B
        sign(jax.Array[...]): sign of the second term

    Returns:
        jax.Array[n_batch, n, n]: ad_A(B)
    """
    assert A.shape == B.shape, f"expect same shape, got {A.shape} and {B.shape}"
    assert A.shape[-2] == A.shape[-1], f"expect square matrix, got {A.shape}"
    batch, A_ = combine_batch(A, 2)
    _, B_ = combine_batch(B, 2)
    sign_batch, sign_ = combine_batch(sign, 0)
    assert (
        sign_batch == batch
    ), f"expect same batch shape, got {batch} (A, B) and {sign_batch} (sign)"
    ret = A_ @ B_ + sign_[:, None, None] * B_ @ A_
    return ret.reshape(batch + ret.shape[-2:])
    # NOTE: or sign is not a batched array?
    # return A @ B + sign[None, None, None] * B @ A


@jax.named_scope("batch.comm")
def comm(A: jax.Array, B: jax.Array) -> jax.Array:
    assert A.shape == B.shape, f"expect same shape, got {A.shape} and {B.shape}"
    return mm(A, B) - mm(B, A)


@jax.named_scope("batch.acomm")
def acomm(A: jax.Array, B: jax.Array) -> jax.Array:
    assert A.shape == B.shape, f"expect same shape, got {A.shape} and {B.shape}"
    return mm(A, B) + mm(B, A)


@jax.named_scope("batch.tobc")
def tobc(
    rho0: jax.Array, Bt: tuple[jax.Array, ...], obs_t: jax.Array
) -> tuple[jax.Array, ...]:
    """time-ordered boundary correlation

    Args:
        rho0(jax.Array[..., dim, dim]): initial density matrix
        Bt(tuple[jax.Array[n_samples, ..., dim, dim], order]): boundary operators at each order, length is the order.
        obs_t(jax.Array[..., dim, dim]): observable at different times

    Returns:
        tuple[jax.Array[...], order]: time-ordered boundary correlation

    !!! note
        0-th order returns empty tuple, the return does not contain the 0-th order.
    """
    assert (
        rho0.shape == obs_t.shape
    ), f"expect same shape, got {rho0.shape} and {obs_t.shape}"
    if not Bt:  # 0th order
        return ()

    for B in Bt:
        assert (
            B.shape[1:] == obs_t.shape
        ), f"expect same shape, got {B.shape} and {obs_t.shape}"
    assert len(Bt) <= 3, "only support up to 3rd order"

    # 1st:
    # ad{B1,c1}(A)
    # B1 A + c1 A B1
    if len(Bt) == 1:
        return _tobc_1(rho0, Bt, obs_t)
    # 2nd:
    # ad{B2,c2}ad_{B1,c1}(A)
    # B2(B1 A + c1 A B1) + c2(B1 A + c1 A B1)B2
    if len(Bt) == 2:
        return _tobc_12(rho0, Bt, obs_t)
    # 3rd:
    # ad{B3,c3}ad{B2,c2}ad_{B1,c1}(A)
    # B3(B2(B1 A + c1 A B1) + c2(B1 A + c1 A B1)B2)
    # + c3(B2(B1 A + c1 A B1) + c2(B1 A + c1 A B1)B2)B3
    if len(Bt) == 3:
        return _tobc_123(rho0, Bt, obs_t)
    raise ValueError(f"unsupported order {len(Bt)}")


def expect(rho0: jax.Array, X: jax.Array):
    # merge extra dims of X
    X_batch, X_ = combine_batch(X, rho0.ndim)
    ret = jax.vmap(lambda x: trace(mm(rho0, x)))(X_).real
    return ret.reshape(X.shape[:-2])


def _tobc_1(rho0: jax.Array, Bt: tuple[jax.Array, ...], obs_t: jax.Array):
    B1 = Bt[0]
    B1_A = jax.vmap(lambda B: mm(B, obs_t))(B1)
    A_B1 = jax.vmap(lambda B: mm(obs_t, B))(B1)
    ad1p = B1_A + A_B1
    ad1m = B1_A - A_B1
    return (
        expect(rho0, ad1p),
        expect(rho0, ad1m),
    )


def _tobc_12(rho0: jax.Array, Bt: tuple[jax.Array, ...], obs_t: jax.Array):
    B1, B2 = Bt
    B1_A = jax.vmap(lambda B: mm(B, obs_t))(B1)
    A_B1 = jax.vmap(lambda B: mm(obs_t, B))(B1)
    ad1p = B1_A + A_B1
    ad1m = B1_A - A_B1
    ad2pp = mm(B2, ad1p) + mm(ad1p, B2)
    ad2pm = mm(B2, ad1p) - mm(ad1p, B2)
    ad2mp = mm(B2, ad1m) + mm(ad1m, B2)
    ad2mm = mm(B2, ad1m) - mm(ad1m, B2)

    return (
        expect(rho0, ad1p),
        expect(rho0, ad1m),
        expect(rho0, ad2pp),
        expect(rho0, ad2pm),
        expect(rho0, ad2mp),
        expect(rho0, ad2mm),
    )


def _tobc_123(rho0: jax.Array, Bt: tuple[jax.Array, ...], obs_t: jax.Array):
    B1, B2, B3 = Bt
    B1_A = jax.vmap(lambda B: mm(B, obs_t))(B1)
    A_B1 = jax.vmap(lambda B: mm(obs_t, B))(B1)
    ad1p = B1_A + A_B1
    ad1m = B1_A - A_B1
    ad2pp = mm(B2, ad1p) + mm(ad1p, B2)
    ad2pm = mm(B2, ad1p) - mm(ad1p, B2)
    ad2mp = mm(B2, ad1m) + mm(ad1m, B2)
    ad2mm = mm(B2, ad1m) - mm(ad1m, B2)
    ad3ppp = mm(B3, ad2pp) + mm(ad2pp, B3)
    ad3ppm = mm(B3, ad2pp) - mm(ad2pp, B3)
    ad3pmp = mm(B3, ad2pm) + mm(ad2pm, B3)
    ad3pmm = mm(B3, ad2pm) - mm(ad2pm, B3)
    ad3mpp = mm(B3, ad2mp) + mm(ad2mp, B3)
    ad3mpm = mm(B3, ad2mp) - mm(ad2mp, B3)
    ad3mmm = mm(B3, ad2mm) + mm(ad2mm, B3)
    ad3mmp = mm(B3, ad2mm) - mm(ad2mm, B3)

    return (
        expect(rho0, ad1p),
        expect(rho0, ad1m),
        expect(rho0, ad2pp),
        expect(rho0, ad2pm),
        expect(rho0, ad2mp),
        expect(rho0, ad2mm),
        expect(rho0, ad3ppp),
        expect(rho0, ad3ppm),
        expect(rho0, ad3pmp),
        expect(rho0, ad3pmm),
        expect(rho0, ad3mpp),
        expect(rho0, ad3mpm),
        expect(rho0, ad3mmm),
        expect(rho0, ad3mmp),
    )
