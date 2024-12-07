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
from hcs_core.ctxp.util import parse_kv_pairs
import hcs_cli.service.synt.outpost as outpost


@click.command()
@click.option("--name", "-n", type=str, required=True, help="Specify the outpost name.")
@click.option("--region", "-r", type=str, required=True, help="Specify the outpost region.")
@click.option(
    "--type", "-t", type=click.Choice(["CLOUD_HOSTED", "ON_PREM"]), required=True, help="Specify the outpost name."
)
@click.option(
    "--property",
    "-p",
    type=str,
    required=False,
    multiple=True,
    help="Property in '=' separated key-value pair. This parameter can be specified multiple times.",
)
def create(name: str, region: str, type: str, property: list, **kwargs):
    """Create an outpost"""

    payload = {"name": name, "properties": parse_kv_pairs(property), "region": region, "type": type}
    return outpost.create(payload, **kwargs)
    # return payload
