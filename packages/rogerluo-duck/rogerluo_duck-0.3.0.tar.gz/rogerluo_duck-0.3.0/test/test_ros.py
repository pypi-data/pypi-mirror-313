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

import math

import jax.numpy as jnp
import jax.scipy as jsp
import jax.random as jr

from duck import batch
from duck.ops import Pauli, State
from duck.ros import RelevantOpSet
from duck.rescalable import OpStr, SiteOp, chain


class TestROS:
    ros = RelevantOpSet.new(
        chain.tfim(1), OpStr.new(State.O), SiteOp.new({0: Pauli.Z, 1: Pauli.Z})
    )

    def test_dtype(self):
        assert self.ros.ham.dtype in (jnp.complex64, jnp.complex128)
        assert self.ros.rho.dtype in (jnp.complex64, jnp.complex128)
        assert self.ros.obs.dtype in (jnp.complex64, jnp.complex128)

    def test_batching(self):
        ros3 = self.ros.enlarge_to(3).batching(10)
        assert ros3.ham.batch_shape == (10,)
        assert ros3.rho.batch_shape == (10,)
        assert ros3.obs.batch_shape == (10,)

    def test_squeeze(self):
        ros3 = self.ros.enlarge_to(3).batching(1).squeeze()
        assert ros3.ham.batch_shape == ()
        assert ros3.rho.batch_shape == ()
        assert ros3.obs.batch_shape == ()

    def test_enlarge(self):
        ros3 = self.ros.enlarge_to(3)
        assert ros3.ham.n_sites == 3
        assert ros3.rho.n_sites == 3
        assert ros3.obs.n_sites == 3

    def test_as_dtype(self):
        ros3 = self.ros.enlarge_to(3).as_dtype(jnp.complex128)
        assert ros3.ham.dtype == jnp.complex128
        assert ros3.rho.dtype == jnp.complex128
        assert ros3.obs.dtype == jnp.complex128

    def test_obs_t(self):
        obs_t = self.ros.obs_t(0.0, 0.2, 1e-4)
        assert obs_t.shape == (1, 2, 2)
        U_t = jsp.linalg.expm(-0.2j * self.ros.ham.as_array())
        target_obs_t = U_t.conj().T @ self.ros.obs.as_array() @ U_t
        assert jnp.allclose(obs_t.as_array(), target_obs_t)
        assert jnp.allclose(
            self.ros.exp_obs_t(0.0, 0.2, 1e-4),
            jnp.trace(self.ros.rho.as_array() @ target_obs_t),
        )

        ros3 = self.ros.enlarge_to(3)
        obs_t = ros3.obs_t(0.0, 0.2, 1e-4)
        assert obs_t.shape == (1, 8, 8)
        U_t = jsp.linalg.expm(-0.2j * ros3.ham.as_array())
        target_obs_t = U_t.conj().T @ ros3.obs.as_array() @ U_t
        assert jnp.allclose(obs_t.as_array(), target_obs_t)
        assert jnp.allclose(
            ros3.exp_obs_t(0.0, 0.2, 1e-4),
            jnp.trace(ros3.rho.as_array() @ target_obs_t),
        )

        batch_ros = self.ros.batching(5)
        obs_t = batch_ros.obs_t(0.0, 0.2, 1e-4)
        assert obs_t.shape == (1, 5, 2, 2)
        U_t = jsp.linalg.expm(-0.2j * batch_ros.ham.as_array())
        target_obs_t = U_t.conj().transpose((0, 2, 1)) @ batch_ros.obs.as_array() @ U_t
        assert jnp.allclose(obs_t.as_array(), target_obs_t)
        result = batch_ros.exp_obs_t(0.0, 0.2, 1e-4)
        target = batch.expect(batch_ros.rho.as_array(), target_obs_t).mean()
        assert result.shape == target.shape
        assert jnp.allclose(result, target)

    def test_boundary_t(self):
        bt = self.ros.boundary_t(0.0, 0.3, 1e-4, ts=(0.1, 0.2, 0.3))
        B = self.ros.ham.boundaryops()[0]
        result = bt[0].as_array()
        assert len(bt) == 1
        assert result.shape == (3, 2, 2)
        U_t_1 = jsp.linalg.expm(-0.1j * self.ros.ham.as_array())
        U_t_2 = jsp.linalg.expm(-0.2j * self.ros.ham.as_array())
        U_t_3 = jsp.linalg.expm(-0.3j * self.ros.ham.as_array())
        target_bt_1 = U_t_1.conj().T @ B.as_array() @ U_t_1
        target_bt_2 = U_t_2.conj().T @ B.as_array() @ U_t_2
        target_bt_3 = U_t_3.conj().T @ B.as_array() @ U_t_3
        assert jnp.allclose(result[0], target_bt_1)
        assert jnp.allclose(result[1], target_bt_2)
        assert jnp.allclose(result[2], target_bt_3)

    def test_n_boundary_corrs(self):
        key = jr.PRNGKey(0)
        selection = self.ros.sample_tebo_selection(key, 10, 20, 2)
        assert len(selection) == 2
        assert selection[0].shape == (10,)

        tobc = self.ros.exp_boundary_corrs(
            selection, 0.0, 0.3, 1e-4, ts=jnp.linspace(0.1, 0.3, 20)
        )
        assert len(tobc) == 7
        assert tobc[0].shape == ()
        assert tobc[1].shape == (10,)

        assert self.ros.n_boundary_corrs(10, 2) == sum(
            math.prod(each.shape) for each in tobc
        )

        batched_ros = self.ros.batching(5)
        tobc = batched_ros.exp_boundary_corrs(
            selection, 0.0, 0.3, 1e-4, ts=jnp.linspace(0.1, 0.3, 20)
        )
        assert len(tobc) == 7
        assert tobc[0].shape == ()
        assert tobc[1].shape == (10,)
