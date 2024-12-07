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
import hcs_cli.service.synt.probe as probe


@click.command()
@cli.org_id
@click.option(
    "--outposts",
    type=str,
    required=False,
    help="Specify the outposts to run this probe, must be a subset of the associated outposts. If not specified, the probe will run on all associated outposts.",
)
@click.argument("id", type=str, required=True)
def run(org: str, outposts: str, id: str, **kwargs):
    """Run the probe immediately."""
    org_id = cli.get_org_id(org)
    outpost_ids = _get_outpost_ids(org, id, outposts)
    return probe.schedule_now(id=id, outpost_ids=outpost_ids, org_id=org_id, **kwargs)


def _get_outpost_ids(org_id, id, outposts):
    if outposts:
        return outposts.split(",")
    p = probe.get(id, org_id)
    return p["outpostIds"]
