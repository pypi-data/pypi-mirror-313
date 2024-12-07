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
@click.argument("site-id", required=False)
@click.option("--edge", type=str, required=False, help="Edge deployment ID.")
@cli.org_id
def set_edge(site_id: str, edge: str, org: str, **kwargs):
    """Set the edge for a site."""
    site_id = recent.require(site_id, "site")
    edge_id = recent.require(edge, "edge")
    org_id = cli.get_org_id(org)
    return portal.site.set_edge(site_id, org_id, edge_id, **kwargs)
