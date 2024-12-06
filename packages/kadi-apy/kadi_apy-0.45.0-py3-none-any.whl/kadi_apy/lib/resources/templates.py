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
from kadi_apy.lib.commons import ExportMixin
from kadi_apy.lib.commons import PermissionMixin
from kadi_apy.lib.resource import Resource


class Template(Resource, ExportMixin, PermissionMixin):
    r"""Model to represent templates.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    :param type: Type of the template. Can either be ``record`` or ``extras``.
    :type type: str
    :param data: Dict in case of a record template or a list in case of a extras
        template containing the content for the template.
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

    base_path = "/templates"
    name = "template"

    def get_users(self, **params):
        r"""Get users from a template. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/users"
        return self._get(endpoint, params=params)

    def get_template_revisions(self, **params):
        r"""Get the revisions of this template.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions"
        return self._get(endpoint, params=params)

    def get_template_revision(self, revision_id, **params):
        r"""Get a specific revision of this template.

        :param revision_id: The revision ID of the template.
        :type revision_id: int
        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions/{revision_id}"
        return self._get(endpoint, params=params)

    def get_groups(self, **params):
        r"""Get group roles from a template. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/groups"
        return self._get(endpoint, params=params)
