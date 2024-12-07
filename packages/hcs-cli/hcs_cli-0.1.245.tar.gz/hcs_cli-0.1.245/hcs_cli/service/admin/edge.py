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
import logging
from typing import Callable
from hcs_core.sglib.client_util import hdc_service_client, default_crud, wait_for_res_status

log = logging.getLogger(__name__)

_client = hdc_service_client("admin")
base_context = "/v2/edge-deployments"
_crud = default_crud(_client, base_context, "edge")

get = _crud.get
list = _crud.list
delete = _crud.delete
create = _crud.create
wait_for_deleted = _crud.wait_for_deleted


def wait_for(
    id: str,
    org_id: str,
    status_map: dict = None,
    is_ready: Callable = None,
    is_error: Callable = None,
    is_transition: Callable = None,
    timeout: str = "20m",
    polling_interval: str = "60s",
):
    name = "edge/" + id

    def fn_get():
        return get(id, org_id)

    return wait_for_res_status(
        resource_name=name,
        fn_get=fn_get,
        get_status="status",
        status_map=status_map,
        is_ready=is_ready,
        is_error=is_error,
        is_transition=is_transition,
        timeout=timeout,
        polling_interval=polling_interval,
    )
    # Edge status
    # [
    # CONNECT_PENDING,
    # CREATE_ACCEPTED,
    # CREATE_FAILED,
    # CREATE_PENDING,
    # CREATING,
    # DELETED,
    # DELETE_FAILED,
    # DELETE_PENDING,
    # DELETING,
    # FORCE_DELETE_PENDING,
    # FORCE_DELETING,
    # FORCE_REPAIR_ACCEPTED,
    # FORCE_REPAIR_PENDING,
    # MIGRATE_FAILED,
    # MIGRATE_PENDING,
    # MIGRATING,
    # POST_PROVISIONING_CONFIG_IN_PROGRESS,
    # READY,
    # REPAIRING,
    # REPAIR_ACCEPTED,
    # REPAIR_FAILED,
    # REPAIR_PENDING,
    # UPDATE_FAILED,
    # UPDATE_PENDING,
    # UPDATING,
    # UPGRADE_FAILED,
    # UPGRADE_PENDING,
    # UPGRADING
    # ]


def safe_delete(id: str, org_id: str, timeout: str = "20m"):
    try:
        delete(id, org_id=org_id, force=True)
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 409:
            raise
        _wait_for_terminal_state(id, org_id, timeout)
        delete(id, org_id=org_id, force=True)

    wait_for_deleted(id, org_id, "10m")


def _wait_for_terminal_state(id, org_id, timeout):
    name = "edge/" + id
    terminal_status = [
        "CREATE_FAILED",
        "DELETED",
        "DELETE_FAILED",
        "MIGRATE_FAILED",
        "READY",
        "REPAIR_FAILED",
        "UPDATE_FAILED",
        "UPGRADE_FAILED",
    ]
    transition_status = [
        "CONNECT_PENDING",
        "CREATE_ACCEPTED",
        "CREATE_PENDING",
        "CREATING",
        "DELETE_PENDING",
        "DELETING",
        "FORCE_DELETE_PENDING",
        "FORCE_DELETING",
        "FORCE_REPAIR_ACCEPTED",
        "FORCE_REPAIR_PENDING",
        "MIGRATE_PENDING",
        "MIGRATING",
        "POST_PROVISIONING_CONFIG_IN_PROGRESS",
        "REPAIRING",
        "REPAIR_ACCEPTED",
        "REPAIR_PENDING",
        "UPDATE_PENDING",
        "UPDATING",
        "UPGRADE_PENDING",
        "UPGRADING",
    ]

    def fn_get():
        return get(id, org_id)

    status_map = {"ready": terminal_status, "error": [], "transition": transition_status}

    wait_for_res_status(
        resource_name=name,
        fn_get=fn_get,
        get_status="status",
        status_map=status_map,
        timeout=timeout,
        not_found_as_success=True,
    )


def get_connection_string(id: str, org_id: str):
    url = f"{base_context}/{id}/device-connection-string?org_id={org_id}"
    return _client.get(url)
