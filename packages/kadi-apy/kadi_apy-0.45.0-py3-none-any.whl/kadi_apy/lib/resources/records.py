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
import copy
import json
import os
import time
from io import BytesIO

import click

from kadi_apy.lib.commons import ExportMixin
from kadi_apy.lib.commons import PermissionMixin
from kadi_apy.lib.commons import TagMixin
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.helper import chunked_response
from kadi_apy.lib.resource import Resource


def _remove_key(list, key_remove):
    return [obj for obj in list if obj["key"] != key_remove]


def _flatten_extras(extras, separator, key_prefix=""):
    flat_extras = []

    for index, extra in enumerate(extras):
        if extra["type"] in ["dict", "list"]:
            flat_extras += _flatten_extras(
                extra["value"],
                separator,
                key_prefix=f"{key_prefix}{extra.get('key', index + 1)}{separator}",
            )
        else:
            new_extra = copy.deepcopy(extra)

            if "key" in extra:
                new_extra["key"] = f"{key_prefix}{extra['key']}"
            else:
                new_extra["key"] = f"{key_prefix}{index + 1}"

            flat_extras.append(new_extra)

    return flat_extras


def _progress_bar(item, iterable, **kwargs):
    """Function which returns either click progress bar or a custom iterable."""

    class Iterable:
        """Custom iterable."""

        def __init__(self, iterable=None):
            self.iterable = iterable

        def __enter__(self):
            return self.iterable

        def __exit__(self, *args):
            pass

    if item.is_verbose():
        return click.progressbar(iterable, **kwargs)

    return Iterable(iterable)


