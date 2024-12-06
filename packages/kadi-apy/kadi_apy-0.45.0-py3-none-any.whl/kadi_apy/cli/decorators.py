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
import sys
from functools import wraps

import click
from requests.exceptions import ConnectionError
from requests.exceptions import MissingSchema
from requests.exceptions import SSLError
from xmlhelpy import Choice
from xmlhelpy import Integer
from xmlhelpy import IntRange
from xmlhelpy import TokenList
from xmlhelpy import option

from kadi_apy.cli.core import CLIKadiManager
from kadi_apy.globals import Verbose
from kadi_apy.lib.core import KadiManager
from kadi_apy.lib.exceptions import KadiAPYConfigurationError
from kadi_apy.lib.exceptions import KadiAPYException
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.helper import get_resource_type


_identity_types = ["ldap", "local", "shib"]


def apy_command(use_kadi_manager=False):
    r"""Decorator to handle the default arguments and exceptions of an APY command.

    This function inits the :class:`.KadiManager` or :class:`.CLIKadiManager` and
    includes it as ``manager`` to ``**kwargs``. It adds the options ``instance`` and
    ``verbose`` to the CLI tool.

    :param use_kadi_manager: Flag to use the :class:`.KadiManager` instead of the
        :class:`.CLIKadiManager`.
    :type use_kadi_manager: bool, optional
    """

    def decorator(func):
        option(
            "instance",
            char="I",
            description="Name of a Kadi instance defined in the config file.",
        )(func)

        option(
            "verbose",
            char="V",
            description="Verbose level to define the amount of print output.",
            default="info",
            param_type=Choice(["error", "warning", "info", "debug"]),
        )(func)

        @wraps(func)
        def decorated_command(instance, verbose, *args, **kwargs):
            try:
                if use_kadi_manager:
                    kwargs["manager"] = KadiManager(
                        instance=instance, verbose=Verbose[verbose.upper()]
                    )
                else:
                    kwargs["manager"] = CLIKadiManager(
                        instance=instance, verbose=Verbose[verbose.upper()]
                    )
            except KadiAPYConfigurationError as e:
                click.echo(e, err=True)
                sys.exit(1)

            try:
                func(*args, **kwargs)
            except KadiAPYException as e:
                click.echo(e, err=True)
                sys.exit(1)
            except SSLError as e:
                click.echo(e, err=True)
                click.echo(
                    "Use 'verify = False' in the config file to skip verifying the"
                    " SSL/TLS certificate of the host (not recommended) or include a"
                    " path to certificates of trusted CAs in the config file via"
                    " 'ca_bundle = /path/to/certfile'."
                )
                sys.exit(1)
            except MissingSchema as e:
                click.echo(e, err=True)
                click.echo(
                    "Please check the host information since the URL schema (e.g. http"
                    " or https) is missing."
                )
                sys.exit(1)
            except ConnectionError as e:
                click.echo(e, err=True)
                host = kwargs["manager"].host
                click.echo(
                    f"Could not connect to the host ({host}). It could be that the host"
                    " is temporarily unavailable or the URL is incorrect."
                )
                sys.exit(1)

        return decorated_command

    # Decoration without parentheses.
    if callable(use_kadi_manager):
        return apy_command()(use_kadi_manager)

    return decorator


