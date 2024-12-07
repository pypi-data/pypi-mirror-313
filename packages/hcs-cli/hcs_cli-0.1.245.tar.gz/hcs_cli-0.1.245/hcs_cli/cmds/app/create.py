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
from hcs_cli.service.app_management import manual_app
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
@click.option("--template", type=str, required=False, help="The pool template ID to associate to.")
@cli.org_id
def create(file: str, template: str, org: str, **kwargs):
    """Create manual app"""

    org_id = cli.get_org_id(org)
    template = recent.require(template, "template")

    # with file:
    #     payload = file.read()

    # try:
    #     data = json.loads(payload)
    # except Exception as e:
    #     msg = "Invalid template: " + str(e)
    #     return msg, 1

    data = {
        "orgId": "",
        "id": "",
        "name": "manual-app1",
        "location": "US",
        "displayName": "manual-app1-display",
        "applicationPath": "c:\\windows\\notepad.exe",
        "version": "v1",
        "publisher": "p1",
        "icons": {},
        "appSpecDetails": [
            {"poolTemplateId": "", "properties": {"startFolder": "c:\\", "commandLineParam": "demo.txt"}}
        ],
    }
    data["orgId"] = org_id
    data["appSpecDetails"][0]["poolTemplateId"] = template

    text = json.dumps(data)
    files = {"application": ("application", text, "application/json")}
    # print(parts)
    ret = manual_app.create(files, **kwargs)
    if ret:
        recent.set("app", ret["id"])
    return ret
