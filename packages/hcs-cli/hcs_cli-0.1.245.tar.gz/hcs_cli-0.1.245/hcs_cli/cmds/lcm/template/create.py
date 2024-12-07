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

import sys
import json
import random
import click
import hcs_core.util.duration as duration
import hcs_cli.service.lcm as lcm
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
@cli.org_id
@cli.wait
def create(file: str, org: str, wait: str, **kwargs):
    """Create a template"""

    with file:
        payload = file.read()

    try:
        template = json.loads(payload)
    except Exception as e:
        msg = "Invalid template: " + str(e)
        return msg, 1

    template_id = _rand_id(16)
    template["id"] = template_id
    org_id = cli.get_org_id(org)
    template["orgId"] = org_id

    provider = _create_zerocloud_provider(org_id)
    template["provider"]["providerAccessId"] = provider["id"]

    ret = lcm.template.create(template)

    recent.require(ret["id"], "template")
    if wait != "0":
        ret = lcm.template.wait(template_id, org_id, duration.to_seconds(wait))
    return ret


def _rand_id(n: int):
    return "".join(random.choices("abcdefghijkmnpqrstuvwxyz23456789", k=n))


def _create_zerocloud_provider(org_id: str):
    data = {"name": "nanw-test-" + _rand_id(4), "orgId": org_id, "type": "ZEROCLOUD"}

    return lcm.provider.create(data)
