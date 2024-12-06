# Copyright 2021 Karlsruhe Institute of Technology
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
import configparser
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

import click
from xmlhelpy import Choice
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.main import kadi_apy
from kadi_apy.globals import CONFIG_PATH


def _check_instance(config_file, instance):
    """Exit if instance is not defined in the config."""

    instances = config_file.sections()
    instances.remove("global")

    if instance not in instances:
        click.echo(
            "Please use an instance which is defined in the config file.\n"
            f"Choose one of {instances}"
        )
        sys.exit(1)


def _load_config_file():
    """Load config file."""

    if not os.path.isfile(CONFIG_PATH):
        click.echo("Config file does not exist. Please run 'kadi-apy config create'.")
        sys.exit(1)

    config_file = configparser.ConfigParser()

    try:
        config_file.read(CONFIG_PATH)
    except configparser.ParsingError as e:
        click.echo(f"Error during parsing the config file:\n{e}")
        sys.exit(1)

    return config_file


def _is_url(value):
    try:
        result = urlparse(value)
        if not result.netloc or not result.scheme in ["http", "https"]:
            return False
        return True
    except ValueError:
        return False


def _user_input(key, instance):
    value = input(f"Please enter {key} for instance '{instance}' and press enter: ")

    if key == "host":
        while _is_url(value) is False:
            value = input(
                f"Please enter a valid url, not '{value}'. Try again and press enter:"
            )

    return value


def _mask_pat(value):
    return value[:5].ljust(len(value), "*")


def _set_config_value(key, instance=None):
    """Set a value in the config file."""

    config_file = _load_config_file()

    if instance is None:
        try:
            instance = config_file["global"]["default"]
        except Exception:
            click.echo("No default instance defined in the config file.")
            sys.exit(1)

    _check_instance(config_file, instance)

    value = _user_input(key, instance)

    config_file.set(instance, key, value)

    with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
        config_file.write(configfile)

    if key == "pat":
        value = _mask_pat(value)

    click.echo(f"Successfully set '{key}' to '{value}' for instance '{instance}'.")


@kadi_apy.group()
def config():
    """Commands to manage configurations."""


@config.command()
def create():
    """Create the config file to store the information to connect to a Kadi instance."""

    if os.path.exists(CONFIG_PATH):
        click.echo(f"Config file already exists at '{CONFIG_PATH}'. Nothing to create.")
        sys.exit(1)
    else:
        config_file = configparser.ConfigParser()
        default_instance = "my_instance"

        config_file["global"] = {
            "default": default_instance,
        }
        config_file[default_instance] = {
            "host": "",
            "pat": "",
        }

        with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
            config_file.write(configfile)

        # Make sure the config file is only readable/writable by the current user on
        # Unix systems.
        os.chmod(CONFIG_PATH, 0o600)

        click.echo(
            f"Created config file at '{CONFIG_PATH}'.\n"
            "You can open the file to add the information about the host and personal"
            " access token (PAT) or use the CLI."
        )


@config.command()
@option(
    "instance",
    char="I",
    description="Name of the instance defined in the config. If empty, the default"
    " instance defined in the config file is used.",
)
def set_host(instance):
    """Set a host in the config file."""

    _set_config_value("host", instance)


@config.command()
@option(
    "instance",
    char="I",
    description="Name of the instance defined in the config. If empty, the default"
    " instance defined in the config file is used.",
)
def set_pat(instance):
    """Set a personal access token (pat) in the config file."""

    _set_config_value("pat", instance)


@config.command()
@option(
    "instance",
    char="I",
    description="Name of the new instance.",
    required=True,
)
def add_instance(instance):
    """Add a new instance to the config file."""

    config_file = _load_config_file()

    if instance == "global":
        click.echo("Please use a different name, not 'global'.")
        sys.exit(1)

    instances = config_file.sections()
    instances.remove("global")

    if instance in instances:
        click.echo(f"Instance '{instance}' already present.")
        sys.exit(1)

    config_file.add_section(instance)

    pat = _user_input("pat", instance)
    config_file.set(instance, "pat", pat)
    pat = _mask_pat(pat)

    host = _user_input("host", instance)
    config_file.set(instance, "host", host)

    with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
        config_file.write(configfile)

    click.echo(
        f"Successfully added instance '{instance}' with host {host} and pat '{pat}' to"
        " the config file."
    )


@config.command()
@option(
    "instance",
    char="I",
    description="Name of the new default instance.",
    required=True,
)
def change_default_instance(instance):
    """Change the default instance."""

    config_file = _load_config_file()

    _check_instance(config_file, instance)

    config_file.set("global", "default", instance)

    with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
        config_file.write(configfile)

    click.echo(f"Default instance is {instance}.")


@config.command()
@option(
    "instance",
    char="I",
    description="Name of the instance to change.",
    required=True,
)
@option(
    "instance-new",
    char="N",
    description="New name of the instance.",
    required=True,
)
def rename_instance(instance, instance_new):
    """Rename an instance."""

    config_file = _load_config_file()

    _check_instance(config_file, instance)
    items = config_file.items(instance)
    config_file.remove_section(instance)
    try:
        config_file.add_section(instance_new)
    except configparser.DuplicateSectionError as e:
        click.echo(f"{e}\nPlease choose another name to rename the instance.")
        sys.exit(1)

    for item in items:
        config_file.set(instance_new, item[0], item[1])

    if config_file.get("global", "default") == instance:
        config_file.set("global", "default", instance_new)

    with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
        config_file.write(configfile)

    click.echo(f"Changed instance name from '{instance}' to '{instance_new}'.")


@config.command()
def show_instances():
    """Show a list of all instances defined in the config."""

    config_file = _load_config_file()

    instances = config_file.sections()
    instances.remove("global")

    default_instance = config_file.get("global", "default")

    click.echo(
        f"Instances defined in the config file: {instances}.\n"
        f"Default instance is '{default_instance}'."
    )


@config.command()
@option(
    "shell",
    char="s",
    description="Your shell type.",
    required=True,
    param_type=Choice(["bash", "zsh", "fish"]),
)
def activate_autocompletion(shell):
    """Activate the autocompletion for bash, zsh or fish."""

    name = "kadi-apy"
    name_upper = name.replace("-", "_").upper()

    if shell in ["bash", "zsh"]:
        config_path = Path.home().joinpath(f".{shell}rc")
        target_path = Path.home().joinpath(f".{name}-complete.{shell}")
    else:
        target_path = Path.home().joinpath(
            ".config", "fish", "completions", f"{name}.fish"
        )
        folder = os.path.dirname(target_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

    if os.path.exists(target_path):
        click.echo("Autocompletion is already activated.")
        sys.exit(0)

    my_env = os.environ.copy()
    my_env[f"_{name_upper}_COMPLETE"] = f"{shell}_source"

    with open(target_path, mode="w", encoding="utf-8") as f:
        subprocess.run(name, env=my_env, stdout=f)

    if shell in ["bash", "zsh"]:
        add_import = True
        with open(config_path, encoding="utf-8") as f:
            if str(target_path) in f.read():
                add_import = False

        # Add line only if not already present.
        if add_import:
            with open(config_path, "a", encoding="utf-8") as file:
                file.write("\n")
                file.write(f". {target_path}")
                file.write("\n")

    click.echo(
        f"Successfully installed {shell} completion at '{target_path}'. To use it,"
        " start a new shell."
    )


@config.command()
@apy_command
def get_kadi_info(manager):
    """Get information about the Kadi instance."""

    manager.misc.get_kadi_info(manager)
