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
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp.util import parse_kv_pairs
import hcs_cli.service.synt.outpost as outpost


@click.command()
@click.argument("id", type=str, required=True)
@click.option("--name", "-n", type=str, required=False)
@click.option(
    "--property",
    "-p",
    type=str,
    required=False,
    multiple=True,
    help="Property in '=' separated key-value pair. This parameter can be specified multiple times.",
)
@cli.org_id
def update(id: str, name: str, property: str, org: str, **kwargs):
    """Update an existing template"""

    org_id = cli.get_org_id(org)

    data = {}
    if name:
        data["name"] = name
    properties = parse_kv_pairs(property)
    if properties:
        data["properties"] = properties
    return outpost.update(id=id, org_id=org_id, data=data, **kwargs)
