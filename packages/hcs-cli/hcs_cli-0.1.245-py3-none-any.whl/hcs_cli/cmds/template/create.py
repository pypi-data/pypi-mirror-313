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
from hcs_cli.service import admin
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

    org_id = cli.get_org_id(org)
    if not template["orgId"]:
        template["orgId"] = org_id

    if not template["providerInstanceId"]:
        provider_id = recent.get("provider")
        if not provider_id:
            raise Exception("Invalid template payload: missing provider ID.")
        template["providerInstanceId"] = provider_id

    ret = admin.template.create(template)

    template_id = ret["id"]
    recent.set("template", template_id)
    if wait != "0":
        ret = admin.template.wait_for_ready(template_id, org_id, wait)
    return ret


def _rand_id(n: int):
    return "".join(random.choices("abcdefghijkmnpqrstuvwxyz23456789", k=n))
