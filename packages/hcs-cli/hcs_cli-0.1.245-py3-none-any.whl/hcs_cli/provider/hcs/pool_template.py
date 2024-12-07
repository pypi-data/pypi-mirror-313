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

from typing import Callable
from hcs_core.plan import actions
from hcs_core.plan import PluginException
import hcs_cli.service.admin as admin


def deploy(data: dict, state: dict, save_state: Callable) -> dict:
    org_id = data["orgId"]

    if state:
        id = state.get("id")
    else:
        id = None

    if not id:
        ret = admin.template.create(data)
        save_state(ret)
        id = ret["id"]

    try:
        template = admin.template.wait_for_ready(id, org_id, timeout="20m")
    except Exception as e:
        template = admin.template.get(id, org_id)
        save_state(template)
        raise PluginException("Template deployment failed.") from e
    return template


def refresh(data: dict, state: dict) -> dict:
    if state:
        id = state["id"]
        if id:
            org_id = data["orgId"]
            t = admin.template.get(id, org_id)
            if t:
                return t

    # Fall back with smart find by name
    name = data["name"]
    search = "name $eq " + name
    templates = admin.template.list(org_id=data["orgId"], search=search)
    if templates:
        return templates[0]


def decide(data: dict, state: dict):
    return actions.create


def destroy(data: dict, state: dict, force: bool) -> dict:
    id = state["id"]
    org_id = data["orgId"]
    admin.template.delete(id, org_id)
    admin.template.wait_for_deleted(id, org_id, 600)


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "15m"
    if action == actions.delete:
        return "10m"
