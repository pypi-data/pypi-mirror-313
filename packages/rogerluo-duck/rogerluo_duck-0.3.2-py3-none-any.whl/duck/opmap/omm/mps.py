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
import equinox as eqx
import jax.numpy as jnp
import jax.random as jr

from duck import batch
from duck.ops import Const
from duck.ops.abc import Op
from duck.opmap.abc import OMM


class MPS(OMM[None]):
    """Matrix Product State in canonical form.

    This class represents a Matrix Product State (MPS) in canonical form
    that can be used in duck RG. The MPS is represented as a sequence of
    isometries that act on the input operator. The isometries are
    initialized randomly.

    If a `batch_shape` is provided, the isometries are initialized with
    the extra batch dimensions. This represents an ensemble of MPS, when
    feeding into the `RelevantOpSet.map_const` method, the `RelevantOpSet`
    will take an average on the batch dimensions so that the output are from
    the ensemble.
    """

    isometries: tuple[jax.Array, ...]
    n_sites_start: int = eqx.field(static=True)
    n_sites_step: int = eqx.field(static=True)
    batch_shape: tuple[int, ...] = eqx.field(static=True)
    bond_dims: tuple[int, ...] = eqx.field(static=True)

    def __init__(
        self,
        key: jax.Array,
        n_sites_start: int,
        bond_dims: tuple[int, ...],
        *,
        n_sites_step: int = 1,
        dtype: jnp.dtype = jnp.float32,
        batch_shape: tuple[int, ...] = (),
    ):
        isometries: list[jax.Array] = []
        output_dims = 2 ** (n_sites_start - n_sites_step)
        for bond in bond_dims:
            input_dims = output_dims * 2**n_sites_step
            output_dims = bond

            # check if dtype is complex
            if dtype == jnp.complex64 or dtype == jnp.complex128:
                proj = jr.normal(
                    key, batch_shape + (input_dims, output_dims), dtype=dtype
                ).astype(dtype)
            else:
                proj = jr.normal(
                    key, batch_shape + (input_dims, output_dims), dtype=dtype
                )
            proj = jnp.linalg.qr(proj)[0]
            isometries.append(proj)

        self.n_sites_start = n_sites_start
        self.n_sites_step = n_sites_step
        self.batch_shape = batch_shape
        self.bond_dims = bond_dims
        self.isometries = tuple(isometries)

    def initialize(self, key: jax.Array) -> tuple[None, jax.Array]:
        return None, key

    def map(self, op: Op, state: None) -> tuple[Op, None]:
        assert (
            op.n_sites >= self.n_sites_start
        ), f"input operator has too few sites, got {op.n_sites} < {self.n_sites_start}"
        assert (
            op.n_sites < self.n_sites_start + len(self.isometries) * self.n_sites_step
        ), f"input operator has too many sites, got {op.n_sites} > {self.n_sites_start + len(self.isometries) * self.n_sites_step - 1}"
        isometry = self.isometries[op.n_sites - self.n_sites_start]
        isometry = jnp.linalg.qr(isometry)[0]
        return (
            Const(
                batch.mm(
                    batch.mm(
                        batch.dagger(isometry),
                        op.as_array(),
                    ),
                    isometry,
                ),
                op.n_sites,
            ),
            None,
        )
