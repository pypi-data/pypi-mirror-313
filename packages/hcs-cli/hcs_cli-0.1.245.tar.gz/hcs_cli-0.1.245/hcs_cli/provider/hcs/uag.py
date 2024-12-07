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

from hcs_core.plan import actions, PluginException
from hcs_cli.service import admin


def deploy(data: dict, state: dict, save_state) -> dict:
    org_id = data["orgId"]
    if not state:
        deployment = admin.uag.create(data)
        save_state(deployment)
    else:
        deployment = state
    id = deployment["id"]
    try:
        deployment = admin.uag.wait_for_ready(id, org_id, "10m")
    except Exception as e:
        deployment = admin.uag.get(id, org_id)
        save_state(deployment)
        raise PluginException("Fail waiting for UAG deployment.") from e
    return deployment


def refresh(data: dict, state: dict) -> dict:
    org_id = data["orgId"]
    if state:
        id = state.get("id")
        if id:
            ret = admin.uag.get(id, org_id)
            if ret:
                return ret
    search = f'name $eq {data["name"]}'
    uags = admin.uag.list(org_id, search=search)
    if uags:
        return uags[0]


def decide(data: dict, state: dict):
    if state["status"] in ["READY"]:
        return actions.skip


def destroy(data: dict, state: dict, force: bool) -> dict:
    id = state["id"]
    org_id = data["orgId"]
    admin.uag.safe_delete(id, org_id)


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "10m"
    if action == actions.delete:
        return "10m"
