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

import logging
from typing import Any, Mapping
from logging import LogRecord
from datetime import datetime

from tomlkit import dumps

from duck.task.logging.json_like import josn_like


class TOMLFormatter(logging.Formatter):
    """Format log record as TOML.

    Args:
        datefmt: Date format string.
        time_stamp: Whether to include time stamp in the log.

    This formatter expects the log message to be a `Mapping`, e.g a `Dict`.
    If the log message has a key `__meta__` and its value is a `Dict`, then
    the `__meta__` is dumped at the beginning of the log as a header. This is
    useful for logging metadata that is common across all log messages.

    In other cases, the log message is wrapped in a `log` key and dumped as a
    list of log messages. This is useful for appending log messages to the same
    log file.
    """

    def __init__(self, datefmt: str | None = None, time_stamp=True) -> None:
        super().__init__(datefmt=datefmt)
        self.meta_has_formated = False
        self.time_stamp = time_stamp

    def format(self, record: LogRecord) -> str:
        if not isinstance(record.msg, Mapping):
            raise TypeError("Log message must be a Mapping, e.g a Dict")

        if (
            not self.meta_has_formated
            and (meta := record.msg.get("__meta__", None)) is not None
            and isinstance(meta, dict)
        ):
            # NOTE: dump meta as header
            return dumps(josn_like(meta)) + "\n"

        if err := record.msg.get("err", None):
            return "\n" + dumps({"log": [{"err": err}]}) + "\n"

        data: dict[str, Any] = {
            "name": record.name,
            "level": record.levelname,
        }
        if self.time_stamp:
            data["time"] = datetime.fromtimestamp(record.created)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            data["exc_text"] = record.exc_text
        if record.stack_info:
            data["stack_info"] = self.formatStack(record.stack_info)

        data["msg"] = josn_like(record.msg)
        return "\n" + dumps({"log": [data]})  # so that we can keep appending log
