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
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.helper import get_resource_type
from kadi_apy.lib.helper import list_to_tokenlist
from kadi_apy.lib.search import Search


class CLISearch(Search, RaiseRequestErrorMixin):
    """Search class to be used in a CLI.

    :param manager: Manager to use for all API requests.
    :type manager: CLIKadiManager
    """

    def search_resources(self, item, user=None, use_my_user_id=False, **params):
        r"""Search for resources.

        :param item: The resource type defined either as string or class.
        :param user: ID of the user whose items are to be searched for.
        :type user: int
        :param use_my_user_id: Flag indicating if only the records corresponding to the
            used PAT are to be searched for.
        :type use_my_user_id: bool
        :param \**params: Additional query parameters.
        :raises KadiAPYInputError: If both a user ID is given and the flag
            ``use_my_user_id`` is ``True``.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        if user is not None and use_my_user_id:
            raise KadiAPYInputError(
                "Please specify either an user id or use the flag '-i'."
            )

        if use_my_user_id:
            user = self.manager.pat_user.id
        elif user is not None:
            user = user.id

        if user is None:
            response = super().search_resources(item, **params)
        else:
            response = super().search_user_resources(item, user=user, **params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params.get("page", 1)

            self.info(
                f"Found {payload['_pagination']['total_items']} {item.__name__}(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                self.info(
                    f"Found {item.__name__} {results['id']} with title "
                    f"'{results['title']}' and identifier '{results['identifier']}'."
                )
        else:
            self.raise_request_error(response)

    def search_resource_ids(self, item, pipe=False, i_am_sure=False, **params):
        r"""Search for resource ids.

        :param item: The resource type defined either as string or class.
        :param pipe: If the results should be printed in form of a tokenlist for piping.
        :type pipe: bool
        :param i_am_sure: If the search results in more than 1000 results, this flag has
            to be activated to search for all results.
        :type i_am_sure: bool
        :param \**params: Additional query parameters.
        :return: A list of ids found.
        :rtype: list
        :raises KadiAPYConfigurationError: If more than 1000 results are found and the
            flag 'i_am_sure' is not set to true.
        """

        if "page" in params:
            del params["page"]

        if "per_page" in params:
            del params["per_page"]

        if isinstance(item, str):
            item = get_resource_type(item)

        page = 1
        response = super().search_resources(item, page=page, per_page=100, **params)

        list_ids = []

        if response.status_code == 200:
            payload = response.json()
            total_pages = payload["_pagination"]["total_pages"]
            total_items = payload["_pagination"]["total_items"]

            if not i_am_sure and total_items > 1000:
                raise KadiAPYInputError(
                    f"Found {total_items} {item.name}(s), which is more than"
                    " 1000. If you are sure to continue, please use the flag"
                    " 'i_am_sure'."
                )

            if not pipe:
                self.info(f"Found {total_items} {item.name}(s).")

            for page in range(1, total_pages + 1):
                if page != 1:
                    response = super().search_resources(
                        item, page=page, per_page=100, **params
                    )
                if response.status_code == 200:
                    payload = response.json()
                    if not pipe and page % 10 == 0:
                        self.info(f"Processing page {page} of {total_pages}.")

                    for result in payload["items"]:
                        list_ids.append(result["id"])
                else:
                    self.raise_request_error(response)
        else:
            self.raise_request_error(response)

        if pipe:
            self.info(list_to_tokenlist(list_ids))
        else:
            if list_ids:
                self.info(list_ids)

        return list_ids

    def search_users(self, **params):
        response = super().search_users(**params)

        if response.status_code == 200:
            payload = response.json()
            current_page = params.get("page", 1)

            self.info(
                f"Found {payload['_pagination']['total_items']} user(s) on "
                f"{payload['_pagination']['total_pages']} page(s).\n"
                f"Showing results of page {current_page}:"
            )
            for results in payload["items"]:
                self.info(
                    f"Found user '{results['displayname']}' (id"
                    f" '{results['id']}', username '{results['identity']['username']}',"
                    f" identity_type '{results['identity']['type']}')."
                )
        else:
            self.raise_request_error(response)
