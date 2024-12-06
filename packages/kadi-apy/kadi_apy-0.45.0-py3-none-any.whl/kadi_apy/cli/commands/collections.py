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
from xmlhelpy import Path
from xmlhelpy import TokenList
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import search_pagination_options
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.main import kadi_apy
from kadi_apy.globals import RESOURCE_ROLES


@kadi_apy.group()
def collections():
    """Commands to manage collections."""


@collections.command()
@apy_command
@option("title", char="t", description="Title of the collection.")
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the collection.",
    default=None,
)
@option(
    "visibility",
    char="v",
    description="Visibility of the collection.",
    default="private",
    param_type=Choice(["private", "public"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned collection id.",
    is_flag=True,
)
@option(
    "exit-not-created",
    char="e",
    description="Exit with error if the collection was not newly created.",
    is_flag=True,
)
def create(manager, **kwargs):
    """Create a collection."""

    manager.collection(**kwargs, create=True)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", helptext="to edit.")
@option(
    "visibility",
    char="v",
    description="Visibility of the collection to set.",
    default=None,
    param_type=Choice(["private", "public"]),
)
@option("title", char="t", default=None, description="Title of the collection to set.")
@option(
    "description",
    char="d",
    default=None,
    description="Description of the collection to set.",
)
def edit(collection, visibility, title, description):
    """Edit the metadata of a collection."""

    collection.set_attribute(
        visibility=visibility, title=title, description=description
    )


@collections.command()
@apy_command
@id_identifier_options(class_type="collection")
@option(
    "description",
    char="d",
    description="Show the description of the collection.",
    is_flag=True,
    default=False,
)
@option(
    "visibility",
    char="v",
    description="Show the visibility of the collection.",
    is_flag=True,
    default=False,
)
@option(
    "records",
    char="r",
    description="Show linked records of the collection.",
    is_flag=True,
    default=False,
)
@option(
    "subcollections",
    char="s",
    description="Show linked child-collections of the collection.",
    is_flag=True,
    default=False,
)
@search_pagination_options
def show_info(collection, **kwargs):
    """Show info of a collection."""

    collection.print_info(**kwargs)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="collection", helptext="to add the user.", keep_manager=True
)
@user_id_options()
@option(
    "permission-new",
    char="p",
    description="Permission of new user.",
    default="member",
    param_type=Choice(RESOURCE_ROLES["collection"]),
)
def add_user(collection, user, permission_new):
    """Add a user to a collection."""

    collection.add_user(user=user, permission_new=permission_new)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="collection", helptext="to remove the user.", keep_manager=True
)
@user_id_options()
def remove_user(collection, user):
    """Remove a user from a collection."""

    collection.remove_user(user=user)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="collection",
    helptext="to add the group with role permissions.",
    keep_manager=True,
)
@id_identifier_options(class_type="group")
@option(
    "permission-new",
    char="p",
    description="Permission of the group.",
    default="member",
    param_type=Choice(RESOURCE_ROLES["collection"]),
)
def add_group_role(collection, group, permission_new):
    """Add a group role to a collection."""

    collection.add_group_role(group, permission_new)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="collection", helptext="to remove the group.", keep_manager=True
)
@id_identifier_options(class_type="group")
def remove_group_role(collection, group):
    """Remove a group role from a collection."""

    collection.remove_group_role(group)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", helptext="to delete.")
@option(
    "i-am-sure",
    description="Enable this option to delete the collection.",
    is_flag=True,
)
def delete(collection, i_am_sure):
    """Delete a collection."""

    collection.delete(i_am_sure)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="collection", helptext="to link to the record.", keep_manager=True
)
@id_identifier_options(class_type="record", helptext="to link to the collection.")
def add_record_link(collection, record):
    """Link record to a collection."""

    collection.add_record_link(record_to=record)


@collections.command()
@apy_command
@id_identifier_options(
    class_type="collection", helptext="to remove the record.", keep_manager=True
)
@id_identifier_options(class_type="record", helptext="to remove from the collection.")
def remove_record_link(collection, record):
    """Remove a record link from a collection."""

    collection.remove_record_link(record)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", keep_manager=True)
