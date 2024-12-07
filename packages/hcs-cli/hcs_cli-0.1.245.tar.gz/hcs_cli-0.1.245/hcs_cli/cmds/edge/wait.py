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
from hcs_cli.service import admin
from hcs_core.util import duration
from hcs_core.ctxp import recent
import hcs_core.sglib.cli_options as cli

_all_status = [
    "CREATE_PENDING",
    "CREATING",
    "READY",
    "POST_PROVISIONING_CONFIG_IN_PROGRESS",
    "UPDATE_PENDING",
    "UPDATING",
    "UPGRADE_PENDING",
    "UPGRADING",
    "CREATE_FAILED",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_PENDING",
    "DELETING",
    "FORCE_DELETE_PENDING",
    "FORCE_DELETING",
    "FORCE_REPAIR_ACCEPTED",
    "FORCE_REPAIR_PENDING",
    "CONNECT_PENDING",
    "CREATE_ACCEPTED",
    "CREATE_FAILED",
    "CREATE_PENDING",
    "CREATING",
    "DELETED",
    "DELETE_FAILED",
    "DELETE_PENDING",
    "DELETING",
    "FORCE_DELETE_PENDING",
    "FORCE_DELETING",
    "FORCE_REPAIR_ACCEPTED",
    "FORCE_REPAIR_PENDING",
    "MIGRATE_FAILED",
    "MIGRATE_PENDING",
    "MIGRATING",
    "POST_PROVISIONING_CONFIG_IN_PROGRESS",
    "READY",
    "REPAIRING",
    "REPAIR_ACCEPTED",
    "REPAIR_FAILED",
    "REPAIR_PENDING",
    "UPDATE_FAILED",
    "UPDATE_PENDING",
    "UPDATING",
    "UPGRADE_FAILED",
    "UPGRADE_PENDING",
    "UPGRADING",
]


@click.command()
@cli.org_id
@click.argument("id", type=str, required=False)
@click.option(
    "--status",
    "-s",
    type=click.Choice(_all_status),
    required=False,
    default="READY",
    help="The target status to wait for.",
)
@click.option("--timeout", "-t", type=str, required=False, default="1m", help="Timeout. Examples: '2m', '30s', '1h30m'")
@click.option(
    "--fail-fast/--fail-timeout",
    "-f",
    type=bool,
    default=True,
    required=False,
    help="Stop waiting if the template reached to non-expected terminal states, e.g. waiting for ERROR but template is READY, or waiting for READY and template is ERROR.",
)
@click.option(
    "--silent/--return-object",
    type=bool,
    required=False,
    default=True,
    help="Slient mode will has no output on success. Otherwise the full template is returned",
)
def wait(org: str, id: str, status: str, timeout: str, fail_fast: bool, silent: bool):
    """Wait for an edge to transit to specific status."""

    org_id = cli.get_org_id(org)
    target_status = status.upper().split(",")
    unexpected_status = []
    if fail_fast:
        if "READY" not in target_status:
            unexpected_status.append("READY")
        if "ERROR" not in target_status:
            unexpected_status.append("ERROR")

    def is_ready(s):
        return s in target_status

    def is_error(s):
        return s.endswith("_FAILED") or s in [
            # 'CREATE_FAILED',
            "DELETED",
            # 'DELETE_FAILED',
            "DELETE_PENDING",
            "DELETING",
            "FORCE_DELETE_PENDING",
            "FORCE_DELETING",
            "FORCE_REPAIR_ACCEPTED",
            "FORCE_REPAIR_PENDING",
            # CONNECT_PENDING,
            # CREATE_ACCEPTED,
            # CREATE_FAILED,
            # CREATE_PENDING,
            # CREATING,
            "DELETED",
            #'DELETE_FAILED',
            "DELETE_PENDING",
            "DELETING",
            "FORCE_DELETE_PENDING",
            "FORCE_DELETING",
            "FORCE_REPAIR_ACCEPTED",
            "FORCE_REPAIR_PENDING",
            #'MIGRATE_FAILED',
            "MIGRATE_PENDING",
            "MIGRATING",
            # POST_PROVISIONING_CONFIG_IN_PROGRESS,
            # READY,
            "REPAIRING",
            "REPAIR_ACCEPTED",
            #'REPAIR_FAILED',
            "REPAIR_PENDING",
            #'UPDATE_FAILED',
            #'UPDATE_PENDING',
            #'UPDATING',
            #'UPGRADE_FAILED',
            #'UPGRADE_PENDING',
            #'UPGRADING',
        ]

    def is_transition(s):
        return s.endswith("ING") or s in [
            "CREATE_ACCEPTED",
            "CREATE_PENDING",
            "CREATING",
            "POST_PROVISIONING_CONFIG_IN_PROGRESS",
            "UPDATE_PENDING",
            "UPDATING",
            "UPGRADE_PENDING",
            "UPGRADING",
        ]

    id = recent.require(id, "edge")
    try:
        edge = admin.edge.get(id, org_id=cli.get_org_id(org))
        if not edge:
            return "", 1
        edge = admin.edge.wait_for(
            id,
            org_id,
            is_ready=is_ready,
            is_error=is_error,
            is_transition=is_transition,
            timeout=timeout,
        )

        return edge if not silent else None
    except Exception as e:
        return str(e), 1
