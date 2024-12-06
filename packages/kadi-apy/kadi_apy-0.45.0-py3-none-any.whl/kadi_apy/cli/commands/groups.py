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
from xmlhelpy import Choice
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import search_pagination_options
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.main import kadi_apy


@kadi_apy.group()
def groups():
    """Commands to manage groups."""


@groups.command()
@apy_command
@option("title", char="t", description="Title of the group.")
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the group.",
    default=None,
)
@option(
    "visibility",
    char="v",
    description="Visibility of the group.",
    default="private",
    param_type=Choice(["private", "public"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned group id.",
    is_flag=True,
)
@option(
    "exit-not-created",
    char="e",
    description="Exit with error if the group was not newly created.",
    is_flag=True,
)
def create(manager, **kwargs):
    """Create a group."""

    manager.group(create=True, **kwargs)


@groups.command()
@apy_command
@id_identifier_options(class_type="group", helptext="to edit.")
@option(
    "visibility",
    char="v",
    description="Visibility of the group to set.",
    default=None,
    param_type=Choice(["private", "public"]),
)
@option("title", char="t", default=None, description="Title of the group to set.")
@option(
    "description",
    char="d",
    default=None,
    description="Description of the group to set.",
)
def edit(group, visibility, title, description):
    """Edit the metadata of a group."""

    group.set_attribute(visibility=visibility, title=title, description=description)


@groups.command()
@apy_command
@id_identifier_options(class_type="group")
@option(
    "description",
    char="d",
    description="Show the description of the group.",
    is_flag=True,
    default=False,
)
@option(
    "visibility",
    char="v",
    description="Show the visibility of the group.",
    is_flag=True,
    default=False,
)
def show_info(group, **kwargs):
    """Show info of a group."""

    group.print_info(**kwargs)


@groups.command()
@apy_command
@id_identifier_options(
    class_type="group", helptext="to add the user.", keep_manager=True
)
@user_id_options(helptext="to add to the group.")
@option(
    "permission-new",
    char="p",
    description="Permission of new user.",
    default="member",
    param_type=Choice(["member", "editor", "admin"]),
)
def add_user(group, user, permission_new):
    """Add a user to a group."""

    group.add_user(user=user, permission_new=permission_new)


@groups.command()
@apy_command
@id_identifier_options(
    class_type="group", helptext="to remove the user.", keep_manager=True
)
@user_id_options(helptext="to remove from the group.")
def remove_user(group, user):
    """Remove a user from a group."""

    group.remove_user(user=user)


@groups.command()
@apy_command
@id_identifier_options(class_type="group", helptext="to delete.")
@option(
    "i-am-sure", description="Enable this option to delete the group.", is_flag=True
)
def delete(group, i_am_sure):
    """Delete a group."""

    group.delete(i_am_sure)


@groups.command()
@apy_command
@search_pagination_options
@user_id_options(
    helptext="to show the user's created groups.", required=False, keep_manager=True
)
@option(
    "my_user_id",
    char="i",
    description="Show only own created groups.",
    is_flag=True,
)
@option(
    "visibility",
    char="v",
    description="Show results based on visibility parameter.",
    default="all",
    param_type=Choice(["private", "public", "all"]),
)
def get_groups(manager, user, my_user_id, **kwargs):
    """Search for groups."""

    if kwargs["visibility"] == "all":
        kwargs["visibility"] = None

    manager.search.search_resources("group", user=user, my_user_id=my_user_id, **kwargs)
