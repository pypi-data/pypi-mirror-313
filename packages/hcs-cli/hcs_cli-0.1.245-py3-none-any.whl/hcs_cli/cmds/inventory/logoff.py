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
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path


@click.command()
@cli.org_id
@click.argument("vm_path", type=str, required=True)
def logoff(org: str, vm_path: str):
    """Log off an user"""
    template, vm = parse_vm_path(vm_path)
    ret = inventory.logoff(template, vm, cli.get_org_id(org))
    if ret:
        return ret
    return ret, 1
