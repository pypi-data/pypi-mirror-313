# Copyright 2020 Karlsruhe Institute of Technology
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
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.lib.resources.users import User


class CLIUser(User, RaiseRequestErrorMixin):
    """User class to be used in a CLI.

    See :class:`.User` for the possible parameters.
    """

    def print_info(self):
        """Print user infos using a CLI."""

        self.info(
            f"Displayname: {self.meta['displayname']}\n"
            f"ID: {self.id}\n"
            f"Username: {self.meta['identity']['username']}\n"
            f"Identity type: {self.meta['identity']['type']}"
        )
