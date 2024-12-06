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

from typing import Any, Sequence

import jax
import equinox as eqx
import jax.numpy as jnp
from jax.experimental import checkify

from duck.ros import RelevantOpSet
from duck.types import RealScalarLike
from duck.opmap.abc import OpMap


class RelevantOpSetPair(eqx.Module):
    before: RelevantOpSet
    mapped: RelevantOpSet

    def n_boundary_corrs(self, n_samples: int, order: int):
        return self.before.n_boundary_corrs(n_samples, order)

    def tobc_mse(
        self,
        selection: tuple[jax.Array, ...],
        t0: RealScalarLike,
        t1: RealScalarLike,
        dt0: RealScalarLike,
        *,
        ts: Sequence[RealScalarLike] | jax.Array | None = None,
    ):
        before = self.before.exp_boundary_corrs(selection, t0, t1, dt0, ts=ts)
        mapped = self.mapped.exp_boundary_corrs(selection, t0, t1, dt0, ts=ts)

        err = jnp.asarray(0.0)
        for each_tobc_before, each_tobc_mapped in zip(before, mapped):
            err += jnp.square(each_tobc_before - each_tobc_mapped).mean()
        return err


class Flow(eqx.Module):
    pairs: list[RelevantOpSetPair]

    @classmethod
    def new[
        State
    ](
        cls,
        fn: OpMap[State],
        state: State,
        first: RelevantOpSet,
        grow_step: int,
        grow_target: int,
    ):
        first_mapped, state = fn(first, state)
        prev = RelevantOpSetPair(first, first_mapped)
        pairs = [prev]
        for _ in range(grow_target - first.n_sites):
            enlarged = prev.mapped.enlarge_by(grow_step)
            enlarged_mapped, state = fn(enlarged, state)
            prev = RelevantOpSetPair(enlarged, enlarged_mapped)
            pairs.append(prev)
        return cls(pairs=pairs), state

    def predict(self):
        """Return the final RelevantOpSet for prediction by growing the last mapped set."""
        return self.pairs[-1].mapped.enlarge()

    @eqx.filter_jit
    def tobc_mse(
        self,
        t0: RealScalarLike,
        t1: RealScalarLike,
        dt0: RealScalarLike,
        *,
        key: jax.Array,
        n_samples: int,
        order: int,
        ts: jax.Array,
    ):
        assert t0 >= 0.0, "t0 should be greater than or equal to 0.0"
        assert t0 < t1, "t0 should be less than t1"
        checkify.check(
            ts[0] >= t0, "ts[0] should be greater than or equal to t0", debug=True
        )
        checkify.check(
            ts[-1] <= t1, "ts[-1] should be less than or equal to t1", debug=True
        )
        selection = self.pairs[0].before.sample_tebo_selection(
            key, n_samples, len(ts), order
        )
        err = jnp.asarray(0.0)
        for pair in self.pairs:
            err += pair.tobc_mse(selection, t0, t1, dt0, ts=ts)

        return err

    def summarize_tobc_mse(
        self,
        t0: RealScalarLike,
        t1: RealScalarLike,
        dt0: RealScalarLike,
        *,
        key: jax.Array,
        n_samples: int,
        order: int,
        ts: jax.Array,
    ):
        assert t0 >= 0.0, "t0 should be greater than or equal to 0.0"
        assert t0 < t1, "t0 should be less than t1"
        checkify.check(
            ts[0] >= t0, "ts[0] should be greater than or equal to t0", debug=True
        )
        checkify.check(
            ts[-1] <= t1, "ts[-1] should be less than or equal to t1", debug=True
        )
        selection = self.pairs[0].before.sample_tebo_selection(
            key, n_samples, len(ts), order
        )
        table: dict[str, dict[str, Any]] = {}
        for pair in self.pairs:
            before_exp_obs_t = pair.before.exp_obs_t(t0, t1, dt0)
            mapped_exp_obs_t = pair.mapped.exp_obs_t(t0, t1, dt0)

            table[f"{pair.before.n_sites}-sites"] = {
                "n_sites": pair.before.n_sites,
                "sqrt(tobc_mse)": jnp.sqrt(
                    pair.tobc_mse(selection, t0, t1, dt0, ts=ts)
                ),
                "exp_obs_t": {
                    "before": before_exp_obs_t,
                    "mapped": mapped_exp_obs_t,
                    "err": jnp.abs(before_exp_obs_t - mapped_exp_obs_t),
                },
            }

        ros = self.predict()
        return {
            "exp_obs_t": {
                "pred": ros.exp_obs_t(t0, t1, dt0),
                "n_sites": ros.n_sites,
            },
            "diagnostics": table,
        }
