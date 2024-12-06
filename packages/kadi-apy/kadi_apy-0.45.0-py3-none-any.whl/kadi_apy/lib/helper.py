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
import re
from datetime import datetime
from datetime import timedelta

from kadi_apy.globals import RESOURCE_TYPES
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError


class RequestMixin:
    """Helper function for managing an instance stored in manager."""

    def __init__(self, manager):
        self.manager = manager

    def _get(self, endpoint, **kwargs):
        return self.manager._get(endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self.manager._post(endpoint, **kwargs)

    def _patch(self, endpoint, **kwargs):
        if hasattr(self, "_meta"):
            self._meta = None
        return self.manager._patch(endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self.manager._put(endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        if hasattr(self, "_meta"):
            self._meta = None
        return self.manager._delete(endpoint, **kwargs)


class VerboseMixin:
    """Helper function for printing according to verbose level."""

    def error(self, text, **kwargs):
        r"""Print text for error level.

        :param text: Text to be printed via :func:`click.echo()`.
        :type text: str
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        """

        self.manager.error(text=text, **kwargs)

    def warning(self, text, **kwargs):
        r"""Print text for warning level.

        :param text: Text to be printed via :func:`click.echo()`.
        :type text: str
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        """

        self.manager.warning(text=text, **kwargs)

    def info(self, text, **kwargs):
        r"""Print text for info level.

        :param text: Text to be printed via :func:`click.echo()`.
        :type text: str
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        """

        self.manager.info(text=text, **kwargs)

    def debug(self, text, **kwargs):
        r"""Print text for debug level.

        :param text: Text to be printed via :func:`click.echo()`.
        :type text: str
        :param \**kwargs: Additional arguments to pass to :func:`click.echo()`.
        """

        self.manager.debug(text=text, **kwargs)

    def is_verbose(self, **kwargs):
        """Check the verbose level.

        :return: See :meth:`.KadiManager.is_verbose`.
        """

        return self.manager.is_verbose(**kwargs)


class ResourceMeta(RequestMixin, VerboseMixin):
    """Helper functions."""

    def __init__(self, manager):
        super().__init__(manager)
        self._meta = None
        self._last_update = None

    @property
    def meta(self):
        """Get all metadata of the resource.

        In case the previous metadata was invalidated, either manually, after a timeout
        or due to another request, a request will be sent to retrieve the possibly
        updated metadata again.

        :return: The metadata of the resource.
        :raises KadiAPYRequestError: If requesting the metadata was not successful.
        """

        if self._last_update is not None:
            # Invalidate the cached metadata automatically after 5 minutes.
            if (datetime.utcnow() - self._last_update) > timedelta(minutes=5):
                self._meta = None

        if self._meta is None:
            response = self._get(f"{self.base_path}/{self.id}")
            if response.status_code != 200:
                raise KadiAPYRequestError(response.json())

            self._meta = response.json()
            self._last_update = datetime.utcnow()

        return self._meta


def chunked_response(path, response):
    """Iterately save the data of a given response to a file.

    :param path: The file path to store the file.
    :type path: str
    :param response: The response object, which needs to support streaming.
    """
    with open(path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1_000_000):
            f.write(chunk)


def generate_identifier(identifier):
    """Creates a valid identifier."""
    identifier = re.sub("[^a-z0-9-_ ]+", "", identifier.lower())
    identifier = re.sub("[ ]+", "-", identifier)

    return identifier[:50]


def get_resource_type(resource_type):
    """Map a resource described via string to a class."""
    from kadi_apy.lib.resources.collections import Collection
    from kadi_apy.lib.resources.groups import Group
    from kadi_apy.lib.resources.records import Record
    from kadi_apy.lib.resources.templates import Template

    if resource_type not in RESOURCE_TYPES:
        raise KadiAPYInputError(f"Resource type '{resource_type}' does not exists.")

    _mapping = {
        "record": Record,
        "collection": Collection,
        "group": Group,
        "template": Template,
    }
    return _mapping[resource_type]


def list_to_tokenlist(input_list, separator=","):
    """Create a tokenlist based on a list."""
    return separator.join(str(v) for v in input_list)
