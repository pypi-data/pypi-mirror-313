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
from hcs_cli.service import portal
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command()
@click.option("--name", "-n", type=str, required=True)
@click.option("--description", "-d", type=str, required=False)
@cli.org_id
def create(name: str, description: str, org: str):
    """Create a site."""
    org_id = cli.get_org_id(org)
    payload = {"name": name, "description": description, "orgId": org_id}
    ret = portal.site.create(payload)
    if ret:
        recent.set("site", ret["id"])
        return ret
    return ret, 1
