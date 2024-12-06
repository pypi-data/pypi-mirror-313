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
from xmlhelpy import Integer
from xmlhelpy import Path
from xmlhelpy import TokenList
from xmlhelpy import option

from kadi_apy.cli.commons import validate_metadatum
from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import file_id_options
from kadi_apy.cli.decorators import id_identifier_options
from kadi_apy.cli.decorators import search_pagination_options
from kadi_apy.cli.decorators import user_id_options
from kadi_apy.cli.main import kadi_apy
from kadi_apy.globals import RESOURCE_ROLES
from kadi_apy.lib.helper import list_to_tokenlist


@kadi_apy.group()
def records():
    """Commands to manage records."""


@records.command()
@apy_command
@option(
    "identifier",
    char="i",
    required=True,
    description="Identifier of the record",
    default=None,
)
@option("title", char="t", description="Title of the record")
@option(
    "visibility",
    char="v",
    description="Visibility of the record",
    default="private",
    param_type=Choice(["private", "public"]),
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned record id.",
    is_flag=True,
)
@option(
    "exit-not-created",
    char="e",
    description="Exit with error if the record was not newly created.",
    is_flag=True,
)
def create(manager, **kwargs):
    """Create a record."""

    manager.record(create=True, **kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to edit.")
@option(
    "visibility",
    char="v",
    description="Visibility of the record",
    default=None,
    param_type=Choice(["private", "public"]),
)
@option("title", char="t", default=None, description="Title of the record")
@option("description", char="d", default=None, description="Description of the record")
@option("type", char="y", default=None, description="Type of the record")
@option("license", char="l", default=None, description="License of the record")
def edit(record, **kwargs):
    """Edit the basic metadata of a record."""

    record.set_attribute(**kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="record", keep_manager=True)
@user_id_options("to add.")
@option(
    "permission-new",
    char="p",
    description="Permission of new user.",
    default="member",
    param_type=Choice(RESOURCE_ROLES["record"]),
)
def add_user(record, user, permission_new):
    """Add a user to a record."""

    record.add_user(user, permission_new)


@records.command()
@apy_command
@id_identifier_options(
    class_type="record",
    helptext="to add the group with role permissions.",
    keep_manager=True,
)
@id_identifier_options(class_type="group")
@option(
    "permission-new",
    char="p",
    description="Permission of the group",
    default="member",
    param_type=Choice(RESOURCE_ROLES["record"]),
)
def add_group_role(record, group, permission_new):
    """Add a group role to a record."""

    record.add_group_role(group, permission_new)


@records.command()
@apy_command
@id_identifier_options(class_type="record", keep_manager=True)
@id_identifier_options(class_type="group")
def remove_group_role(record, group):
    """Remove a group role from a record."""

    record.remove_group_role(group)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "description",
    char="d",
    description="Show the description of the record",
    is_flag=True,
    default=False,
)
@option(
    "filelist",
    char="l",
    description="Show the filelist of the record",
    is_flag=True,
    default=False,
)
@search_pagination_options(description_page="Page for filelist.")
@option(
    "metadata",
    char="m",
    description="Show the metadata of the record.",
    is_flag=True,
    default=False,
)
@option(
    "visibility",
    char="v",
    description="Show the visibility of the record.",
    is_flag=True,
    default=False,
)
@option(
    "pipe",
    char="i",
    description="Use for piping. Do not show basic info.",
    is_flag=True,
    default=False,
)
def show_info(record, **kwargs):
    """Prints information of a record."""

    record.print_info(**kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option("file-name", char="n", required=True, description="Name of the file or folder")
@option("file-description", char="d", description="The description of a single file")
@option(
    "pattern",
    char="p",
    description="Pattern for selecting certain files when using a folder as input."
    " By default, all files are taken into account."
    " To set a pattern, Unix shell-style wildcards can be used (see Python package"
    " fnmatch).",
)
@option(
    "exclude_pattern",
    char="e",
    description="Pattern for excluding certain files when using a folder as input."
    " To set a pattern, Unix shell-style wildcards can be used (see Python package"
    " fnmatch).",
)
@option(
    "force",
    char="f",
    description="Enable if existing file(s) with identical name(s) should be replaced.",
    is_flag=True,
    default=False,
)
def add_files(record, **kwargs):
    """Add a file or a folder content to a record."""

    record.upload_file(**kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "string",
    char="s",
    required=True,
    description="String to be added as file to the record.",
)
@option(
    "file-name",
    char="n",
    required=True,
    description="Name of the file to store the sting.",
)
@option(
    "force",
    char="f",
    description="Enable if existing file with identical name should be replaced.",
    is_flag=True,
    default=False,
)
def add_string_as_file(record, string, file_name, force):
    """Add a string as a file to a record."""

    record.upload_string_to_file(string, file_name, force=force)


@records.command()
@apy_command
@id_identifier_options(class_type="record", keep_manager=True)
@user_id_options(helptext="to remove.")
def remove_user(record, user):
    """Remove a user from a record."""

    record.remove_user(user)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to delete.")
@option(
    "i-am-sure", description="Enable this option to delete the record", is_flag=True
)
def delete(record, i_am_sure):
    """Delete a record."""

    record.delete(i_am_sure)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to add a metadatum.")
@option("metadatum", char="m", required=True, description="Name of metadatum to add")
@option("value", char="v", required=True, description="Value of metadatum to add")
@option(
    "type",
    char="t",
    description="Type of metadatum to add",
    param_type=Choice(["string", "integer", "float", "boolean"]),
    default="string",
)
@option(
    "unit",
    char="u",
    description="Unit of metadatum to add",
    default=None,
)
@option(
    "force",
    char="f",
    description="Force overwriting existing metadatum with identical name",
    is_flag=True,
    default=False,
)
def add_metadatum(record, force, metadatum, value, type, unit):
    """Add a metadatum to a record."""

    metadatum_new = validate_metadatum(
        metadatum=metadatum, value=value, type=type, unit=unit
    )

    record.add_metadatum(metadatum_new=metadatum_new, force=force)


@records.command()
@apy_command
@id_identifier_options(
    class_type="record",
    helptext="to add metadata as dictionary or as a list of dictionaries.",
)
@option("metadata", char="m", description="Metadata string input", default=None)
@option(
    "file",
    char="p",
    description="Path to file containing metadata",
    param_type=Path(exists=True),
    default=None,
)
@option(
    "force",
    char="f",
    description="Force deleting and overwriting existing metadata.",
    is_flag=True,
    default=False,
)
def add_metadata(record, metadata, file, force):
    """Add metadata with dict or a list of dicts as input."""

    record.add_metadata(metadata=metadata, file=file, force=force)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to delete a metadatum.")
@option(
    "metadatum", char="m", required=True, description="Name of metadatum to remove."
)
def delete_metadatum(record, metadatum):
    """Delete a metadatum of a record."""

    record.remove_metadatum(metadatum)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to delete all metadata.")
@option(
    "i-am-sure",
    description="Enable this option to delete all metadata of the record.",
    is_flag=True,
)
def delete_all_metadata(record, i_am_sure):
    """Delete all metadatum of a record."""

    record.remove_all_metadata(i_am_sure)


@records.command()
@apy_command
@id_identifier_options(
    class_type="record",
    helptext="to download files from.",
    allow_tokenlist=True,
)
@file_id_options(helptext="to download.", required=False)
@option(
    "filepath",
    char="p",
    description="Path (folder) to store the file.",
    param_type=Path(exists=True),
    default=".",
)
@option(
    "pattern",
    char="P",
    description="Pattern for selecting certain files. To set a pattern, Unix"
    " shell-style wildcards can be used (see Python package fnmatch).",
)
@option(
    "exclude_pattern",
    char="e",
    description="Pattern for excluding certain files. To set a pattern, Unix"
    " shell-style wildcards can be used (see Python package fnmatch).",
)
@option(
    "force",
    char="f",
    description="Force overwriting file in the given folder.",
    is_flag=True,
    default=False,
)
@option(
    "use-folder",
    char="u",
    description="Create, if not already existing, a folder in the specified file path"
    " with the record's identifier as name and saves all files in this folder.",
    is_flag=True,
    default=False,
)
@option(
    "pipe",
    char="E",
    description="Use this flag if you want to pipe the returned tokenlist of downloaded"
    " files.",
    is_flag=True,
)
def get_file(
    manager,
    record,
    file_id,
    filepath,
    pattern,
    exclude_pattern,
    force,
    use_folder,
    record_ids,
    pipe,
):
    """Download one file, all files or files with pattern from a record."""
    list_downloaded = []

    if record is not None:
        list_downloaded.append(
            record.get_file(
                filepath, force, file_id, pattern, exclude_pattern, use_folder, pipe
            )
        )
    elif record_ids is not None:
        for record_id in record_ids:
            record = manager.record(id=int(record_id))
            files = record.get_file(
                filepath, force, file_id, pattern, exclude_pattern, use_folder, pipe
            )
            if files is not None:
                list_downloaded.extend(files)

    if pipe:
        manager.info(list_to_tokenlist(list_downloaded))


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "tag",
    char="t",
    required=True,
    description="Tag to add.",
    param_type=TokenList,
)
def add_tag(record, tag):
    """Add a tag or several tags to a record."""

    for i in tag:
        record.add_tag(i)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option("tag", char="t", required=True, description="Tag to remove.")
