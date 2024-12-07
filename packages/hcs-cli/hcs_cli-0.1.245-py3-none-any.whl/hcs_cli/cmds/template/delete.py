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
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command()
@click.argument("id", type=str, required=False)
@cli.force
@cli.confirm
@cli.org_id
@cli.wait
def delete(id: str, force: bool, confirm: bool, org: str, wait: str):
    """Delete template by ID"""

    org_id = cli.get_org_id(org)
    id = recent.require(id, "template")
    ret = admin.template.get(id, org_id)
    if not ret:
        return "", 1

    if not confirm:
        click.confirm(f"Delete template {ret['name']} ({id})?", abort=True)

    ret = admin.template.delete(id, org_id, force)

    if wait == "0":
        return ret

    admin.template.wait_for_deleted(id, org_id, wait)
