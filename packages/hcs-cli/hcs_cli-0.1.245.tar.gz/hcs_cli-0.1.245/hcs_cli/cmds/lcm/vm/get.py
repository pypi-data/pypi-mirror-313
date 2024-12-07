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
from hcs_cli.service.lcm import vm
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
def get(vm_path: str, org: str, **kwargs):
    """Get VM by ID"""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    ret = vm.get(template_id, vm_id, org_id, **kwargs)
    if not ret:
        return "", 1
    return ret