def remove_tag(record, tag):
    """Remove a tag from a record."""

    record.remove_tag(tag)


@records.command()
@apy_command
@id_identifier_options(class_type="record", keep_manager=True)
@id_identifier_options(
    class_type="record",
    name="link",
    helptext="to be linked.",
    allow_tokenlist=True,
)
@option("name", char="n", required=True, description="Name of the linking.")
@option(
    "term", char="t", required=False, description="An IRI specifying an existing term."
)
def add_record_link(manager, record, link, name, term, record_ids):
    """Add a record link to a record."""
    if link is not None:
        record.link_record(record_to=link, name=name, term_iri=term)
    elif record_ids is not None:
        for record_id in record_ids:
            record_link = manager.record(id=int(record_id))
            record.link_record(record_to=record_link, name=name, term_iri=term)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "record-link-id",
    char="l",
    required=True,
    description="Record link ID.",
    param_type=Integer,
)
def delete_record_link(record, record_link_id):
    """Delete a record link."""

    record.delete_record_link(record_link_id=record_link_id)


@records.command()
@apy_command
@id_identifier_options(
    class_type="record", helptext="to link to the collection.", keep_manager=True
)
@id_identifier_options(class_type="collection", helptext="to link to the record.")
def add_collection_link(record, collection):
    """Link record to a collection."""

    record.add_collection_link(collection)


