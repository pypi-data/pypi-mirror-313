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
from datetime import datetime

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.helper import ResourceMeta


class User(ResourceMeta):
    r"""Model to represent users.

    A user can either be clearly identified via its id or the combination of username
    and identity type.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    :param id: The ID of an existing user.
    :type id: int, optional
    :param username: The username.
    :type username: str, optional
    :param identity_type: The identity type of the user.
    :type identity_type: str, optional
    :param use_pat: Flag to indicate that the pat stored in the KadiManager should be
        used for instantiating the user.
    :type use_pat: bool, optional
    :raises KadiAPYRequestError: If retrieving the user was not successful.
    """

    base_path = "/users"
    name = "user"

    def __init__(
        self,
        manager,
        id=None,
        username=None,
        identity_type=None,
        use_pat=False,
    ):
        super().__init__(manager)
        self.id = id

        if self.id is not None:
            response = self._get(f"{self.base_path}/{self.id}")
            if response.status_code != 200:
                raise KadiAPYRequestError(
                    f"The user with ID {self.id} does not exist.\n"
                    f"{response.json()['description']}"
                )

            self._meta = response.json()

        elif use_pat:
            response = self._get("/users/me")
            if response.status_code != 200:
                raise KadiAPYRequestError(response.json())

            self._meta = response.json()
            self.id = self._meta["id"]

        elif username is not None and identity_type is not None:
            response = self._get(f"{self.base_path}/{identity_type}/{username}")
            if response.status_code != 200:
                raise KadiAPYRequestError(
                    f"The user with username {username} and identity type "
                    f"{identity_type} does not exist.\n{response.json()['description']}"
                )
            self._meta = response.json()
            self.id = self._meta["id"]

        else:
            raise KadiAPYInputError(
                "Please specify the user via id or username and identity type."
            )

        # Save the time the metadata was updated last.
        self._last_update = datetime.utcnow()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            f"{self.meta['displayname']} (id: {self.id}, account type:"
            f" {self.meta['identity']['type']}, username:"
            f" {self.meta['identity']['username']})"
        )
