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
from hcs_cli.service.lcm import template
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command("list")
@cli.org_id
@cli.limit
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
@click.option("--name", "-n", type=str, required=False, help="Optionally, specify name pattern to find.")
def list_templates(org: str, limit: int, type: str, name: str, **kwargs):
    """List templates"""
    if org == "all":
        ret = template.list(limit=limit, name=name, type=type)
    else:
        ret = template.list(limit=limit, org_id=cli.get_org_id(org), name=name, type=type)
    recent.helper.default_list(ret, "template")
    return ret
