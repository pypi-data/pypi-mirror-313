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

from typing import Callable

import jax
import equinox as eqx
from jaxtyping import PyTree

from duck.ros import RelevantOpSet
from duck.flow import Flow
from duck.opmap.abc import OpMap

type GradLoss[State] = Callable[
    [OpMap[State], State, int, jax.Array],
    tuple[tuple[jax.Array, State], PyTree],
]


def tobc_mse_loss[
    State
](
    ros: RelevantOpSet,
    t0: float,
    t1: float,
    dt0: float,
    grow_step: int,
    *,
    n_samples: int = 20,
    order: int = 2,
    ts: jax.Array,
) -> GradLoss[State]:
    """Return a function that computes the time-ordered boundary correlation
    (TOBC) mean squared error (MSE) loss and its gradient.

    Args:
        ros: The relevant operator set.
        state: The initial state passed to the ansatz.
        t0: The initial time.
        t1: The final time.
        dt0: The time step.
        n_samples: The number of samples.
        order: The order of the integrator.
        ts: The time points.

    Returns:
        A function that computes the TOBC MSE loss and its gradient.
    """

    @eqx.filter_value_and_grad(has_aux=True)
    def grad_loss(
        ansatz: OpMap[State],
        state: State,
        grow_target: int,
        key: jax.Array,
    ):
        flow, state_ = Flow.new(ansatz, state, ros, grow_step, grow_target)
        mse = flow.tobc_mse(
            t0, t1, dt0, key=key, n_samples=n_samples, order=order, ts=ts
        )
        return mse, state_

    return grad_loss
