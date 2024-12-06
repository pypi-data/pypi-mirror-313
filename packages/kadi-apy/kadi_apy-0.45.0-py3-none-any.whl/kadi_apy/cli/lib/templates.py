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
from kadi_apy.cli.commons import BasicCLIMixin
from kadi_apy.cli.commons import DeleteItemCLIMixin
from kadi_apy.cli.commons import ExportCLIMixin
from kadi_apy.cli.commons import GroupRoleCLIMixin
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.cli.commons import UserCLIMixin
from kadi_apy.lib.resources.templates import Template


class CLITemplate(
    BasicCLIMixin,
    DeleteItemCLIMixin,
    ExportCLIMixin,
    UserCLIMixin,
    GroupRoleCLIMixin,
    Template,
    RaiseRequestErrorMixin,
):
    """Template class to be used in a CLI.

    :param manager: See :class:`.Template`.
    :param type: See :class:`.Template`.
    :param data: See :class:`.Template`.
    :param id: See :class:`.Template`.
    :param identifier: See :class:`.Template`.
    :param skip_request: See :class:`.Template`.
    :param create: See :class:`.Template`.
    :param pipe: Flag to indicate if only the id should be printed which can be used for
        piping.
    :type pipe: bool, optional
    :param title: Title of the new resource.
    :type title: str, optional
    :param exit_not_created: Flag to indicate if the function should exit with
        ``sys.exit(1)`` if the resource is not created.
    :type exit_not_created: bool, optional
    """

    def __init__(
        self, pipe=False, title=None, create=False, exit_not_created=False, **kwargs
    ):
        super().__init__(title=title, create=create, **kwargs)

        self._print_item_created(
            title=title,
            pipe=pipe,
            create=create,
            exit_not_created=exit_not_created,
        )
