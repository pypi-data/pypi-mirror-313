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
from kadi_apy.cli.commons import BasicCLIMixin
from kadi_apy.cli.commons import DeleteItemCLIMixin
from kadi_apy.cli.commons import ExportCLIMixin
from kadi_apy.cli.commons import GroupRoleCLIMixin
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.cli.commons import TagCLIMixin
from kadi_apy.cli.commons import UserCLIMixin
from kadi_apy.lib.resources.collections import Collection


class CLICollection(
    BasicCLIMixin,
    UserCLIMixin,
    GroupRoleCLIMixin,
    TagCLIMixin,
    DeleteItemCLIMixin,
    ExportCLIMixin,
    Collection,
    RaiseRequestErrorMixin,
):
    """Collection class to be used in a CLI.

    :param manager: See :class:`.Collection`.
    :param id: See :class:`.Collection`.
    :param identifier: See :class:`.Collection`.
    :param skip_request: See :class:`.Collection`.
    :param create: See :class:`.Collection`.
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

    def add_record_link(self, record_to):
        """Add a record to a collection using a CLI.

        :param record_to: The the record to add.
        :type record_to: Record
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().add_record_link(record_id=record_to.id)
        if response.status_code == 201:
            self.info(f"Successfully linked {record_to} to {self}.")
        elif response.status_code == 409:
            self.info(f"Link from {self} to {record_to} already exists. Nothing to do.")
        else:
            self.error(f"Linking {record_to} to {self} was not successful.")
            self.raise_request_error(response)

    def remove_record_link(self, record):
        """Remove a record from a collection using a CLI.

        :param record: The record to remove.
        :type record: Record
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().remove_record_link(record_id=record.id)
        if response.status_code == 204:
            self.info(f"Successfully removed {record} from {self}.")
        else:
            self.error(f"Removing {record} from {self} was not successful.")
            self.raise_request_error(response)

    def add_collection_link(self, child_collection):
        """Add a child collection to a parent collection using CLI.

        :param child_collection: The child collection to which the parent collection
            should be added.
        :type child_collection: Collection
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().add_collection_link(collection_id=child_collection.id)
        if response.status_code == 201:
            self.info(f"Successfully linked child {child_collection} to parent {self}.")
        elif response.status_code == 409:
            self.info(
                f"Link from {self} to {child_collection} already exists. Nothing to do."
            )
        else:
            self.error(
                f"Linking child {child_collection} to parent {self} was not successful."
            )
            self.raise_request_error(response)

    def remove_collection_link(self, child_collection):
        """Remove a child collection from a parent collection using CLI.

        :param child_collection: The child collection to remove
            from the parent collection.
        :type child_collection: Collection
        :raises KadiAPYRequestError: If request was not successful.
        """

        response = super().remove_collection_link(collection_id=child_collection.id)
        if response.status_code == 204:
            self.info(
                f"Successfully removed child {child_collection} from parent {self}."
            )
        else:
            self.error(
                f"Removing child {child_collection} from parent {self} was not"
                " successful."
            )
            self.raise_request_error(response)

    def print_info(self, pipe=False, **kwargs):
        r"""Print infos of a collection using the CLI.

        :param \**kwargs: Specify additional infos to print.
        :raises: KadiAPYRequestError: If request was not successful
        """
        super().print_info(pipe=pipe, **kwargs)

        if kwargs.get("records", False):
            response = self.get_records(
                page=kwargs.get("page"), per_page=kwargs.get("per_page")
            )
            if response.status_code == 200:
                payload = response.json()
                self.info(
                    f"Found {payload['_pagination']['total_items']} record(s) on "
                    f"{payload['_pagination']['total_pages']} page(s).\n"
                    f"Showing results of page {kwargs.get('page')}:"
                )
                for results in payload["items"]:
                    self.info(
                        f"Found record '{results['title']}' with id"
                        f" '{results['id']}' and identifier"
                        f" '{results['identifier']}'."
                    )
            else:
                self.raise_request_error(response)

        if kwargs.get("subcollections", False):
            response = self.get_collections(
                page=kwargs.get("page"), per_page=kwargs.get("per_page")
            )
            if response.status_code == 200:
                payload = response.json()
                self.info(
                    f"Found {payload['_pagination']['total_items']} collection(s) on "
                    f"{payload['_pagination']['total_pages']} page(s).\n"
                    f"Showing results of page {kwargs.get('page')}:"
                )

                for results in payload["items"]:
                    self.info(
                        f"Found collection '{results['title']}' with id"
                        f" '{results['id']}' and identifier"
                        f" '{results['identifier']}'."
                    )
            else:
                self.raise_request_error(response)
