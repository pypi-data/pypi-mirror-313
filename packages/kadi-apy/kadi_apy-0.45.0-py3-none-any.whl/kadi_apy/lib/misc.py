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
from kadi_apy.lib.helper import RequestMixin
from kadi_apy.lib.helper import VerboseMixin
from kadi_apy.lib.helper import get_resource_type
from kadi_apy.lib.imports import import_eln
from kadi_apy.lib.imports import import_json_schema
from kadi_apy.lib.imports import import_shacl


class Miscellaneous(RequestMixin, VerboseMixin):
    """Model to handle miscellaneous functionality.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    """

    def get_deleted_resources(self, **params):
        r"""Get a list of deleted resources in the trash. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = "/trash"
        return self._get(endpoint, params=params)

    def restore(self, item, item_id):
        """Restore an item from the trash.

        :param item: The resource type defined either as string or class.
        :param item_id: The ID of the item to restore.
        :type item_id: int
        :return: The response object.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        endpoint = f"{item.base_path}/{item_id}/restore"
        return self._post(endpoint)

    def purge(self, item, item_id):
        """Purge an item from the trash.

        :param item: The resource type defined either as string or class.
        :param item_id: The ID of the item to restore.
        :type item_id: int
        :return: The response object.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        endpoint = f"{item.base_path}/{item_id}/purge"
        return self._post(endpoint)

    def get_licenses(self, **params):
        r"""Get a list of available licenses.  Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = "/licenses"
        return self._get(endpoint, params=params)

    def get_kadi_info(self):
        """Get information about the Kadi instance.

        :return: The response object.
        """

        endpoint = "/info"
        return self._get(endpoint)

    def get_roles(self):
        """Get all possible roles and corresponding permissions of all resources.

        :return: The response object.
        """

        endpoint = "/roles"
        return self._get(endpoint)

    def get_tags(self, **params):
        r"""Get a list of all tags. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = "/tags"
        return self._get(endpoint, params=params)

    def import_eln(self, file_path):
        """Import an RO-Crate file following the "ELN" file specification.

        :param file_path: The path of the file.
        :type file_path: str
        :raises KadiAPYInputError: If the structure of the RO-Crate is not valid.
        :raises KadiAPYRequestError: If any request was not successful while importing
            the data and metadata.
        """
        return import_eln(self.manager, file_path)

    def import_json_schema(self, file_path, template_type="extras"):
        """Import JSON Schema file and create a template.

        Note that only JSON Schema draft 2020-12 is fully supported, but older schemas
        might still work.

        :param file_path: The path of the file.
        :type file_path: str
        :param template_type: Type of the template. Can either be ``"record"`` or
            ``"extras"``.
        :type template_type: str
        :raises KadiAPYInputError: If the structure of the Schema is not valid.
        :raises KadiAPYRequestError: If any request was not successful while importing
            the metadata.
        """
        return import_json_schema(self.manager, file_path, template_type)

    def import_shacl(self, file_path, template_type="extras"):
        """Import SHACL Shapes file and create a template.

        :param file_path: The path of the file.
        :type file_path: str
        :param template_type: Type of the template. Can either be ``"record"`` or
            ``"extras"``.
        :type template_type: str
        :raises KadiAPYInputError: If the structure of the Shapes is not valid.
        :raises KadiAPYRequestError: If any request was not successful while importing
            the metadata.
        """
        return import_shacl(self.manager, file_path, template_type)