@records.command()
@apy_command
@id_identifier_options(
    class_type="record", helptext="to remove collection.", keep_manager=True
)
@id_identifier_options(class_type="collection", helptext="to remove from the record.")
def remove_collection_link(record, collection):
    """Remove a record link from a collection."""

    record.remove_collection_link(collection)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@search_pagination_options
@option(
    "direction",
    char="d",
    description="Direction of the record links.",
    param_type=Choice(["in", "out"]),
    default="out",
)
def show_record_links_to(record, page, per_page, direction):
    """Print record links to another record."""

    record.get_record_links(page=page, per_page=per_page, direction=direction)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "name",
    char="n",
    required=True,
    description="Name of the metadatum. Nested values can be separated via '.'.",
    param_type=TokenList(separator="."),
)
@option(
    "information",
    char="i",
    description="Specify the information to print.",
    param_type=Choice(["value", "unit", "type"]),
    default="value",
)
@option(
    "pipe",
    char="p",
    description="Use this flag if you want to pipe the returned information.",
    is_flag=True,
)
def get_metadatum(record, name, information, pipe):
    """Print information of a specific metadatum."""

    record.get_metadatum(name, information=information, pipe=pipe)


@records.command()
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
@option(
    "mimetype",
    char="m",
    description="MIME type(s) for search.",
    param_type=TokenList,
    excludes=["user", "use-my-user-id"],
)
@option(
    "collection",
    char="c",
    description="Collection ID(s) to search in.",
    param_type=TokenList,
    excludes=["user", "use-my-user-id"],
)
@option(
    "child_collections",
    char="C",
    description="Include child collections in the search.",
    is_flag=True,
    excludes=["user", "use-my-user-id"],
)
@search_pagination_options
@user_id_options(
    helptext="to show the user's created records.", required=False, keep_manager=True
)
@option(
    "use-my-user-id",
    char="i",
    description="Show only own created records.",
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
def get_records(manager, user, use_my_user_id, **kwargs):
    """Search for records."""
    if kwargs["visibility"] == "all":
        kwargs["visibility"] = None

    manager.search.search_resources(
        "record", user=user, use_my_user_id=use_my_user_id, **kwargs
    )


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@file_id_options()
@option("name", char="a", description="The new name of the file.")
@option("mimetype", char="m", description="The new MIME type of the file.")
def edit_file(record, file_id, name, mimetype):
    """Edit the metadata of a file of a record."""

    record.edit_file(file_id, name, mimetype)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@file_id_options()
def delete_file(record, file_id):
    """Delete a file of a record."""

    record.delete_file(file_id)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "i-am-sure",
    description="Enable this option to delete all files of the record.",
    is_flag=True,
)
def delete_files(record, i_am_sure):
    """Delete all files of a record."""

    record.delete_files(i_am_sure)


