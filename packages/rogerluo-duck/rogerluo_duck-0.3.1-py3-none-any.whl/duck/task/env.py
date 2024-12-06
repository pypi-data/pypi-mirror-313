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
from typing import Any, Mapping
from pathlib import Path

from tomlkit import parse


def find_pyproject(root: Path | None = None):
    if root is None:
        root = Path(sys.argv[0]).resolve()

    for directory in [root, *root.resolve().parents]:
        candidate = directory / "pyproject.toml"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("pyproject.toml not found")


class PyProject:
    def __init__(self, path: Path | str | None = None):
        if isinstance(path, str):
            path = Path(path)

        self.path = find_pyproject(path)
        self.data = self.parse()

    def parse(self):
        with self.path.open() as file:
            return parse(file.read())

    def __repr__(self):
        return f'PyProject("{self.path}")'

    @property
    def tool(self) -> Mapping[str, Mapping[str, Any]]:
        if "tool" not in self.data.keys():
            return {}

        item = self.data["tool"].unwrap()
        if isinstance(item, dict):
            return item

        raise ValueError("tool is not a dictionary")

    @property
    def duck_data_dir(self) -> Path:
        tool = self.tool
        if "duck" in tool.keys():
            path = tool["duck"].get("data_dir", "data")
        else:
            path = "data"

        return self.path.parent / Path(path)
