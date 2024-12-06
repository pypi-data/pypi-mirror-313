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

from typing import Sequence

import jax
import equinox as eqx
import jax.numpy as jnp

from duck import batch
from duck.ops import Op, Const
from duck.types import RealScalarLike
from duck.solve.realtime import op_t

# NOTE:
# we don't support multi-observables in a single ROS
# to make things simpler, we can support it in the future
# by building a ROSUnion type on top of ROS, where the union
# share the same ham and rho, but different obs


class RelevantOpSet(eqx.Module):
    ham: Op
    "problem hamiltonian"
    rho: Op
    "initial density matrix"
    obs: Op
    "target observables"

    @classmethod
    def new(
        cls,
        ham: Op,
        rho: Op,
        obs: Op,
        *,
        dtype: jnp.dtype = jnp.float32,
    ):
        dtype = jnp.promote_types(
            jnp.promote_types(
                jnp.promote_types(ham.dtype, rho.dtype),
                obs.dtype,
            ),
            dtype,
        )
        dtype = jnp.promote_types(dtype, jnp.complex64)
        return cls(
            ham.as_dtype(dtype),
            rho.as_dtype(dtype),
            obs.as_dtype(dtype),
        )

    def __post_init__(self):
        assert (
            self.ham.n_sites == self.rho.n_sites
        ), f"all operators must have the same number of sites, got {self.ham.n_sites} and {self.rho.n_sites}"
        assert (
            self.obs.n_sites == self.ham.n_sites
        ), f"all operators must have the same number of sites, got {self.obs.n_sites} and {self.ham.n_sites}"

        assert (
            self.ham.shape == self.rho.shape
        ), f"all operators must have the same shape, got {self.ham.shape} and {self.rho.shape}"
        assert (
            self.obs.shape == self.ham.shape
        ), f"all operators must have the same shape, got {self.obs.shape} and {self.ham.shape}"

        assert (
            self.ham.dtype == self.rho.dtype
        ), f"all operators must have the same dtype, got {self.ham.dtype} and {self.rho.dtype}"
        assert (
            self.obs.dtype == self.ham.dtype
        ), f"all operators must have the same dtype, got {self.obs.dtype} and {self.ham.dtype}"

    def as_dtype(self, dtype: jnp.dtype):
        return type(self)(
            self.ham.as_dtype(dtype),
            self.rho.as_dtype(dtype),
            self.obs.as_dtype(dtype),
        )

    def enlarge(self):
        return type(self)(
            self.ham.enlarge(),
            self.rho.enlarge(),
            self.obs.enlarge(),
        )

    def enlarge_to(self, n_sites: int):
        return type(self)(
            self.ham.enlarge_to(n_sites),
            self.rho.enlarge_to(n_sites),
            self.obs.enlarge_to(n_sites),
        )

    def enlarge_by(self, n_sites: int):
        return type(self)(
            self.ham.enlarge_by(n_sites),
            self.rho.enlarge_by(n_sites),
            self.obs.enlarge_by(n_sites),
        )

    @property
    def n_sites(self):
        return self.ham.n_sites

    @property
    def shape(self):
        return self.ham.shape

    @property
    def batch_shape(self):
        return self.ham.batch_shape

    @property
    def dtype(self):
        return self.ham.dtype

    @property
    def n_dim(self):
        return self.ham.n_dim

    @property
    def n_batch(self):
        return self.ham.n_batch

    def batching(self, extra: int | tuple[int, ...]):
        return type(self)(
            self.ham.batching(extra),
            self.rho.batching(extra),
            self.obs.batching(extra),
        )

    def squeeze(self, axes: int | Sequence[int] | None = None):
        return type(self)(
            self.ham.squeeze(axes),
            self.rho.squeeze(axes),
            self.obs.squeeze(axes),
        )

    def exp_obs_t(
        self, t0: RealScalarLike, t1: RealScalarLike, dt0: RealScalarLike | None = None
    ):
        """compute the expectation value of the observable at time t1

        Args:
            t0(RealScalarLike): initial time.
            t1(RealScalarLike): final time.
            dt0(RealScalarLike): time step.
        """
        exp = batch.expect(self.rho.as_array(), self.obs_t(t0, t1, dt0).as_array()[0])
        if self.batch_shape:
            return exp.mean(axis=0).squeeze()
        return exp

    def obs_t(
        self,
        t0: RealScalarLike,
        t1: RealScalarLike,
        dt0: RealScalarLike | None = None,
        *,
        ts: Sequence[RealScalarLike] | jax.Array | None = None,
    ):
        """Compute the time-evolved observable.

        Args:

            t0(RealScalarLike): initial time.
            t1(RealScalarLike): final time.
            dt0(RealScalarLike): time step.
            ts(Sequence[RealScalarLike] | jax.Array | None): time steps to evaluate the observable.

        Returns:
            operator(Const[timestep, batch, dim, dim]): time-evolved observable at each time step.
        """
        return op_t(self.ham.unwrap(), self.obs.as_const(), t0, t1, dt0, ts=ts)

    def boundary_t(
        self,
        t0: RealScalarLike,
        t1: RealScalarLike,
        dt0: RealScalarLike | None = None,
        *,
        ts: Sequence[RealScalarLike] | jax.Array | None = None,
    ) -> tuple[Const, ...]:
        """Compute the time-evolved boundary operators.

        Args:

            t0(RealScalarLike): initial time.
            t1(RealScalarLike): final time.
            dt0(RealScalarLike): time step.
            ts(Sequence[RealScalarLike] | jax.Array | None): time steps to evaluate the boundary operators.

        Returns:
            operators(tuple[Const[timestep, batch, dim, dim], ...]):
                time-evolved boundary operators at each time step.
        """
        return tuple(
            op_t(
                self.ham.unwrap(),
                b.as_const(),
                t0,
                t1,
                dt0,
                ts=ts,
            )
            for b in self.ham.boundaryops()
        )

    def exp_boundary_corrs(
        self,
        selection: tuple[jax.Array, ...],
        t0: RealScalarLike,
        t1: RealScalarLike,
        dt0: RealScalarLike | None = None,
        *,
        ts: Sequence[RealScalarLike] | jax.Array | None = None,
    ) -> tuple[jax.Array, ...]:
        """Compute the expectation value of the boundary correlation functions.

        Args:

            selection(tuple[i32[n_samples], ...]): selection of boundary
                operators on each time step and boundary operator type. The selection should be
                the same length as `b_t`. The value of selection should be in the range of
                [0, #timestep x #boundary_ops).
            t0(RealScalarLike): initial time.
            t1(RealScalarLike): final time.
            dt0(RealScalarLike): time step.
            ts(Sequence[RealScalarLike] | jax.Array | None): time steps to evaluate the boundary correlation functions.

        Returns:
            correlations(tuple[jax.Array[], jax.Array[n_samples], ...]): boundary correlation functions at each order.
                If the ROS is batched the result will be averaged over the batch dimension.

            | order | #elements |
            |-------|-----------|
            | 0     | 1         |
            | 1     | 3         |
            | 2     | 7         |
            | 3     | 15        |
        """
        o_t = self.obs_t(t0, t1, dt0).squeeze(axes=0)
        b_t = self.boundary_t(t0, t1, dt0, ts=ts)
        corrs = self.__boundary_corrs(self.rho.as_const(), o_t, b_t, selection)
        if self.batch_shape:  # taking average on ensemble
            return tuple(
                b.reshape((self.n_batch, -1)).mean(axis=0).squeeze() for b in corrs
            )
        else:
            return corrs

    def n_boundary_corrs(self, n_samples: int, order: int) -> int:
        n_terms = 2 * (2**order - 1)
        n_corrs_per_order = n_samples * self.n_batch
        n_terms_per_o = self.n_batch + n_corrs_per_order * n_terms
        return n_terms_per_o

    def sample_tebo_selection(
        self, key: jax.Array, n_samples: int, n_timesteps: int, order: int
    ):
        """Sample the selection indices of time-evolved boundary operators (TEBO).

        Args:
            key(jax.Array): random key.
            n_samples(int): number of samples.
            n_timesteps(int): number of time steps stored in resulting TEBOs.
            order(int): order of the boundary correlation functions.

        Returns:
            tuple[tuple[jax.Array[n_samples], ...], ...]: #order `jax.Array`s of selection indices of TEBOs for each observable.
        """
        max_index = len(self.ham.boundaryops()) * n_timesteps
        return tuple(
            jax.random.randint(key, (n_samples,), 0, max_index) for _ in range(order)
        )

    @staticmethod
    def __boundary_corrs(
        rho0: Const,
        o_t: Const,
        b_t: tuple[Const, ...],
        selection: tuple[jax.Array, ...],
    ) -> tuple[jax.Array, ...]:
        """compute the boundary correlation functions.

        Args:
            rho0(Const[batch, dim, dim]): initial density matrix
            o_t(Const[batch, dim, dim]): time-ordered observable at final time.
            b_t(tuple[Const[timestep, batch, dim, dim], ...]): time-ordered boundary operators at each time step.
            selection(tuple[i32[n_samples], ...]): selection of boundary
                operators on each time step and boundary operator type. The selection should be
                the same length as `b_t`. The value of selection should be in the range of
                [0, #timestep x #boundary_ops).

        Returns:
            tuple[jax.Array[batch], jax.Array[n_samples, batch], ...]: boundary correlation functions at each order.

            | order | #elements |
            |-------|-----------|
            | 0     | 1         |
            | 1     | 3         |
            | 2     | 7         |
            | 3     | 15        |
        """
        zero_th = (batch.expect(rho0.as_array(), o_t.as_array()),)
        if len(selection) == 0:
            return zero_th

        Bt = jnp.stack(tuple(b.as_array() for b in b_t))
        # merge first two dim of Bt
        Bt = Bt.reshape((-1,) + Bt.shape[2:])
        return zero_th + batch.tobc(
            rho0.as_array(), tuple(Bt[pick] for pick in selection), o_t.as_array()
        )
