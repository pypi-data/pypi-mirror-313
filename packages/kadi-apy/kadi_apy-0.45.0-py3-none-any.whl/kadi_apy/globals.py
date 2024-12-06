# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import Enum
from pathlib import Path


CONFIG_PATH = Path.home().joinpath(".kadiconfig")

RESOURCE_ROLES = {
    "record": ["member", "collaborator", "editor", "admin"],
    "collection": ["member", "collaborator", "editor", "admin"],
    "group": ["member", "editor", "admin"],
    "template": ["member", "editor", "admin"],
}

RESOURCE_TYPES = ["record", "collection", "group", "template"]


class Verbose(Enum):
    """Class to handle different verbose level for output."""

    ERROR = 30
    WARNING = 20
    INFO = 10
    DEBUG = 0
