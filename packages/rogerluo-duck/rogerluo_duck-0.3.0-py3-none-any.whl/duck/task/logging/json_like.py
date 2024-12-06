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

from typing import Any, overload
from pathlib import Path

import jax


@overload
def josn_like(data: dict[str, Any]) -> dict[str, Any]: ...


@overload
def josn_like(data: jax.Array) -> list | int | float | str: ...


@overload
def josn_like(data: list) -> list: ...


@overload
def josn_like(data: Path) -> str: ...


@overload
def josn_like(data: Any) -> int | float | str: ...


def josn_like(data) -> dict | list | int | float | str:
    if isinstance(data, dict):
        return {k: josn_like(v) for k, v in data.items()}
    elif isinstance(data, jax.Array):
        if data.ndim == 0:
            return data.item()
        else:
            return data.tolist()
    elif isinstance(data, list):
        return [josn_like(v) for v in data]
    elif isinstance(data, Path):
        return str(data)
    else:
        return data
