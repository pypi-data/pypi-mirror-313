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
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.lib.helper import get_resource_type
from kadi_apy.lib.misc import Miscellaneous


class CLIMiscellaneous(Miscellaneous, RaiseRequestErrorMixin):
    """Model to handle miscellaneous functionality.

    See :class:`.Miscellaneous` for the possible parameters.
    """

    def get_deleted_resources(self, **params):
        r"""Get a list of deleted resources in the trash using the CLI.

        Supports pagination.

        :param \**params: Additional query parameters.
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().get_deleted_resources(**params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params.get("page", 1)

            self.info(
                f"Found {payload['_pagination']['total_items']} resource(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                self.info(
                    f"Found {results['type']} {results['id']} with identifier"
                    f" '{results['identifier']}'."
                )
        else:
            self.raise_request_error(response)

    def restore(self, item, item_id):
        """Restore an item from the trash using the CLI.

        :param item: The resource type defined as class.
        :param item_id: The ID of the item to restore.
        :type item_id: int
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().restore(item=item, item_id=item_id)
        if response.status_code == 200:
            self.info(f"Successfully restored {item.name} {item_id} from the trash.")
        else:
            self.raise_request_error(response)

    def purge(self, item, item_id):
        """Purge an item from the trash  using the CLI.

        :param item: The resource type defined as class or string.
        :param item_id: The ID of the item to restore.
        :type item_id: int
        :raises KadiAPYRequestError: If request was not successful.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        response = super().purge(item=item, item_id=item_id)

        # Records are handled differently and return status code 202 on success.
        if response.status_code in {202, 204}:
            self.info(f"Successfully purged {item.name} {item_id} from the trash.")
        else:
            self.raise_request_error(response)

    def get_licenses(self, **params):
        r"""Get a list of available licenses using the CLI.

        :param \**params: Additional query parameters.
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().get_licenses(**params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params.get("page", 1)

            self.info(
                f"Found {payload['_pagination']['total_items']} license(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                self.info(f"{results['name']}")
        else:
            self.raise_request_error(response)

    def get_kadi_info(self, manager):
        """Print information about the Kadi instance and the config file.

        :param manager: Used Manager.
        :type manager: KadiManager, CLIKadiManager

        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        response = super().get_kadi_info()
        if response.status_code == 200:
            version = response.json()["version"]

            if manager.instance is not None:
                print_instance = f"'{manager.instance}' "
            else:
                print_instance = ""

            token_mask = f"{manager.pat[:10]}***"

            self.info(
                f"You are using instance {print_instance}with host '{manager.host}' and"
                f" Kadi4Mat version '{version}'.\nThe token is '{token_mask}' and"
                f" belongs to {manager.pat_user}."
            )
        else:
            self.raise_request_error(response)

    def get_roles(self, item_type=None):
        r"""Get a list of all possible roles.

        Print all possible roles and corresponding permissions of all resources or of
        one resource.

        :param item_type: Type of resource for printing roles and permissions.
        :type item_type: str, optional
        :raises KadiAPYRequestError: If request was not successful.
        """
        response = super().get_roles()
        if response.status_code == 200:
            payload = response.json()
            for item, roles in payload.items():
                if item_type is not None:
                    if item_type != item:
                        continue
                self.info(f"Roles for resource '{item}':")
                for role in roles:
                    name = role["name"]
                    self.info(f"  As '{name}', you have the following possibilities:")
                    permissions = role["permissions"]
                    for permission in permissions:
                        action = permission["action"]
                        description = permission["description"]
                        self.info(f"    {action}: {description}")

        else:
            self.raise_request_error(response)

    def get_tags(self, **params):
        r"""Get a list of all available tags using the CLI.

        :param \**params: Additional query parameters.
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().get_tags(**params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params.get("page", 1)

            self.info(
                f"Found {payload['_pagination']['total_items']} tags(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                self.info(f"{results['name']}")
        else:
            self.raise_request_error(response)