@records.command()
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
    "mimetype", char="m", description="MIME type(s) for search.", param_type=TokenList
)
@option(
    "collection",
    char="c",
    description="Collection ID(s) to search in.",
    param_type=TokenList,
)
@option(
    "child_collections",
    char="C",
    description="Include child collections in the search.",
    is_flag=True,
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
    description="Use this flag if you want to pipe the returned"
    " record ids as tokenlist.",
    is_flag=True,
)
@option(
    "i-am-sure",
    description="Enable this option in case more than 1000 results are found.",
    is_flag=True,
)
def get_record_ids(manager, **kwargs):
    """Search for records. The ids of all found results are displayed."""
    if kwargs["visibility"] == "all":
        kwargs["visibility"] = None

    manager.search.search_resource_ids("record", **kwargs)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to export.", allow_tokenlist=True)
@option(
    "export-type",
    char="e",
    description="Export type.",
    default="json",
    param_type=Choice(["json", "pdf", "qr", "rdf", "ro-crate"]),
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
    " with the record's identifier as name and save the exported file in this folder.",
    is_flag=True,
    default=False,
)
def export(
    manager, record, export_type, path, name, force, pipe, use_folder, record_ids
):
    """Export the record using a specific export type."""
    if record is not None:
        record.export(export_type, path, name, force, pipe, use_folder)
    elif record_ids is not None:
        for record_id in record_ids:
            record = manager.record(id=record_id)
            record.export(export_type, path, name, force, pipe, use_folder)


@records.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to export.", allow_tokenlist=True)
@option(
    "export-type",
    char="e",
    description="Export type.",
    default="json",
    param_type=Choice(["json"]),
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
    " with the record's identifier as name and save the exported file in this folder.",
    is_flag=True,
    default=False,
)
def export_metadata(
    manager,
    record,
    export_type,
    path,
    name,
    force,
    pipe,
    use_folder,
    record_ids,
):
    """Export the extra metadata of a record."""
    if record is not None:
        record.export_metadata(export_type, path, name, force, pipe, use_folder)
    elif record_ids is not None:
        for record_id in record_ids:
            record = manager.record(id=record_id)
            record.export_metadata(export_type, path, name, force, pipe, use_folder)


@records.command()
@apy_command
@id_identifier_options(class_type="record")
@option(
    "record-link-id",
    char="l",
    required=True,
    description="Record link ID.",
    param_type=Integer,
)
@option("name", char="n", required=True, description="New name of the linking.")
def update_record_link(record, record_link_id, name):
    """Update the name of a record link."""

    record.update_record_link(record_link_id=record_link_id, name=name)
