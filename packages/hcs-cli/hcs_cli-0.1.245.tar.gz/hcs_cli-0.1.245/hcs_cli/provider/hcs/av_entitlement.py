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
from hcs_cli.service import av


def deploy(data: dict, state: dict, save_state) -> dict:
    if data["data"]["apps"]:
        av.entitlements.create(data)
        return av.entitlements.get_by_app_id(data)
    else:
        return state


def refresh(data: dict, state: dict) -> dict:
    return av.entitlements.get_by_app_id(data)


def decide(data: dict, state: dict):
    return actions.create


def destroy(data: dict, state: dict, force: bool) -> dict:
    if state:
        av.entitlements.delete(state)
    return state


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "1m"
    if action == actions.delete:
        return "1m"