@id_identifier_options(
    class_type="collection",
    name="child",
    helptext="to link to the parent collection.",
    char="l",
)
def add_collection_link(collection, child):
    """Link a child collection to a parent collection."""

    collection.add_collection_link(child)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", keep_manager=True)
@id_identifier_options(
    class_type="collection",
    name="child",
    helptext="to remove from the parent collection.",
    char="l",
)
def remove_collection_link(collection, child):
    """Remove a child collection from a parent collection."""

    collection.remove_collection_link(child)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", helptext="to add a tag.")
@option(
    "tag",
    char="t",
    required=True,
    description="Tag to add.",
    param_type=TokenList,
)
def add_tag(collection, tag):
    """Add a tag or several tags to a collection."""

    for i in tag:
        collection.add_tag(i)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", helptext="to remove a tag.")
@option("tag", char="t", required=True, description="Tag to remove.")
def remove_tag(collection, tag):
    """Remove a tag from a collection."""

    collection.remove_tag(tag)


@collections.command()
@apy_command
@option(
    "tag",
    char="t",
    description="Tag(s) for search.",
    param_type=TokenList,
    excludes=["user", "use-my-user-id"],
)
@option(
    "tag-operator",
    char="T",
    description="The operator to filter the tags with. Defaults to 'or'.",
    param_type=Choice(["or", "and"]),
    excludes=["user", "use-my-user-id"],
)
@search_pagination_options
@user_id_options(
    helptext="to show the user's created collections.",
    required=False,
    keep_manager=True,
)
@option(
    "use-my-user-id",
    char="i",
    description="Show only own created collections.",
    is_flag=True,
)
@option(
    "visibility",
    char="v",
    description="Show results based on visibility parameter.",
    param_type=Choice(["private", "public", "all"]),
    excludes=["user", "use-my-user-id"],
)
@option(
    "query",
    char="q",
    description="The search query.",
    excludes=["user", "use-my-user-id"],
)
def get_collections(manager, user, use_my_user_id, **kwargs):
    """Search for collections."""

    if kwargs["visibility"] == "all":
        kwargs["visibility"] = None

    manager.search.search_resources(
        "collection", user=user, use_my_user_id=use_my_user_id, **kwargs
    )


@collections.command()
@apy_command
@option("tag", char="t", description="Tag(s) for search.", param_type=TokenList)
@option(
    "tag-operator",
    char="T",
    description="The operator to filter the tags with.",
    param_type=Choice(["or", "and"]),
    default="or",
)
@option(
    "visibility",
    char="v",
    description="Show results based on visibility parameter.",
    default="all",
    param_type=Choice(["private", "public", "all"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned."
    " collection ids as tokenlist.",
    is_flag=True,
)
@option(
    "i-am-sure",
    description="Enable this option in case more than 1000 results are found.",
    is_flag=True,
)
def get_collection_ids(manager, **kwargs):
    """Search for collections. The ids of all found results are displayed."""

    if kwargs["visibility"] == "all":
        kwargs["visibility"] = None

    manager.search.search_resource_ids("collection", **kwargs)


@collections.command()
@apy_command
@id_identifier_options(class_type="collection", helptext="to export.")
@option(
    "export-type",
    char="e",
    description="Export type.",
    default="json",
    param_type=Choice(["json", "qr", "rdf", "ro-crate"]),
)
@option(
    "path",
    char="p",
    description="Path (folder) to store the file.",
    param_type=Path(exists=True),
    default=".",
)
@option(
    "name",
    char="n",
    description="Name of the file to store. The identifier is used as default.",
)
@option(
    "force",
    char="f",
    description="Enable if existing file with identical name should be replaced.",
    is_flag=True,
    default=False,
)
@option(
    "pipe",
    char="P",
    description="Use this flag if you want to pipe the returned json.",
    is_flag=True,
)
@option(
    "use-folder",
    char="u",
    description="Create, if not already existing, a folder in the specified file path"
    " with the collection's identifier as name and save the exported file in this"
    " folder.",
    is_flag=True,
    default=False,
)
def export(collection, export_type, path, name, force, pipe, use_folder):
    """Export the collection using a specific export type."""

    collection.export(export_type, path, name, force, pipe, use_folder)
