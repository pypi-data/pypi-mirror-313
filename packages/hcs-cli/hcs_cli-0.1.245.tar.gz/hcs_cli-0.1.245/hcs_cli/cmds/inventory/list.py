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
from hcs_core.ctxp import recent


@click.command()
@cli.org_id
@click.argument("template_id", type=str, required=False)
def list(template_id: str, org: str):
    """List template VMs"""
    template_id = recent.require(template_id, "template")
    ret = inventory.list(template_id, cli.get_org_id(org))
    recent.helper.default_list(ret, "vm")
    if not ret:
        return "", 1
    return ret
