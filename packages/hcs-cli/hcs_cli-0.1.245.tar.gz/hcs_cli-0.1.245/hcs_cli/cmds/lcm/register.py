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
from hcs_cli.service import inventory, lcm
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path


@click.command()
@cli.org_id
@click.option("--cloud-id", type=str, required=True)
@click.argument("vm_path", type=str, required=False)
def register(org: str, vm_path: str, cloud_id: str):
    """Register an existing VM."""
    org_id = cli.get_org_id(org)
    template_id, vm_id = parse_vm_path(vm_path)

    template = lcm.template.get(template_id, org_id)
    if not template:
        return "Template not found.", 1

    vms = [{"id": vm_id, "cloudId": cloud_id}]
    ret = inventory.vm.begin_adding_vms(template_id=template_id, org_id=org_id, vms=vms)
    print(ret)
    template_type = template["templateType"]
    num_sessions = template["agentCustomization"]["sessionsPerVm"]
    vms = [{"id": vm_id, "powerState": "poweredOn"}]
    ret = inventory.vm.finish_adding_vms(
        template_id=template_id, org_id=org_id, num_sessions=num_sessions, template_type=template_type, vms=vms
    )
    return ret
