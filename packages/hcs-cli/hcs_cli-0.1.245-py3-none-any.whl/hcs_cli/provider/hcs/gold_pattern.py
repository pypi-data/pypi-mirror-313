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
import hcs_cli.service.ims as ims


def deploy(data: dict, state: dict) -> dict:
    ret = ims.gold_pattern.create(data)
    return ret


def refresh(data: dict, state: dict) -> dict:
    body = data["goldPattern"]
    org_id = body["orgId"]
    if state:
        id = state.get("id")
        if id:
            ret = ims.gold_pattern.get(id, org_id)
            if ret:
                return ret

    # search by provider id and name, which is the criteria used by service side verification
    image_name = body["goldPatternDetails"]["data"]["imageName"]
    ret = ims.gold_pattern.list(org_id, provider_instance_id=body["providerInstanceId"])

    # The current API does not have query parameter for imageName and does not support REST search.
    for r in ret:
        details = r.get("goldPatternDetails")
        if details:
            data = details.get("data")
            if data:
                name = data.get("imageName")
                if name == image_name:
                    return r


def decide(data: dict, state: dict):
    return actions.skip


def destroy(data: dict, state: dict, force: bool) -> dict:
    id = state["id"]
    org_id = data["goldPattern"]["orgId"]
    return ims.gold_pattern.delete(id=id, org_id=org_id)


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "1m"
    if action == actions.delete:
        return "1m"
