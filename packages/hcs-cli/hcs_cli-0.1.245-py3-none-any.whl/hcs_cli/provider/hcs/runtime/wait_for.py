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

import logging
from hcs_cli.service import admin
from hcs_core.plan import PlanException, context, actions
from hcs_core.sglib.client_util import hdc_service_client, wait_for_res_status

_client = hdc_service_client("")

log = logging.getLogger(__name__)


def process(data: dict, state: dict) -> dict:
    url = data["url"]
    name = data.get("name")
    interval = data.get("interval", "10s")
    timeout = data.get("timeout", "1m")
    criteria = data.get("criteria")
    field = data.get("field")
    expected = data.get("expected", ["ready"])
    unexpected = data.get("unexpected", [])
    transition = data.get("transition", [None])
    wait_on_not_found = data.get("wait_on_not_found", False)

    def fn_get():
        ret = _client.get(url)
        if not ret:
            if wait_on_not_found:
                return {}
        return ret

    def fn_get_status(t):
        if field:
            field_keys = field.split(".")
            field_len = len(field_keys)
            subt = t
            for x in range(field_len):
                if subt:
                    subt = subt.get(field_keys[x])
                else:
                    break
            return subt
        else:
            return "ready" if t else None

    status_map = {
        "ready": expected,
        "error": unexpected,
        "transition": transition,
    }
    ret = wait_for_res_status(
        name,
        fn_get=fn_get,
        get_status=fn_get_status,
        status_map=status_map,
        timeout=timeout,
        polling_interval=interval,
    )
    return ret


def destroy(data: dict, state: dict, force: bool):
    return


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return data.get("timeout", "1m")
    return "1m"