def id_identifier_options(
    class_type,
    keep_manager=False,
    helptext=None,
    name=None,
    required=True,
    char=None,
    allow_tokenlist=False,
    tokenlist_name=None,
    tokenlist_char="T",
):
    r"""Decorator to handle the common ID and identifier options of commands.

    This function inits a resource and includes it to ``**kwargs``. It adds the options
    to read the ID or the identifier of the resource to the CLI tool.

    :param class_type: The resource type defined either as string or class.
    :param keep_manager: Whether to keep the manager for further use.
    :type keep_manager: bool, optional
    :param helptext: Text to describe the input.
    :type helptext: str, optional
    :param name: Name to better describe the input.
    :type name: str, optional
    :param required: Whether the parameter is required.
    :type required: bool, optional
    :param char: Char for the options.
    :type char: str, optional
    :param allow_tokenlist: Flag indicating if a tokenlist should be an option for
        input. If ``True`` the manager is passed to the function even if
        ``keep_manager`` is ``False``.
    :type allow_tokenlist: bool, optional
    :param tokenlist_name: Name of the tokenlist.
    :type tokenlist_name: str, optional
    :param tokenlist_char: Char for the tokenlist.
    :type tokenlist_char: str, optional
    """

    def decorator(func):
        if isinstance(class_type, str):
            resource = get_resource_type(class_type)
        else:
            resource = class_type

        help_id = f"ID of the {resource.name}"
        if helptext:
            help_id = f"{help_id} {helptext}"
        else:
            help_id = help_id + "."

        help_identifier = f"Identifier of the {resource.name}"
        if helptext:
            help_identifier = f"{help_identifier} {helptext}"
        else:
            help_identifier = help_identifier + "."

        char_option_1 = None
        char_option_2 = None

        if name is None:
            text_option = f"{resource.name}-id"
            if not char:
                char_option_1 = f"{resource.name[0].lower()}"
        else:
            text_option = f"{resource.name}-id-{name.lower()}"
            if not char:
                char_option_1 = f"{name[0].lower()}"

        if char:
            char_option_1 = f"{char[0].lower()}"
            char_option_2 = f"{char[0].upper()}"

        option(
            text_option,
            char=char_option_1,
            description=help_id,
            param_type=Integer,
            default=None,
        )(func)

        if allow_tokenlist:
            tokenlist_description = f"Tokenlist of {resource.name} IDs"
            if helptext:
                tokenlist_description = f"{tokenlist_description} {helptext}"
            else:
                tokenlist_description = help_id + "."

            if tokenlist_name is None:
                text_tokenlist_option = f"{resource.name}-ids"
            else:
                text_tokenlist_option = tokenlist_name

            option(
                text_tokenlist_option,
                char=tokenlist_char,
                description=tokenlist_description,
                param_type=TokenList,
            )(func)

        if name is None:
            text_option = f"{resource.name}-identifier"
            if not char:
                char_option_2 = f"{resource.name[0].upper()}"
        else:
            text_option = f"{resource.name}-identifier-{name.lower()}"
            if not char:
                char_option_2 = f"{name[0].upper()}"

        option(
            text_option,
            char=char_option_2,
            description=help_identifier,
            default=None,
        )(func)

        @wraps(func)
        def decorated_command(manager, *args, **kwargs):
            if name is None:
                text_id = f"{resource.name}_id"
                text_identifier = f"{resource.name}_identifier"
            else:
                text_id = f"{resource.name}_id_{name.lower()}"
                text_identifier = f"{resource.name}_identifier_{name.lower()}"

            item_id = kwargs[str(text_id)]
            item_identifier = kwargs[f"{text_identifier}"]

            if (item_id is None and item_identifier is None and required) or (
                item_id is not None and item_identifier is not None
            ):
                exit = False
                if allow_tokenlist:
                    if tokenlist_name is None:
                        text_tokenlist_option = f"{resource.name}_ids"
                    else:
                        text_tokenlist_option = tokenlist_name

                    if kwargs[str(text_tokenlist_option)] is None:
                        text = (
                            f"Please specify the {resource.name} ids via"
                            f" '{text_tokenlist_option}' or either the id or the"
                            f" identifier of the {resource.name}"
                        )
                        exit = True
                else:
                    text = (
                        f"Please specify either the id or the identifier of the"
                        f" {resource.name}"
                    )
                    exit = True

                if exit:
                    if helptext:
                        text = f"{text} {helptext}"
                    else:
                        text = f"{text}."
                    click.echo(text)
                    sys.exit(1)

            # Init the item either by the id or the identifier.
            # The item is directly passed to the function as e.g. record in case of
            # records or {name} if a name is given. If no information is given, None is
            # returned.
            if item_id is not None or item_identifier is not None:
                item = getattr(manager, resource.name)(
                    identifier=item_identifier, id=item_id
                )
            else:
                item = None

            if name is None:
                kwargs[str(resource.name)] = item
            else:
                kwargs[f"{name.lower()}"] = item

            del kwargs[str(text_id)]
            del kwargs[str(text_identifier)]

            if keep_manager or allow_tokenlist:
                kwargs["manager"] = manager

            func(*args, **kwargs)

        return decorated_command

    return decorator


