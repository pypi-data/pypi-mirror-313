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

import json

from httpx import HTTPStatusError


from hcs_core.ctxp import jsondot
from hcs_core.plan import actions, PluginException
from hcs_cli.service import av


def deploy(data: dict, state: dict, save_state) -> dict:
    org_id = data["orgId"]
    av_app_name = data["appName"]
    try:
        if not state:
            av.avimport.import_av_app(data)
    except HTTPStatusError as e:
        err = json.loads(e.response.text)
        if (
            err
            and e.response.status_code == 400
            and err.get("errors")
            and err.get("errors")[0].get("code") == "IMPORT_IN_PROGRESS"
        ):
            pass
        else:
            raise e
    try:
        deployment = av.avimport.wait_for(av_app_name, org_id, timeout="5m")
    except Exception as e:
        deployment = av.app.get_by_names([av_app_name], org_id)
        save_state(deployment)
        raise PluginException("Error waiting for app volume import deployment.") from e
    return deployment


def refresh(data: dict, state: dict) -> dict:
    org_id = data["orgId"]
    get_app_info = av.app.get_by_names([data["appName"]], org_id)
    if get_app_info:
        return get_app_info[0]


def decide(data: dict, state: dict):
    if state["name"] == data["appName"]:
        return actions.skip


def destroy(data: dict, state: dict, force: bool) -> dict:
    av_app_name = data["appName"]
    org_id = data["orgId"]
    av.app.delete(av_app_name, org_id)
    av.avimport.wait_for_deleted(app_name=av_app_name, org_id=org_id, timeout="1m")
    return state


def eta(action: str, data: dict, state: dict):
    return "1m"
