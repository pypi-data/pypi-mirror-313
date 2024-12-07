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
from hcs_cli.service import admin
from hcs_cli.service.admin import VM
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.confirm
@cli.wait
def delete(vm_path: str, org: str, confirm: bool, wait: str, **kwargs):
    """Delete a VM by ID"""
    org_id = cli.get_org_id(org)
    template_id, vm_id = parse_vm_path(vm_path)

    vm = VM(org_id, template_id, vm_id)
    existing = vm.get()
    if not existing:
        return "", 1

    template = admin.template.get(template_id, org_id)

    if not confirm:
        click.confirm(f"Delete vm {existing['id']} from template {template['name']} ({template['id']})?", abort=True)

    vm.delete()

    if wait == "0":
        return

    vm.wait_for_deleted(wait)
