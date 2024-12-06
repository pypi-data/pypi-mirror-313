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
from typing import Sequence

import jax
import diffrax
import equinox as eqx

from duck.ops import Op, Const
from duck.types import RealScalarLike


class HeisenbergEq(eqx.Module):
    ham: Op

    @eqx.filter_jit
    def __call__(self, t: RealScalarLike, y: Const, args: None = None):
        return 1.0j * self.ham(t).comm(y)


# TODO: forward more diffeqsolve options
# NOTE: see also https://github.com/patrick-kidger/diffrax/pull/197 about the warning
def op_t(
    ham: Op,
    op0: Const,
    t0: RealScalarLike,
    t1: RealScalarLike,
    dt0: RealScalarLike | None = None,
    *,
    ts: Sequence[RealScalarLike] | jax.Array | None = None,
    max_steps: int | None = 4096,
) -> Const:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        sol = diffrax.diffeqsolve(
            diffrax.ODETerm(HeisenbergEq(ham)),
            diffrax.Tsit5(),
            t0=t0,
            t1=t1,
            dt0=dt0,
            y0=op0,
            saveat=diffrax.SaveAt(ts=ts) if ts is not None else diffrax.SaveAt(t1=True),
            max_steps=max_steps,
        )
        assert sol.ys is not None
    return sol.ys
