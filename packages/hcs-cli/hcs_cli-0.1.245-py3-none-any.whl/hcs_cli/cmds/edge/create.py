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
import sys
from hcs_cli.service import admin
from hcs_core.ctxp import CtxpException, recent
import hcs_core.sglib.cli_options as cli
from hcs_core.sglib import payload_util


@click.command()
@cli.org_id
@click.option("--provider", "-p", type=str, default=None, required=False, help="Override the provider instance ID")
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the payload file name. If not specified, STDIN will be used.",
)
@cli.wait
def create(org: str, provider: str, file: str, wait: str):
    """Create an edge.

    Example:
      hcs edge create < path/to/payload.json
    """

    payload = payload_util.get_payload_with_defaults(file, org)
    org_id = cli.get_org_id(org)

    if provider:
        payload["providerInstanceId"] = provider
    else:
        if not payload["providerInstanceId"]:
            payload["providerInstanceId"] = recent.require(None, "provider")
    if not payload["orgId"]:
        payload["orgId"] = org_id

    _validate(payload)

    ret = admin.edge.create(payload)
    if not ret:
        return "", 1
    edge_id = ret["id"]
    recent.set("edge", edge_id)
    if wait != "0":
        admin.edge._wait_for_terminal_state(edge_id, org_id, wait)

    return ret


def _validate(payload):
    if not payload.get("providerInstanceId"):
        raise CtxpException("Missing providerInstanceId")
