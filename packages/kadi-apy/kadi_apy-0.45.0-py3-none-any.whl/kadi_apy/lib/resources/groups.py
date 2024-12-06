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
from kadi_apy.lib.resource import Resource


class Group(Resource):
    r"""Model to represent groups.

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

    base_path = "/groups"
    name = "group"

    def get_records(self, **params):
        r"""Get records shared with a group. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/records"
        return self._get(endpoint, params=params)

    def get_collections(self, **params):
        r"""Get collections shared with a group. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/collections"
        return self._get(endpoint, params=params)

    def get_templates(self, **params):
        r"""Get templates shared with a group. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/templates"
        return self._get(endpoint, params=params)

    def get_users(self, **params):
        r"""Get users of a group. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/members"
        return self._get(endpoint, params=params)

    def add_user(self, user_id, role_name):
        """Add a user.

        :param user_id: The ID of the user to add.
        :type user_id: int
        :param role_name: Role of the user.
        :type role_name: str
        :return: The response object.
        """

        endpoint = self._actions["add_member"]
        data = {"role": {"name": role_name}, "user": {"id": user_id}}
        return self._post(endpoint, json=data)

    def remove_user(self, user_id):
        """Remove a user.

        :param user_id: The ID of the user to remove.
        :type user_id: int
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/members/{user_id}"
        return self._delete(endpoint, json=None)

    def get_group_revisions(self, **params):
        r"""Get the revisions of this group.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions"
        return self._get(endpoint, params=params)

    def get_group_revision(self, revision_id, **params):
        r"""Get a specific revision from this group.

        :param revision_id: The revision ID of the group.
        :type revision_id: int
        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions/{revision_id}"
        return self._get(endpoint, params=params)

    def change_user_role(self, user_id, role_name):
        """Change role of a user.

        :param user_id: The ID of the user whose role should be changed.
        :type user_id: int
        :param role_name: Name of the new role.
        :type role_name: str
        :return: The response object.
        """

        endpoint = f"{self._actions['add_member']}/{user_id}"
        data = {"name": role_name}
        return self._patch(endpoint, json=data)
