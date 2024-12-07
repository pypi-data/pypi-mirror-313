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

import time
from hcs_core.sglib.client_util import hdc_service_client, default_crud, wait_for_res_status
from hcs_core.util.query_util import with_query, PageRequest

_client = hdc_service_client("admin")
_crud = default_crud(_client, "/v2/templates", "template")


def create(payload):
    return _crud.create(payload, ignore_warnings=True)


def delete(id: str, org_id: str, force: bool = True):
    return _crud.delete(id, org_id, force=force)


def update(id: str, org_id: str, patch_to: dict, **kwargs):
    url = f"/v2/templates/{id}?org_id={org_id}"
    # print(url)
    # import json
    # print(json.dumps(patch_to))
    return _client.patch(url, json=patch_to)


def wait_for_ready(id: str, org_id: str, timeout: str = "10m"):
    return wait_for(
        id=id, org_id=org_id, target_status="READY", unexpected_status=["ERROR", "DELETING"], timeout=timeout
    )


def wait_for(
    id: str,
    org_id: str,
    target_status: list,
    unexpected_status: list = None,
    transition_status: list = None,
    timeout: str = "10m",
):
    name = "template/" + id
    fn_get = lambda: get(id, org_id)
    fn_get_status = lambda t: t["reportedStatus"].get("statusValue")

    if not target_status:
        raise Exception("Invalid parameter. target_status must not be empty.")

    if isinstance(target_status, str):
        target_status = [target_status]

    if not unexpected_status:
        unexpected_status = list({"ERROR", "DELETING"} - set(target_status))

    if not transition_status:
        transition_status = ["EXPANDING", "SHRINKING", "INIT"]
    status_map = {
        "ready": target_status,
        "error": unexpected_status,
        "transition": transition_status,
    }
    return wait_for_res_status(
        resource_name=name, fn_get=fn_get, get_status=fn_get_status, status_map=status_map, timeout=timeout
    )


wait_for_deleted = _crud.wait_for_deleted


get = _crud.get
list = _crud.list


def action(id: str, org_id: str, action: str):
    url = f"/v2/templates/{id}?org_id={org_id}&action={action}"
    return _client.post(url)
