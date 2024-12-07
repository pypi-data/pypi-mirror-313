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
import click
import hcs_core.sglib.cli_options as cli
import hcs_cli.service.synt.probe as probe


@click.command()
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the probe file name. If not specified, STDIN will be used.",
)
@click.option(
    "--outposts",
    type=str,
    required=False,
    help="List of outpost IDs, in comma-separated string. If specified, will overrride the existing outpostIds in the file, if any.",
)
@cli.org_id
def create(file: str, outposts: str, org: str, **kwargs):
    """Create a probe"""

    with file:
        data = file.read()

    try:
        payload = json.loads(data)
    except Exception as e:
        msg = "Invalid probe data: " + str(e)
        return msg, 1

    org_id = cli.get_org_id(org)

    if outposts:
        ids = outposts.split(",")
        payload["outpostIds"] = ids
    # return payload
    return probe.create(payload=payload, org_id=org_id, **kwargs)
