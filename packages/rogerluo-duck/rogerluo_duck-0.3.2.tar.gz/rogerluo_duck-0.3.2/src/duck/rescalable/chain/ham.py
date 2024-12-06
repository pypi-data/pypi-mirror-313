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

from duck import time
from duck.ops.const import Spin, Pauli
from duck.rescalable.a import OpA

from .ab import OpAB


def tfim(
    n_sites: int,
    h: time.FactorsLike | None = None,
):
    return (OpAB.new(Pauli.Z, Pauli.Z) + OpA.new(Pauli.X, h)).enlarge_to(n_sites)


def heisenberg(
    n_sites: int,
    h: time.FactorsLike | None = None,
):
    ret = OpAB.new(Spin.X, Spin.X) + OpAB.new(Spin.Y, Spin.Y) + OpAB.new(Spin.Z, Spin.Z)
    if h is not None:
        ret += OpA.new(Spin.Z, h)
    return ret.enlarge_to(n_sites)
