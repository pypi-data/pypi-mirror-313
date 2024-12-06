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

from logging import Handler, LogRecord

from wandb.sdk.wandb_run import Run

from duck.task.logging.json_like import josn_like


class WandbHandler(Handler):
    def __init__(self, run: Run):
        super().__init__()
        self.run = run

    def emit(self, record: LogRecord):
        if not isinstance(record.msg, dict):
            return

        if "__meta__" in record.msg.keys():
            return

        self.run.log(josn_like(record.msg))

    def close(self) -> None:
        super().close()
        self.run.finish()
