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
from hcs_core.sglib.client_util import hdc_service_client, default_crud, wait_for_res_status

_client = hdc_service_client("admin")
_crud = default_crud(_client, "/v2/uag-deployments", "uag")
get = _crud.get
list = _crud.list
create = _crud.create
delete = _crud.delete
wait_for_deleted = _crud.wait_for_deleted


def wait_for_ready(id, org_id, timeout):
    name = "uag/" + id
    fn_get = lambda: get(id, org_id)
    status_map = {
        "ready": "READY",
        "error": ["FAILED", "DELETION_FAILED"],
        "transition": [
            "DEPLOYING",
            "PENDING",
        ],
        # Other
        # 'ADDING_EXTERNAL_ACCESS',
        # 'ADDING_EXTERNAL_ACCESS_FAILED',
        # 'ADDING_EXTERNAL_ACCESS_ROLLBACK',
        # 'ADDING_EXTERNAL_ACCESS_ROLLBACK_FAILED',
        # 'ADDING_INTERNAL_ACCESS',
        # 'ADDING_INTERNAL_ACCESS_FAILED',
        # 'ADDING_INTERNAL_ACCESS_ROLLBACK',
        # 'ADDING_INTERNAL_ACCESS_ROLLBACK_FAILED',
        # 'DELETED',
        # 'DELETE_PENDING',
        # 'DELETING',
        # 'DELETION_FAILED',
        # 'PARTIALLY_READY',
        # 'REMOVING_EXTERNAL_ACCESS',
        # 'REMOVING_EXTERNAL_ACCESS_FAILED',
        # 'REMOVING_EXTERNAL_ACCESS_ROLLBACK',
        # 'REMOVING_EXTERNAL_ACCESS_ROLLBACK_FAILED',
        # 'REMOVING_INTERNAL_ACCESS',
        # 'REMOVING_INTERNAL_ACCESS_FAILED',
        # 'REMOVING_INTERNAL_ACCESS_ROLLBACK',
        # 'REMOVING_INTERNAL_ACCESS_ROLLBACK_FAILED',
        # 'UPDATE_FAILED',
        # 'UPDATE_PENDING',
        # 'UPDATING',
        # 'UPGRADE_FAILED',
        # 'UPGRADE_PENDING',
        # 'UPGRADING'
    }
    return wait_for_res_status(
        resource_name=name, fn_get=fn_get, get_status="status", status_map=status_map, timeout=timeout
    )


def _wait_for_terminal_state(id, org_id, timeout):
    name = "uag/" + id
    terminal_status = ["READY", "FAILED", "DELETED", "DELETION_FAILED"]

    def fn_get():
        return get(id, org_id)

    status_map = {"ready": terminal_status, "error": [], "transition": ["DELETE_PENDING"]}

    wait_for_res_status(
        resource_name=name,
        fn_get=fn_get,
        get_status="status",
        status_map=status_map,
        timeout=timeout,
        not_found_as_success=True,
    )


def safe_delete(id: str, org_id: str, timeout: str = "20m"):
    try:
        delete(id, org_id=org_id, force=True)
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 409:
            raise
        _wait_for_terminal_state(id, org_id, timeout)
        delete(id, org_id=org_id, force=True)

    def fn_is_error(uag):
        return uag["status"] == "DELETION_FAILED"

    wait_for_deleted(id, org_id, "10m", fn_is_error=fn_is_error)
