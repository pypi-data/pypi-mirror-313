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
import click
from xmlhelpy import Choice
from xmlhelpy import Path
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import search_pagination_options
from kadi_apy.cli.main import kadi_apy
from kadi_apy.globals import RESOURCE_TYPES
from kadi_apy.lib.helper import get_resource_type


@kadi_apy.group()
def misc():
    """Commands for miscellaneous functionality."""


@misc.command()
@apy_command
@search_pagination_options
@option(
    "filter",
    char="f",
    description="Filter by title or identifier.",
    default="",
)
def get_deleted_resources(manager, **kwargs):
    """Show a list of deleted resources in the trash."""

    manager.misc.get_deleted_resources(**kwargs)


@misc.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Type of the resource to restore.",
    param_type=Choice(RESOURCE_TYPES),
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the resource to restore.",
    required=True,
)
def restore_resource(manager, item_type, item_id):
    """Restore a resource from the trash."""

    item = get_resource_type(item_type)

    manager.misc.restore(item=item, item_id=item_id)


@misc.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Type of the resource to purge.",
    param_type=Choice(RESOURCE_TYPES),
    required=True,
)
@option(
    "item-id",
    char="i",
    description="ID of the resource to purge.",
    required=True,
)
def purge_resource(manager, item_type, item_id):
    """Purge a resource from the trash."""

    item = get_resource_type(item_type)

    manager.misc.purge(item=item, item_id=item_id)


@misc.command()
@apy_command
@search_pagination_options
@option(
    "filter",
    char="f",
    description="Filter.",
    default="",
)
def get_licenses(manager, **kwargs):
    """Show a list available licenses."""

    manager.misc.get_licenses(**kwargs)


@misc.command()
@apy_command
@option(
    "item-type",
    char="t",
    description="Show only roles of this resource.",
    param_type=Choice(["record", "collection", "template", "group"]),
)
def get_roles(manager, item_type):
    """Show a list of roles and corresponding permissions of all resources."""

    manager.misc.get_roles(item_type)


@misc.command()
@apy_command
@search_pagination_options
@option(
    "filter",
    char="f",
    description="Filter.",
    default="",
)
@option(
    "type",
    char="t",
    description="A resource type to limit the tags to.",
    default=None,
    param_type=Choice(["record", "collection"]),
)
def get_tags(manager, **kwargs):
    """Show a list available tags."""

    manager.misc.get_tags(**kwargs)


@misc.command()
@apy_command(use_kadi_manager=True)
@option(
    "path",
    char="p",
    description="Path of the ELN file to import.",
    param_type=Path(exists=True, path_type="file"),
    required=True,
)
def import_eln(manager, path):
    """Import an RO-Crate file following the "ELN" file specification."""
    manager.misc.import_eln(path)

    click.echo("File has been imported successfully.")


@misc.command()
@apy_command(use_kadi_manager=True)
@option(
    "path",
    char="p",
    description="Path of the JSON Schema file to import.",
    param_type=Path(exists=True, path_type="file"),
    required=True,
)
@option(
    "type",
    char="y",
    description="Type of the template to create from JSON Schema.",
    param_type=Choice(["extras", "record"]),
    default="extras",
    var_name="template_type",
)
def import_json_schema(manager, path, template_type):
    """Import JSON Schema file and create a template."""
    manager.misc.import_json_schema(path, template_type)

    click.echo("File has been imported successfully.")


@misc.command()
@apy_command(use_kadi_manager=True)
@option(
    "path",
    char="p",
    description="Path of the SHACl file to import.",
    param_type=Path(exists=True, path_type="file"),
    required=True,
)
@option(
    "type",
    char="y",
    description="Type of the template to create from SHACL shapes.",
    param_type=Choice(["extras", "record"]),
    default="extras",
    var_name="template_type",
)
def import_shacl(manager, path, template_type):
    """Import SHACL file and create a template."""
    manager.misc.import_shacl(path, template_type)

    click.echo("File has been imported successfully.")
