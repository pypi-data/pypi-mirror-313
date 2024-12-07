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

import re

from hcs_core.plan import actions, PluginException
from hcs_cli.service import av


def deploy(data: dict, state: dict) -> dict:
    providerInstanceId = data["providerInstanceId"]
    result = dict()
    try:
        deployment = av.fileshare.wait_for(providerInstanceId, timeout="30m")
        if deployment and deployment.content[0]:
            _storage_acc_name = deployment.content[0].path.split(".")
            _acc_name = re.sub("[^A-Za-z0-9]", "", _storage_acc_name[0])
            result = {"storageAccountName": _acc_name}
    except Exception as e:
        raise PluginException("Exception while checking for AV fileshare provision.") from e
    return result


def refresh(data: dict, state: dict) -> dict:
    return state


def decide(data: dict, state: dict):
    return actions.skip


def destroy(data: dict, state: dict, force: bool) -> dict:
    return state


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "10m"
    if action == actions.delete:
        return "1m"