def user_id_options(helptext=None, required=True, keep_manager=False):
    r"""Decorator to handle options to identify a user.

    This function inits a :class:`.CLIUser` and includes it to ``**kwargs``. Is adds
    the options to read the user ID, username and identity-type to the CLI tool.

    :param helptext: Text to describe the input.
    :type helptext: str, optional
    :param keep_manager: Whether to keep the manager for further use.
    :type keep_manager: bool, optional
    :param required: Whether to init the user is required.
    :type required: bool, optional
    """

    def decorator(func):
        description = "ID of the user"
        if helptext:
            description = f"{description} {helptext}"
        else:
            description = description + "."

        option(
            "user",
            char="u",
            description=description,
            default=None,
            param_type=Integer,
        )(func)

        description = "Username of the user"
        if helptext:
            description = f"{description} {helptext}"
        else:
            description = description + "."

        option(
            "username",
            char="U",
            description=description,
            default=None,
        )(func)

        description = "Identity type of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "identity-type",
            char="D",
            description=description,
            param_type=Choice(_identity_types),
        )(func)

        @wraps(func)
        def decorated_command(user, username, identity_type, manager, *args, **kwargs):
            if user is None and username is None:
                if required:
                    raise KadiAPYInputError(
                        "Please specify the user via id or username and identity type."
                    )
                kwargs["user"] = None

            elif username is not None and identity_type is None:
                raise KadiAPYInputError(
                    f"Please specify the identity type to username '{username}'."
                    f" The following types are available {_identity_types}."
                )
            else:
                kwargs["user"] = manager.user(
                    id=user, username=username, identity_type=identity_type
                )

            if keep_manager:
                kwargs["manager"] = manager

            func(*args, **kwargs)

        return decorated_command

    return decorator


def file_id_options(helptext=None, required=True, name=None, char=None):
    r"""Decorator to handle options to identify a file of a record.

    :param helptext: Text to describe the input.
    :type helptext: str, optional
    :param required: Whether to init the file is required.
    :type required: bool, optional
    :param name: Name to better describe the input.
    :type name: str, optional
    :param char: Char for the options.
    :type char: str, optional
    """

    def decorator(func):
        description = "Name of the file"
        if helptext:
            description = f"{description} {helptext}"
        else:
            description = description + "."

        char_option_1 = None
        char_option_2 = None

        if name is None:
            text_option = "file-name"
            if not char:
                char_option_1 = "n"
        else:
            text_option = f"{name}-name"
            if not char:
                char_option_1 = f"{name[0].lower()}"

        if char:
            char_option_1 = f"{char[0].lower()}"
            char_option_2 = f"{char[0].upper()}"

        option(
            text_option,
            char=char_option_1,
            description=description,
            default=None,
        )(func)

        description = "ID of the file"
        if helptext:
            description = f"{description} {helptext}"
        else:
            description = description + "."

        if name is None:
            text_option = "file-id"
            if not char:
                char_option_2 = "i"
        else:
            text_option = f"{name}-id"
            if not char:
                char_option_2 = f"{name[0].upper()}"

        option(
            text_option,
            char=char_option_2,
            description=description,
            default=None,
        )(func)

        @wraps(func)
        def decorated_command(*args, **kwargs):
            if name is None:
                text_id = "file_id"
                text_name = "file_name"
            else:
                text_id = f"{name}_id"
                text_name = f"{name}_name"

            file_id = kwargs[str(text_id)]
            file_name = kwargs[str(text_name)]

            if required:
                if (file_name is None and file_id is None) or (
                    file_name is not None and file_id is not None
                ):
                    text = "Please specify either the name or the id of the file"
                    if helptext:
                        text = f"{text} {helptext}"
                    click.echo(f"{text}.")
                    sys.exit(1)

            if file_name:
                record = kwargs["record"]
                kwargs[str(text_id)] = record.get_file_id(file_name)
            else:
                kwargs[str(text_id)] = file_id

            del kwargs[str(text_name)]

            func(*args, **kwargs)

        return decorated_command

    return decorator


def search_pagination_options(description_page=None):
    r"""Decorator to add two parameters for the search.

    :param description_page: Description of the ``page`` option.
    :type description_page: str, optional
    """

    def decorator(func):
        description = "Page for search results."
        if description_page is not None:
            description = description_page
        option(
            "page",
            char="p",
            description=description,
            param_type=IntRange(min=1),
            default=1,
        )(func)
        option(
            "per-page",
            char="n",
            description="Number of results per page.",
            param_type=IntRange(1, 100),
            default=10,
        )(func)

        @wraps(func)
        def decorated_command(*args, **kwargs):
            func(*args, **kwargs)

        return decorated_command

    if callable(description_page):
        return search_pagination_options()(description_page)

    return decorator
