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
import fnmatch
import json
import os
import pathlib
import sys

import click

from kadi_apy.cli.commons import BasicCLIMixin
from kadi_apy.cli.commons import DeleteItemCLIMixin
from kadi_apy.cli.commons import ExportCLIMixin
from kadi_apy.cli.commons import GroupRoleCLIMixin
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.cli.commons import TagCLIMixin
from kadi_apy.cli.commons import UserCLIMixin
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.resources.records import Record


def _rename_duplicate_entry(filepath_store, index):
    path = pathlib.Path(filepath_store)
    base = ""
    if len(path.parts) > 1:
        base = os.path.join(*path.parts[:-1])
    file_name = f"{path.stem}_{index}{path.suffix}"
    return os.path.join(base, file_name)


class CLIRecord(
    BasicCLIMixin,
    UserCLIMixin,
    GroupRoleCLIMixin,
    TagCLIMixin,
    DeleteItemCLIMixin,
    ExportCLIMixin,
    Record,
    RaiseRequestErrorMixin,
):
    """Records class to be used in a CLI.

    :param manager: See :class:`.Record`.
    :param id: See :class:`.Record`.
    :param identifier: See :class:`.Record`.
    :param skip_request: See :class:`.Record`.
    :param create: See :class:`.Record`.
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

    def _upload_file(self, file_path, file_description=None, force=False):
        """Prepare uploading files."""

        file_name = os.path.basename(file_path)

        self.info(f"Prepare upload of file '{file_name}'")

        response = super().upload_file(
            file_path=file_path, file_description=file_description, force=force
        )
        if response.status_code == 409 and not force:
            self.error(
                f"A file with the name '{file_name}' already exists.\n"
                f"File '{file_name} was not uploaded. Use '-f' to force overwriting"
                " existing file.",
            )
            sys.exit(1)
        elif response.status_code in (200, 201):
            self.info(f"Upload of file '{file_name}' was successful.")
        else:
            self.error(f"Upload of file '{file_name}' was not successful. ")
            self.raise_request_error(response)

    def upload_file(
        self,
        file_name,
        file_description=None,
        pattern=None,
        exclude_pattern=None,
        force=False,
    ):
        """Upload files into a record using the CLI.

        :param file_name: The path to the file (incl. name of the file) or folder.
        :type file_name: str
        :param file_description: The description of a single file.
        :type file_description: str, optional
        :param pattern: Pattern for selecting files matching certain pattern.
        :type pattern: str, optional
        :param exclude_pattern: Pattern for excluding files matching certain pattern.
        :type exclude_pattern: str, optional
        :param force: Whether to replace an existing file with identical name.
        :type force: bool, optional
        :raises KadiAPYRequestError: If request was not successful.
        """

        if not os.path.isdir(file_name):
            if not os.path.isfile(file_name):
                raise KadiAPYInputError(f"File: {file_name} does not exist.")

            self._upload_file(
                file_path=file_name, file_description=file_description, force=force
            )

        else:
            if file_description:
                raise KadiAPYInputError(
                    "The file description can only be applied on single file."
                )
            filelist = os.listdir(file_name)

            if pattern:
                filelist = fnmatch.filter(filelist, pattern)

            if exclude_pattern:
                i = 0
                while i < len(filelist):
                    if fnmatch.fnmatch(filelist[i], exclude_pattern):
                        del filelist[i]
                    else:
                        i += 1

            if not filelist:
                self.warning("Found no file to upload.")
                sys.exit(0)

            for file_upload in filelist:
                file_path = os.path.join(file_name, file_upload)

                if os.path.isdir(file_path):
                    continue

                self._upload_file(
                    file_path=file_path, file_description=file_description, force=force
                )

    def upload_string_to_file(
        self, string, file_name, file_description=None, force=False
    ):
        """Upload a string to save as a file in a record using the CLI.

        :param string: The string to save as a file.
        :type string: str
        :param file_name: The name under which the file should be stored.
        :type file_name: str
        :param file_description: The description of the file.
        :type file_description: str, optional
        :param force: Whether to replace an existing file with identical name.
        :type force: bool, optional
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().upload_string_to_file(
            string, file_name, file_description=file_description, force=force
        )
        if response.status_code in (200, 201):
            self.info(
                f"String was successfully stored as file '{file_name}' in {self}."
            )
        elif response.status_code == 409 and not force:
            self.error(
                f"A file with the name '{file_name}' already exists.\nFile"
                f" '{file_name}' was not updated. Use '-f' to force overwriting"
                " existing file."
            )
            sys.exit(1)
        else:
            self.error(f"Upload of string to file '{file_name}' was not successful.")
            self.raise_request_error(response)

    def add_metadatum(self, metadatum_new, force=False):
        """Add a metadatum to a record using the CLI.

        :param metadatum_new: The metadatum to add.
        :type metadatum_new: dict
        :param force: Whether to overwrite the metadatum with the new value in case the
            metadatum already exists.
        :type force: bool
        :raises KadiAPYRequestError: If request was not successful.
        """

        metadatum = metadatum_new["key"]
        try:
            unit = metadatum_new["unit"]
        except:
            unit = None
        value = metadatum_new["value"]

        if force is False and super().check_metadatum(metadatum):
            raise KadiAPYInputError(
                f"Metadatum '{metadatum}' already exists. Use '--force' to overwrite "
                "it or change the name."
            )

        metadata_before_update = self.meta["extras"]

        response = super().add_metadatum(metadatum_new, force)

        metadata_after_update = self.meta["extras"]

        if response.status_code == 200:
            if metadata_before_update == metadata_after_update:
                self.info("Metadata were not changed.")
            else:
                text_unit = ""
                if unit is not None:
                    text_unit = f"and the unit '{unit}' "
                self.info(
                    f"Successfully added metadatum '{metadatum}' with the value "
                    f"'{value}' {text_unit}to {self}."
                )
        else:
            self.info(
                f"Something went wrong when trying to add new metadatum '{metadatum}'"
                f" to {self}."
            )
            self.raise_request_error(response)

    def add_metadata(self, metadata=None, file=None, force=False):
        """Add metadata with dict or a list of dicts as input using the CLI.

        Either specify the metadata via a *file* to be read from or via *metadata*.

        :param metadata: One or more metadata entries to add, either as dictionary
            or a list of dictionaries.
        :type metadata: dict, list
        :param file: File path to read the metadata from.
        :type file: dict, list
        :param force: Whether to overwrite existing metadata with identical name.
        :type force: bool
        :raises KadiAPYRequestError: If request was not successful.
        """
        if (metadata is None and file is None) or (
            metadata is not None and file is not None
        ):
            raise KadiAPYInputError("Please specify either metadata or a file.")

        if file and not os.path.isfile(file):
            raise KadiAPYInputError(f"File: '{file}' does not exist.")

        try:
            if file:
                with open(file, encoding="utf-8") as f:
                    metadata = json.load(f)
            elif isinstance(metadata, list):
                pass
            else:
                metadata = json.loads(metadata)
        except json.JSONDecodeError as e:
            raise KadiAPYInputError(
                f"Error loading JSON input ({e}). \nA simple"
                " bash example to use as input could be"
                ' \'[{"key":"foo","type":"str","value":"bar"}]\'.'
            ) from e

        def _callback(metadatum, is_nested):
            metadatum_key = metadatum.get("key")

            if is_nested:
                self.info(
                    f"Metadatum {metadatum_key} is of type '{metadatum.get('type')}'"
                    " and will not be replaced."
                )
            else:
                metadatum_unit = metadatum.get("unit")
                text_unit = ""

                if metadatum_unit is not None:
                    text_unit = f"and the unit '{metadatum_unit}' "

                self.info(
                    f"Found metadatum '{metadatum_key}' with the value"
                    f" '{metadatum.get('value')}' {text_unit}to add to {self}."
                )

        metadata_before_update = self.meta["extras"]

        response = super().add_metadata(metadata, force, callback=_callback)

        metadata_after_update = self.meta["extras"]

        if response.status_code == 200:
            if metadata_before_update == metadata_after_update:
                self.info("Metadata were not changed.")
            else:
                self.info(f"Successfully updated the metadata of {self}.")
        else:
            self.info(
                f"Something went wrong when trying to add new metadata to {self}."
            )
            self.raise_request_error(response)

    def get_file(
        self,
        filepath,
        force=False,
        file_id=None,
        pattern=None,
        exclude_pattern=None,
        use_folder=False,
        pipe=False,
    ):
        """Download one file, all files or files matching a pattern from a record using
        the CLI.

        If a file ID is given, the specified file is download. Otherwise all files or
        all files matching the pattern are downloaded.

        :param filepath: The path to folder to store the file.
        :type filepath: str
        :param force: Whether to overwrite a file with identical name.
        :type force: bool, optional
        :param file_id: The file ID (UUID) of a file to download.
        :type file_id: bool, optional
        :param pattern: Pattern for selecting files matching certain pattern.
        :type pattern: str, optional
        :param exclude_pattern: Pattern for selecting files matching certain pattern.
        :type exclude_pattern: str, optional
        :param use_folder: Flag indicating if the a folder with the name of the
            records's identifier should be created within given *filepath*. The
            downloaded file(s) are stored in this folder.
        :type use_folder: bool, optional
        :return: A list of downloaded files with file path.
        :type: list
        :raises KadiAPYRequestError: If request was not successful.
        """

        if file_id is not None and pattern is not None:
            self.error(
                "Please specific either a file to download or a pattern.",
            )
            sys.exit(1)

        list_file_ids = []
        list_file_names = []

        if file_id is not None:
            try:
                list_file_names.append(super().get_file_name(file_id))
            except KadiAPYInputError as e:
                self.error(e, err=True)
                sys.exit(1)

            list_file_ids.append(file_id)

        else:
            page = 1
            response = super().get_filelist(page=page, per_page=100)

            if response.status_code == 200:
                payload = response.json()
                total_pages = payload["_pagination"]["total_pages"]
                for page in range(1, total_pages + 1):
                    if page != 1:
                        response = super().get_filelist(page=page, per_page=100)
                        payload = response.json()

                    for results in payload["items"]:
                        list_file_ids.append(results["id"])
                        list_file_names.append(results["name"])
            else:
                self.raise_request_error(response)

            if pattern:
                i = 0
                while i < len(list_file_names):
                    if not fnmatch.fnmatch(list_file_names[i], pattern):
                        del list_file_names[i]
                        del list_file_ids[i]
                    else:
                        i += 1

            if exclude_pattern:
                i = 0
                while i < len(list_file_names):
                    if fnmatch.fnmatch(list_file_names[i], exclude_pattern):
                        del list_file_names[i]
                        del list_file_ids[i]
                    else:
                        i += 1

            number_files = len(list_file_ids)

            if not pipe:
                if number_files == 0:
                    if pattern:
                        self.info(
                            f"No files present in {self} matching pattern '{pattern}'."
                        )
                    else:
                        self.info(f"No files present in {self}.")
                    return

                self.info(f"Starting to download {number_files} file(s) from {self}.")

        list_downloaded = []

        for name_iter, id_iter in zip(list_file_names, list_file_ids):
            if use_folder:
                identifier = self.meta["identifier"]
                filepath_store = os.path.join(filepath, identifier, name_iter)
                try:
                    os.mkdir(os.path.join(filepath, identifier))
                except FileExistsError:
                    pass
            else:
                filepath_store = os.path.join(filepath, name_iter)

            index = 2
            filepath_temp = filepath_store

            if force:
                while filepath_temp in list_downloaded:
                    filepath_temp = _rename_duplicate_entry(filepath_store, index)
                    index += 1

                list_downloaded.append(filepath_temp)

            else:
                while os.path.isfile(filepath_temp):
                    filepath_temp = _rename_duplicate_entry(filepath_store, index)
                    index += 1

                list_downloaded.append(filepath_temp)

            response = super().download_file(id_iter, filepath_temp)

            if response.status_code == 200:
                if not pipe:
                    self.info(
                        f"Successfully downloaded file '{name_iter}' from {self} and "
                        f"stored in '{filepath_temp}'."
                    )
            else:
                if not pipe:
                    self.info(
                        f"Something went wrong when trying to download file"
                        f" '{name_iter}' from {self}."
                    )
                self.raise_request_error(response)

        return list_downloaded

    def link_record(self, record_to, name, term_iri=None):
        """Add a record link to a record using the CLI.

        :param record_to: The  record to link.
        :type record_to: record
        :param name: The name of the link.
        :type name: str
        :param term_iri: An IRI specifying an existing term that the link should
            represent.
        :type term_iri: str
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().link_record(
            record_to=record_to.id, name=name, term_iri=term_iri
        )

        if response.status_code == 409:
            self.info("Link already exists. Nothing to do.")
            return
        if response.status_code == 201:
            self.info(f"Successfully linked {self} to {record_to}.")
        else:
            self.raise_request_error(response)

    def delete_record_link(self, record_link_id):
        """Delete a record link using the CLI.

        :param record_link_id: The ID of the record link to delete. Attention: The
            record link ID is not the record ID.
        :type record_link_id: int
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().delete_record_link(record_link_id=record_link_id)
        if response.status_code == 204:
            self.info(
                f"Linking of record {self.id} with link id {record_link_id} was "
                "deleted."
            )
        else:
            self.raise_request_error(response)

    def get_record_links(self, page, per_page, direction):
        """Print record links to another record using the CLI.

        :param page: Page of the search request.
        :type page: int
        :param per_page: Number of results per page.
        :type per_page: int
        :param direction: Specify whether to print incoming or outcoming links
        :type direction: str
        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        response = super().get_record_links(
            page=page, per_page=per_page, direction=direction
        )
        if response.status_code == 200:
            payload = response.json()
            self.info(
                f"Found {payload['_pagination']['total_items']} record(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {page}:"
            )
            if direction == "in":
                record_direction = "record_from"
            else:
                record_direction = "record_to"

            for results in payload["items"]:
                self.info(
                    f"Link id '{results['id']}': Link name: '{results['name']}'."
                    f" {self} is linked with record"
                    f" '{results[record_direction]['title']}'"
                    f" (id: {results[record_direction]['id']}, identifier:"
                    f" '{results[record_direction]['identifier']}) via direction"
                    f" '{direction}''."
                )
        else:
            self.raise_request_error(response)

    def get_metadatum(self, name, information="value", pipe=False):
        """Print information of a specific metadatum using the CLI.

        :param name: See :meth:`.Record.get_metadatum`.
        :type name: str or list
        :param information: The information of the metadatum to print.
        :type information: str, optional
        :param pipe: Whether to only print the result for piping.
        :type pipe: bool
        :raises KadiAPYRequestError: If request was not successful.
        """
        keys = name if isinstance(name, list) else [name]

        result = super().get_metadatum(keys)

        if result is None:
            self.error(
                f"Metadatum '{'.'.join(keys)}' is not present in {self}.", err=True
            )
            sys.exit(1)

        if information not in result:
            self.error(
                f"The value for '{information}' is not present in metadatum"
                f" '{'.'.join(keys)}'.",
                err=True,
            )
            sys.exit(1)

        result = result[information]

        if pipe:
            self.info(result)
        else:
            self.info(
                f"The metadatum '{'.'.join(keys)}' has the {information} '{result}'."
            )

    def edit_file(self, file, name, mimetype):
        """Edit the metadata of a file of a record using the CLI.

        :param file: The ID (UUID) of the file to edit.
        :type file: str
        :param name: The new name of the file.
        :type name: str
        :param mimetype: The new mimetype of the file.
        :type mimetype: str
        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        if name is not None and self.has_file(name):
            self.error(f"File {name} already present in {self}.")
            sys.exit(1)

        response = super().edit_file(file, name=name, mimetype=mimetype)
        if response.status_code != 200:
            self.raise_request_error(response)
        else:
            self.info("File updated successfully.")

    def delete_file(self, file_id):
        r"""Delete a file of the record using the CLI.

        :param file_id: The ID (UUID) of the file to delete.
        :type file_id: str
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().delete_file(file_id)
        if response.status_code != 204:
            self.raise_request_error(response)
        else:
            self.info("File deleted successfully.")

    def delete_files(self, i_am_sure=False):
        """Delete all files of a record using the CLI.

        :param i_am_sure: Flag which has to set to ``True`` to delete all files.
        :type i_am_sure: bool
        :raises  KadiAPYInputError: If i_am_sure is not ``True``.
        :raises KadiAPYRequestError: If request was not successful.
        """

        if not i_am_sure:
            raise KadiAPYInputError(
                f"If you are sure you want to delete all files in {self}, "
                "use the flag --i-am-sure."
            )

        response = super().get_filelist(page=1, per_page=100)

        if response.status_code == 200:
            payload = response.json()
            total_pages = payload["_pagination"]["total_pages"]
            for page in range(1, total_pages + 1):
                for results in payload["items"]:
                    response_delete = super().delete_file(results["id"])
                    if response_delete.status_code != 204:
                        self.raise_request_error(response_delete)
                    else:
                        self.info(f"Deleting file {results['name']} was successful.")
                if page < total_pages:
                    response = super().get_filelist(page=1, per_page=100)
                    if response.status_code == 200:
                        payload = response.json()
                    else:
                        self.raise_request_error(response)

        else:
            self.raise_request_error(response)

    def remove_metadatum(self, metadatum):
        """Delete a metadatum of a record using the CLI.

        Only first level metadata are supported (no nested types).

        :param metadatum: The metadatum to remove.
        :type metadatum: str
        :raises KadiAPYRequestError: If request was not successful.
        """

        if super().check_metadatum(metadatum):
            response = super().remove_metadatum(metadatum)
            if response.status_code == 200:
                self.info(f"Successfully removed metadatum '{metadatum}' from {self}.")
            else:
                self.info(
                    f"Something went wrong when trying to remove metadatum "
                    f"'{metadatum}' from {self}."
                )
                self.raise_request_error(response)
        else:
            self.info(
                f"Metadatum '{metadatum}' is not present in {self}. Nothing to do."
            )

    def remove_all_metadata(self, i_am_sure=False):
        """Remove all metadata from a record.

        :param i_am_sure: Flag which has to set to ``True`` to remove all metadata.
        :type i_am_sure: bool
        :raises KadiAPYRequestError: If request was not successful.
        """
        if not i_am_sure:
            raise KadiAPYInputError(
                f"If you are sure you want to delete all metadata in {self}, "
                "use the flag --i-am-sure."
            )

        response = super().remove_all_metadata()
        if response.status_code == 200:
            self.info(f"Successfully removed all metadata from {self}.")
        else:
            self.raise_request_error(response)

    def add_collection_link(self, collection):
        """Add a record to a collection using the CLI.

        :param collection: The collection to which the record should be added.
        :type collection: Collection
        :raises KadiAPYRequestError: If request was not successful.
        """
        response = super().add_collection_link(collection_id=collection.id)

        if response.status_code == 201:
            self.info(f"Successfully linked {self} to {collection}.")
        elif response.status_code == 409:
            self.info(
                f"Link from {collection} to {self} already exists. Nothing to do."
            )
        else:
            self.info(f"Linking {collection} to {self} was not successful.")
            self.raise_request_error(response)

    def remove_collection_link(self, collection):
        """Remove a record from a collection using the CLI.

        :param collection: The collection from which the record should be removed.
        :type collection: Collection
        :raises KadiAPYRequestError: If request was not successful.
        """
        response = super().remove_collection_link(collection_id=collection.id)

        if response.status_code == 204:
            self.info(f"Successfully removed {self} from {collection}.")
        else:
            self.error(f"Removing {self} from {collection} was not successful.")
            self.raise_request_error(response)

    def update_record_link(self, record_link_id, name):
        """Update the name of a record link using the CLI.

        :param record_link_id: The ID of the record link to update. Attention: The
            record link ID is not the record ID.
        :type record_link_id: int
        :param name: The name of the link.
        :type name: str
        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        response = super().update_record_link(record_link_id, name=name)

        if response.status_code == 409:
            self.info("Identical link already exists.")
        elif response.status_code == 200:
            self.info(f"Successfully updated name of record link {record_link_id}.")
        else:
            self.error("Updating of record link was not successful.")

    def print_info(self, pipe=False, **kwargs):
        r"""Print infos of a record using the CLI.

        :param \**kwargs: Specify additional infos to print.
        :raises: KadiAPYRequestError: If request was not successful
        """
        super().print_info(pipe=pipe, **kwargs)

        if kwargs.get("filelist", False):
            response = self.get_filelist(
                page=kwargs.get("page"), per_page=kwargs.get("per_page")
            )
            if response.status_code == 200:
                payload = response.json()
                click.echo(
                    f"Found {payload['_pagination']['total_items']} file(s) on "
                    f"{payload['_pagination']['total_pages']} page(s).\n"
                    f"Showing results of page {kwargs['page']}:"
                )
                for results in payload["items"]:
                    click.echo(
                        f"Found file '{results['name']}' with id" f" '{results['id']}'."
                    )
            else:
                self.raise_request_error(response)

        if kwargs.get("metadata", False):
            if not pipe:
                self.info("Metadata:")

                list_metadata = self.flatten_extras()

                for metadata in list_metadata:
                    metadatum = metadata["key"]
                    value = metadata["value"]
                    if "unit" in metadata:
                        unit = f" and unit '{metadata['unit']}'."
                    else:
                        unit = "."

                    self.info(
                        f"Found metadatum '{metadatum}' with value" f" '{value}'{unit}"
                    )
            else:
                self.info(
                    json.dumps(
                        self.meta["extras"],
                        indent=2,
                        sort_keys=True,
                        ensure_ascii=False,
                    )
                )

    def export_metadata(
        self,
        export_type,
        path=".",
        name=None,
        force=False,
        pipe=False,
        use_folder=False,
        **params,
    ):
        r"""Export the extra metadata of a record using the CLI.

        :param export_type: The export format.
        :type export_type: str
        :param path: The path to store.
        :type path: str, optional
        :param name: The name of the file. The identifier is used as default.
        :type name: str, optional
        :param force: Whether to replace an existing file with identical name.
        :type force: bool, optional
        :param pipe: Flag to indicate if json should be piped.
        :type pipe: bool, optional
        :param use_folder: Flag indicating if the a folder with the name of the
            resource's identifier should be created within given *path*. The
            exported file is stored in this folder.
        :param \**params: Additional query parameters.
        :raises KadiAPYInputError: If export type is invalid or if not json is used as
            input type together with pipe.
        :raises KadiAPYRequestError: If request was not successful.
        """
        if not pipe:
            if name is None:
                name = self.meta["identifier"]

            if use_folder:
                identifier = self.meta["identifier"]
                path = os.path.join(path, identifier)
                try:
                    os.mkdir(path)
                except FileExistsError:
                    pass

            path = os.path.join(path, name)

            if export_type != "json":
                raise KadiAPYInputError(f"Export type '{export_type}' is invalid.")

            if not path.endswith(".json"):
                path = f"{path}.json"

            if os.path.isfile(path) and not force:
                self.error(
                    f"A file with the name '{path}' already exists. \nFile"
                    f" '{path}' was not replaced. Use '-f' to force overwriting"
                    " existing file."
                )
                sys.exit(1)

        response = super().export_metadata(path, export_type, pipe, **params)

        if response.status_code == 200:
            self.info(
                f"Successfully exported {self} as {export_type} and"
                f" stored in '{path}'."
            )
        else:
            self.error(f"Something went wrong when trying to export the {self}.")
            self.raise_request_error(response)
