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
import json
import sys
from hcs_cli.service import admin
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the payload file name. If not specified, STDIN will be used.",
)
@cli.org_id
def create(file: str, org: str, **kwargs):
    """Create Active Directory record"""

    org_id = cli.get_org_id(org)

    with file:
        payload = file.read()

    try:
        template = json.loads(payload)
    except Exception as e:
        msg = "Invalid template: " + str(e)
        return msg, 1

    template["orgId"] = org_id

    ret = admin.ad.create(template, **kwargs)
    if ret:
        recent.set("ad", ret["id"])
    return ret
