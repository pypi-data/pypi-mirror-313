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

import sys
from typing import Any
from pathlib import Path
from dataclasses import field

from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from duck.task.env import PyProject


@dataclass(frozen=True)
class Grow:
    start: int
    """initial scale"""
    target: int
    """target scale"""
    step: int = 1
    """growing step (scale size increase)"""


@dataclass(kw_only=True, frozen=True)
class Evolution:
    t0: float = 0.0
    """initial time"""
    t1: float
    """final time"""
    dt0: float | None = None
    """initial time step"""
    n_timesteps: int = 20
    """number of timesteps save per evolution for TOBCs"""


@dataclass(frozen=True)
class Loss:
    n_samples: int = 20
    """number of samples for TOBCs"""
    order: int = 2
    """maximum order of the TOBCs in loss function"""


@dataclass
class Logging:
    every: int = 10
    """log every `every` epochs"""
    file: bool = False
    """log to file, default `False`"""
    data_dir: Path = field(default_factory=lambda: PyProject().duck_data_dir)
    """directory to save logs"""
    wandb: bool = False


@dataclass(kw_only=True)
class Config:
    name: str = field(
        default_factory=lambda: Path(sys.argv[0]).resolve().with_suffix("").name
    )
    """name of the task, default is the name of the script"""
    note: str = ""
    """note of the task"""
    seed: int = 42
    """random seed"""
    n_epochs: int
    """number of epochs"""
    logging: Logging = field(default_factory=Logging)
    """logging configuration"""
    progress: bool = False
    "show progress bar, default `False`"
    evolution: Evolution
    """evolution configuration"""
    loss: Loss
    """loss configuration"""
    grow: Grow
    """grow configuration"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        return TypeAdapter(cls).validate_python(data)

    def dump(self) -> dict[str, Any]:
        return TypeAdapter(type(self)).dump_python(self)
