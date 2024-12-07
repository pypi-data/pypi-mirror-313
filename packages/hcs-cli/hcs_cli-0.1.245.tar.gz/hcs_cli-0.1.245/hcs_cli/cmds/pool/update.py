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
import hcs_core.util.duration as duration
from hcs_cli.service import portal
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent
from hcs_cli.support.patch_util import calculate_patch


@click.command()
@click.argument("template_id", type=str, required=False)
@click.option(
    "--update",
    "-u",
    type=str,
    multiple=True,
    required=True,
    help="Specify field and value pair to update. E.g. '-u sparePolicy.max=3'.",
)
@cli.org_id
@cli.wait
def update(template_id: str, update, org: str, wait: str, **kwargs):
    """Update an existing pool"""

    org_id = cli.get_org_id(org)

    pool_id = recent.require(template_id, "pool")
    pool = portal.pool.get(pool_id, org_id)

    if not pool:
        return "Pool not found: " + pool_id

    patch = {}
    for pair in update:
        k, v = pair.split("=")
        patch[k] = v

    ret = portal.pool.update(pool_id, org_id, patch)
    return ret
