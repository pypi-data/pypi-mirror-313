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
import shutil
import subprocess
import sys

from xmlhelpy import Path
from xmlhelpy import group
from xmlhelpy import option

from kadi_apy.cli.decorators import apy_command
from kadi_apy.cli.decorators import file_id_options
from kadi_apy.cli.decorators import id_identifier_options


@group()
def workflows():
    """Commands to manage workflows (experimental)."""


@workflows.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to download the workflow from")
@file_id_options(helptext="to execute as workflow", required=True, name="workflow")
@option(
    "path",
    char="p",
    description="Path to store and execute the workflow.",
    param_type=Path(exists=True),
    default=".",
)
@option(
    "force",
    char="f",
    description="Enable if existing file with identical name should be replaced.",
    is_flag=True,
    default=False,
)
def execute(record, workflow_id, path, force):
    """Download and execute a workflow."""

    if not shutil.which("process_engine"):
        record.error(
            "'process_engine' not found in PATH, see"
            " https://gitlab.com/iam-cms/workflows/process-engine how to install it.",
        )
        sys.exit(1)

    response = record.get_file_info(workflow_id)

    if response.status_code == 200:
        payload = response.json()
        if payload["mimetype"] != "application/x-flow+json":
            file_name = payload["name"]
            record.error(
                f"Given file '{file_name}' is not a workflow file.",
            )
            sys.exit(1)
    else:
        record.error(f"File with ID '{workflow_id}' is not available in {record}.")
        record.raise_request_error(response)

    list_filepath = record.get_file(path, force=force, file_id=workflow_id)

    workflow_file = list_filepath[0]

    record.info(f"Starting executing the workflow at '{path}'.")

    cmd = ["process_engine", "run", workflow_file, "-p", path]

    sys.exit(subprocess.call(cmd))