class Record(Resource, ExportMixin, PermissionMixin, TagMixin):
    r"""Model to represent records.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    :param id: The ID of an existing resource.
    :type id: int, optional
    :param identifier: The unique identifier of a new or existing resource,
        which is only relevant if no ID was given. If present, the identifier will be
        used to check for an existing resource instead. If no existing resource could be
        found or the resource to check does not use a unique identifier, it will be used
        to create a new resource instead, together with the additional metadata. The
        identifier is adjusted if it contains spaces, invalid characters or exceeds the
        length of 50 valid characters.
    :type identifier: str, optional
    :param skip_request: Flag to skip the initial request.
    :type skip_request: bool, optional
    :param create: Flag to determine if a resource should be created in case
        a identifier is given and the resource does not exist.
    :type create: bool, optional
    :param \**kwargs: Additional metadata of the new resource to create.
    """

    base_path = "/records"
    name = "record"

    def add_collection_link(self, collection_id):
        """Add a record to a collection.

        :param collection_id: The ID of the collection to which the record should be
            added.
        :type collection_id: int
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/collections"
        data = {"id": collection_id}

        return self._post(endpoint, json=data)

    def remove_collection_link(self, collection_id):
        """Remove a record from a collection.

        :param collection_id: The ID of the collection from which the record should be
            removed.
        :type collection_id: int
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/collections/{collection_id}"
        return self._delete(endpoint, json=None)

    def check_metadatum(self, metadatum):
        """Check if a record has a certain metadatum.

        Does currently not support metadata in nested types.

        :param metadatum: The metadatum to check.
        :type metadatum: str
        :return: ``True`` if the metadatum exists, otherwise ``False``.
        :rtype: bool
        """

        for obj in self.meta["extras"]:
            if obj["key"] == metadatum:
                return True
        return False

    def add_metadatum(self, metadatum, force=False):
        """Add metadatum to a record.

        Validation supports currently no nested metadata.

        :param metadatum: The metadatum to add.
        :type metadatum: dict
        :param force: Whether to overwrite the metadatum with the new value in case the
            metadatum already exists.
        :type force: bool
        :return: The response object.
        """

        endpoint = self._actions["edit"]
        metadata = copy.deepcopy(self.meta["extras"])

        metadatum_key = metadatum.get("key")

        if self.check_metadatum(metadatum_key):
            if force:
                metadata = [obj for obj in metadata if obj["key"] != metadatum_key]
                metadata.append(metadatum)
        else:
            metadata.append(metadatum)

        return self._patch(endpoint, json={"extras": metadata})

    def add_metadata(self, metadata_new, force=False, callback=None):
        r"""Add metadata to a record.

        Validation supports currently no nested metadata.

        :param metadata_new: One or more metadata entries to add, either as dictionary
            or a list of dictionaries.
        :type metadata_new: dict, list
        :param force: Whether to overwrite the metadatum with the new value in case the
            metadatum already exists.
        :type force: bool
        :param callback: Callback function.
        :type callback: optional
        :return: The response object.
        """
        if not isinstance(metadata_new, list):
            metadata_new = [metadata_new]

        metadata_old = copy.deepcopy(self.meta["extras"])

        for metadatum_new in metadata_new:
            found = False

            for metadatum_old in metadata_old:
                if metadatum_new.get("key") == metadatum_old["key"]:
                    found = True

                    if force:
                        if metadatum_old["type"] in ["dict", "list"]:
                            metadata_new = _remove_key(
                                metadata_new, metadatum_old["key"]
                            )
                            if callback:
                                callback(metadatum_old, True)
                        else:
                            metadata_old = _remove_key(
                                metadata_old, metadatum_old["key"]
                            )
                            if callback:
                                callback(metadatum_new, False)
                    else:
                        metadata_new = _remove_key(metadata_new, metadatum_old["key"])

            if callback and not found:
                callback(metadatum_new, False)

        return self._patch(
            self._actions["edit"], json={"extras": metadata_old + metadata_new}
        )

    def remove_metadatum(self, metadatum):
        """Remove a metadatum from a record.

        Only first level metadata are supported (no nested types).

        :param metadatum: The metadatum to remove.
        :type metadatum: str
        :return: The response object.
        """

        metadata = [obj for obj in self.meta["extras"] if obj["key"] != metadatum]
        return self._patch(self._actions["edit"], json={"extras": metadata})

    def remove_all_metadata(self):
        """Remove all metadata from a record.

        :return: The response object.
        """

        return self._patch(self._actions["edit"], json={"extras": []})

    def _initiate_upload(
        self, file_name, file_size, file_description=None, force=False
    ):
        file_metadata = {
            "name": file_name,
            "size": file_size,
        }

        if file_description is not None:
            file_metadata["description"] = file_description

        endpoint = self._actions["new_upload"]
        response = self._post(endpoint, json=file_metadata)

        if response.status_code == 409 and force:
            del file_metadata["name"]

            endpoint = response.json()["file"]["_actions"]["edit_data"]
            response = self._put(endpoint, json=file_metadata)

        return response

    def _upload_data(self, file, upload_meta):
        upload_type = upload_meta["upload_type"]
        endpoint = upload_meta["_actions"]["upload_data"]

        if upload_type == "direct":
            return self._put(endpoint, data=file)

        chunk_count = upload_meta["chunk_count"]
        chunk_size = upload_meta["_meta"]["chunk_size"]

        # Upload the file chunks.
        with _progress_bar(self, range(chunk_count)) as iterable_bar:
            for i in iterable_bar:
                chunk_data = file.read(chunk_size)
                headers = {
                    "Kadi-Chunk-Index": str(i),
                    "Kadi-Chunk-Size": str(len(chunk_data)),
                }

                response = self._put(endpoint, data=chunk_data, headers=headers)

                if response.status_code != 200:
                    return response

        # Finish the upload.
        endpoint = response.json()["_actions"]["finish"]
        response = self._post(endpoint)

        if response.status_code != 202:
            return response

        # Wait for the upload to process.
        endpoint = response.json()["_links"]["self"]
        delay = 0.1

        time.sleep(delay)

        while True:
            response = self._get(endpoint)

            if response.status_code == 200:
                task_meta = response.json()["_meta"]["task"]

                if "file" in task_meta or "error" in task_meta:
                    break
            else:
                break

            time.sleep(delay)

            if delay < 10:
                delay += 1

        return response

    def upload_file(
        self,
        file_path,
        file_name=None,
        file_description=None,
        force=False,
    ):
        """Upload a file to a record.

        :param file_path: The path to the file (incl. name of the file).
        :type file_path: str
        :param file_name: The name under which the file should be stored. If no name is
            given, the name is taken from the file path.
        :type file_name: str, optional
        :param file_description: The description of the file.
        :type file_description: str, optional
        :param force: Whether to replace an existing file with identical name.
        :type force: bool, optional
        :return: The final response object of the upload process.
        """
        file_name = os.path.basename(file_path) if file_name is None else file_name
        file_size = os.path.getsize(file_path)

        response = self._initiate_upload(
            file_name, file_size, file_description=file_description, force=force
        )

        if response.status_code != 201:
            return response

        with open(file_path, "rb") as f:
            return self._upload_data(f, response.json())

    def upload_string_to_file(
        self, string, file_name, file_description=None, force=False
    ):
        """Upload a string to save as a file in a record.

        :param string: The string to save as a file.
        :type string: str
        :param file_name: The name under which the file should be stored.
        :type file_name: str
        :param file_description: The description of the file.
        :type file_description: str, optional
        :param force: Whether to replace an existing file with identical name.
        :type force: bool, optional
        :return: The final response object of the upload process.
        """
        mem = BytesIO(string.encode())
        file_size = mem.getbuffer().nbytes

        response = self._initiate_upload(
            file_name, file_size, file_description=file_description, force=force
        )

        if response.status_code != 201:
            return response

        return self._upload_data(mem, response.json())

    def download_file(self, file_id, file_path):
        """Download a file of a record.

        :param file_id: The file ID of the file to download.
        :type file_id: str
        :param file_path: The full path to store the file.
        :type file_path: str
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/files/{file_id}/download"
        response = self._get(endpoint, stream=True)

        if response.status_code == 200:
            chunked_response(file_path, response)

        return response

    def download_all_files(self, file_path):
        """Download all files of a record as ZIP archive.

        :param file_path: The full path to store the archive.
        :type file_path: str
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/files/download"
        response = self._get(endpoint, stream=True)

        if response.status_code == 200:
            chunked_response(file_path, response)

        return response

    def get_file_revisions(self, **params):
        r"""Get the file revisions of a file in this record.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/files/revisions"
        return self._get(endpoint, params=params)

    def get_file_revision(self, revision_id, **params):
        r"""Get a specific file revision of a file in this record.

        :param revision_id: The revision ID of the file.
        :type revision_id: int
        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/files/revisions/{revision_id}"
        return self._get(endpoint, params=params)

    def get_record_revisions(self, **params):
        r"""Get the revisions of this record.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions"
        return self._get(endpoint, params=params)

    def get_record_revision(self, revision_id, **params):
        r"""Get a specific revision of this record.

        :param revision_id: The revision ID of the record.
        :type revision_id: int
        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions/{revision_id}"
        return self._get(endpoint, params=params)

    def get_users(self, **params):
        r"""Get users from a record. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/users"
        return self._get(endpoint, params=params)

    def get_groups(self, **params):
        r"""Get group roles from a record. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/groups"
        return self._get(endpoint, params=params)

    def get_filelist(self, **params):
        r"""Get the filelist. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/files"
        return self._get(endpoint, params=params)

    def get_number_files(self):
        """Get number of all files of a record.

        :return: The number of files.
        :rtype: int
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = self.get_filelist()
        if response.status_code == 200:
            payload = response.json()
            return payload["_pagination"]["total_items"]
        raise KadiAPYRequestError(response.json())

    def get_file_name(self, file_id):
        """Get file name from a given file ID.

        :param file_id: The ID of the file.
        :type group_id: str
        :return: The name of the file.
        :rtype: str
        :raises KadiAPYInputError: If no file with the given file ID exists.
        """

        endpoint = f"{self.base_path}/{self.id}/files/{file_id}"
        response = self._get(endpoint)
        if response.status_code == 200:
            return response.json()["name"]

        raise KadiAPYInputError(f"No file with id {file_id} in {self}.")

    def get_metadatum(self, name):
        """Return a specific metadatum.

        :param name: Either a single key as a string or a list of strings for nested
            metadata. Note that for list values, the keys are replaced by corresponding
            indices, also as string, starting at 1.
        :type name: str or list
        :return: The metadatum or ``None`` if it could not be found.
        """
        keys = name if isinstance(name, list) else [name]

        # The current list of extras to search.
        current_extras = self.meta["extras"]
        # The current extra that was found based on the keys to search, which may or may
        # not represent the result yet.
        current_extra = None
        # The type of the nested extra we are currently in, which is relevant for nested
        # extras.
        nested_type = None

        for i, key in enumerate(keys):
            if nested_type == "list":
                try:
                    index = int(key)
                except ValueError:
                    return None

                if index < 1 or index > len(current_extras):
                    return None

                current_extra = current_extras[index - 1]
            else:
                try:
                    # Due to using a generator expression, the iteration stops once a
                    # match is found.
                    current_extra = next(
                        extra for extra in current_extras if extra["key"] == key
                    )
                except StopIteration:
                    return None

            current_extras = current_extra["value"]
            nested_type = current_extra["type"]

            # Did not find all keys yet, but cannot continue the search.
            if i < len(keys) - 1 and not isinstance(current_extras, list):
                return None

        return current_extra

    def link_record(self, record_to, name, term_iri=None):
        """Link record.

        :param record_to: The ID of the record to link.
        :type record_to: int
        :param name: The name of the link.
        :type name: str
        :param term_iri: An IRI specifying an existing term that the link should
            represent.
        :type term_iri: str
        :return: The response object.
        """

        endpoint = self._actions["link_record"]
        data = {"record_to": {"id": record_to}, "name": name, "term": term_iri}
        return self._post(endpoint, json=data)

    def delete_record_link(self, record_link_id):
        """Delete a record link.

        :param record_link_id: The ID of the record link to delete. Attention: The
            record link ID is not the record ID.
        :type record_link_id: int
        :return: The response object.
        """

        return self._delete(f"{self.base_path}/{self.id}/records/{record_link_id}")

    def update_record_link(self, record_link_id, **kwargs):
        r"""Update the name of record link.

        :param record_link_id: The ID of the record link to update. Attention: The
            record link ID is not the record ID.
        :type record_link_id: int
        :param \**kwargs: The metadata to update the record link with.
        :return: The response object.
        """

        return self._patch(
            f"{self.base_path}/{self.id}/records/{record_link_id}", json=kwargs
        )

    def get_record_links(self, **params):
        r"""Get record links. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/records"
        return self._get(endpoint, params=params)

    def get_collection_links(self, **params):
        r"""Get collection links. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/collections"
        return self._get(endpoint, params=params)

    def get_file_id(self, file_name):
        """Get the file ID based on the file name.

        :param file_name: The name of the file.
        :type file_name: str
        :return: The file ID (UUID).
        :rtype: str
        :raises KadiAPYInputError: If no file with the given name exists.
        """

        response = self._get(f"{self.base_path}/{self.id}/files/name/{file_name}")

        if response.status_code == 200:
            return response.json()["id"]

        raise KadiAPYInputError(f"No file with name {file_name} in {self}.")

    def get_file_info(self, file_id):
        """Get information of a file based on the file_id.

        :param file_id: The ID of the file.
        :type file_id: str
        :return: The response object.
        """

        return self._get(f"{self.base_path}/{self.id}/files/{file_id}")

    def has_file(self, file_name):
        """Check if file with the given name already exists.

        :param file_name: The name of the file.
        :type file_name: str
        :return: ``True`` if file already exists, otherwise ``False``.
        """

        try:
            self.get_file_id(file_name)
            return True
        except:
            return False

    def edit_file(self, file_id, **kwargs):
        r"""Edit the metadata of a file of the record.

        :param file_id: The ID (UUID) of the file to edit.
        :type file_id: str
        :param \**kwargs: The metadata to update the file with.
        :return: The response object.
        """

        kwargs = {key: value for key, value in kwargs.items() if value is not None}

        return self._patch(f"{self.base_path}/{self.id}/files/{file_id}", json=kwargs)

    def delete_file(self, file_id):
        r"""Delete a file of the record.

        :param file_id: The ID (UUID) of the file to delete.
        :type file_id: str
        :return: The response object.
        """

        return self._delete(f"{self.base_path}/{self.id}/files/{file_id}")

    def flatten_extras(self, separator="."):
        r"""Create a list of flattened metadata.

        :param separator: A string for separating the metadata.
        :type separator: str, optional
        :return: A list of flattened metadata.
        :rtype: list
        """

        return _flatten_extras(self.meta["extras"], separator, key_prefix="")

    def export_metadata(self, path, export_type="json", pipe=False, **params):
        r"""Export the extra metadata of a record.

        :param path: The path (including name of the file) to store the exported data.
        :type path: str
        :param export_type: The export format.
        :type export_type: str
        :param pipe: If ``True``, nothing is written here.
        :type pipe: bool
        :param \**params: Additional query parameters.
        :return: The response object.
        :raises KadiAPYInputError: If export type is invalid.
        """
        if export_type != "json":
            raise KadiAPYInputError(f"Export type '{export_type}' is invalid.")

        if isinstance(params.get("filter"), dict):
            params["filter"] = json.dumps(params["filter"])

        response = self._get(
            f"{self.base_path}/{self.id}/extras/export/{export_type}", params=params
        )

        if not pipe and response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)

        return response
