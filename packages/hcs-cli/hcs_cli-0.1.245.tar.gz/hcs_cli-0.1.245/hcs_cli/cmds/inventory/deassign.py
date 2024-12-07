"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import json
import click
from hcs_cli.service import inventory
import hcs_core.sglib.cli_options as cli


@click.command()
@cli.org_id
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
def deassign(org: str, file):
    """Assign user to VM"""
    org_id = cli.get_org_id(org)
    with file:
        data = file.read()

    try:
        payload = json.loads(data)
    except Exception as e:
        msg = "Invalid payload: " + str(e)
        return msg, 1

    payload["orgId"] = org_id
    return inventory.deassign(payload)
