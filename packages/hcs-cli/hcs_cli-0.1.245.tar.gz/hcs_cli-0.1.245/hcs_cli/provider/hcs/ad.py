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

from hcs_core.plan import actions
from hcs_cli.service import admin
from httpx import HTTPStatusError


def deploy(data: dict, state: dict) -> dict:
    ret = admin.ad.create(data)
    ret["_creator"] = "hcs_plan"
    return ret


def refresh(data: dict, state: dict) -> dict:
    org_id = data["orgId"]
    if state:
        id = state.get("id")
        if id:
            return admin.ad.get(id, org_id)

    # Fall back with smart find by name
    search = "name $eq " + data["name"]
    ads = admin.ad.list(org_id=org_id, search=search)
    if ads:
        return ads[0]

    # Fall back with smart find by dnsName
    search = "dnsDomainName $eq " + data["dnsDomainName"]
    ads = admin.ad.list(org_id=org_id, search=search)
    if ads:
        return ads[0]


def decide(data: dict, state: dict):
    return actions.skip


def destroy(data: dict, state: dict, force: bool) -> dict:
    org_id = data["orgId"]
    id = state["id"]
    try:
        return admin.ad.delete(id, org_id)
    except HTTPStatusError as e:
        if e.response and e.response.status_code == 409 and "ACTIVE_DIRECTORY_IN_USE" in e.response.text:
            pass
        else:
            raise e


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "1m"
    if action == actions.delete:
        return "1m"
