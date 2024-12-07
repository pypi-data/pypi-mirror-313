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

import click
from hcs_cli.service import inventory
from hcs_cli.support.param_util import parse_vm_path
import hcs_core.sglib.cli_options as cli
import hcs_core.ctxp.data_util as data_util


@click.command()
@cli.org_id
@click.option(
    "--update",
    "-u",
    type=str,
    required=True,
    help="Specify field and value pair to update. E.g., '-f lifecycleStatus=MAINTENANCE'.",
)
@click.argument("vm_path", type=str, required=False)
def update(org: str, update: str, vm_path: str):
    """Update a specific VM."""
    template_id, vm_id = parse_vm_path(vm_path)

    org_id = cli.get_org_id(org)
    existing_vm = inventory.get(template_id, vm_id, org_id)
    if not existing_vm:
        return "VM not found", 1

    k, v = update.split("=")

    current_value = data_util.deep_get_attr(existing_vm, k)
    if str(current_value) == str(v):
        return existing_vm

    # data_util.deep_set_attr(vm, k, v)
    body = {k: v}
    ret = inventory.update(template_id, vm_id, org_id, body)
    return ret
