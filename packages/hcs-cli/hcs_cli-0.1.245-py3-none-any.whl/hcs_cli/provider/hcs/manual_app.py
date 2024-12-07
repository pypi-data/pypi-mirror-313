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
from hcs_cli.service.app_management import manual_app


def deploy(data: dict, state: dict) -> dict:
    return manual_app.create(data)


def refresh(data: dict, state: dict) -> dict:
    id = None
    org_id = data["orgId"]
    if state:
        id = state["id"]

        # workaround https://jira-euc.eng.vmware.com/jira/browse/HV2-109561
        try:
            p = manual_app.get(id, org_id)
        except Exception as e:
            return
        if p:
            return p

    # Fall back with smart find by name
    # TODO


def decide(data: dict, state: dict):
    return actions.skip


def destroy(data: dict, state: dict, force: bool) -> dict:
    org_id = data["orgId"]
    id = state["id"]
    return manual_app.delete(id, org_id)


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "1m"
    if action == actions.delete:
        return "1m"
