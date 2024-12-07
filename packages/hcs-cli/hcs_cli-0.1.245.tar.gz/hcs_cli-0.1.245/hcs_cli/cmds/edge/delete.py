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

import httpx
import click
from hcs_core.ctxp import recent
from hcs_cli.service import admin
import hcs_core.sglib.cli_options as cli


@click.command()
@click.argument("id", type=str, required=False)
@cli.org_id
@cli.wait
@click.option(
    "--delete-all/--delete-edge-only",
    type=bool,
    default=True,
    help="Specify whether to delete associated resources, if any.",
)
@cli.force
@cli.confirm
def delete(id: str, org: str, wait: str, delete_all: bool, force: bool, confirm: bool):
    """Delete edge by ID"""

    org_id = cli.get_org_id(org)
    id = recent.require(id, "edge")
    ret = admin.edge.get(id, org_id)
    if not ret:
        return "", 1

    if not confirm:
        click.confirm(f"Delete edge {ret['name']} ({id})?", abort=True)

    if delete_all:
        uags = admin.helper.get_uags_by_edge(id, org_id)
        for u in uags:
            _start_deleting_uag(u["id"], org_id)
        for u in uags:
            admin.uag.wait_for_deleted(u["id"], org_id, timeout="10m")

    ret = admin.edge.delete(id, org_id, force=force)
    if not ret:
        return "", 1

    acceptable_status = [
        "DELETE_PENDING",
        "DELETED",
        "FORCE_DELETE_PENDING",
        "DELETING",
        "FORCE_DELETING",
    ]
    accepted = ret["status"] in acceptable_status
    if not accepted:
        return ret, 1

    if wait == "0":
        return ret

    admin.edge.wait_for_deleted(id, org_id, wait)


def _start_deleting_uag(uag_id: str, org_id: str):
    try:
        admin.uag.delete(uag_id, org_id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            if e.response.text.find("UAG_DEPLOYMENT_DELETE_ALREADY_IN_PROGRESS") > 0:
                return
        raise
