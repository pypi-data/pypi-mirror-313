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
from hcs_core.sglib.client_util import hdc_service_client, wait_for_res_status, wait_for_res_deleted
from .app import get_by_names
from hcs_core.util import hcs_constants

log = logging.getLogger(__name__)
_client = hdc_service_client("av-appies")


def import_av_app(payload: dict):
    pid = payload["data"]["providerInstanceId"]
    import_status = get_import_status(pid)
    if import_status and import_status["importStatus"] == hcs_constants.AV_IMPORT_AVAILABLE:
        url = hcs_constants.AV_IMPORT_API_URL
        return _client.post(url, payload)
    else:
        return


def get_import_status(pid: str):
    url = hcs_constants.AV_IMPORT_STATUS_API_URL + pid
    return _client.get(url)


def wait_for(av_app_name: str, org_id: str, timeout: str = "20m"):
    name = "av-import-app/" + av_app_name

    def fn_get_status(_rec):
        try:
            if _rec:
                _l_status = _rec[0].get("name")
            else:
                _l_status = ""
        except Exception as e:
            _l_status = hcs_constants.ERROR
        return _l_status

    def fn_get_av_fs_info():
        return get_by_names([av_app_name], org_id)

    status_map = {"ready": av_app_name, "error": hcs_constants.ERROR, "transition": ""}
    return wait_for_res_status(
        resource_name=name, fn_get=fn_get_av_fs_info, get_status=fn_get_status, status_map=status_map, timeout=timeout
    )


def wait_for_deleted(app_name: str, org_id: str, timeout: str = "10m"):
    name = "av_import/" + app_name

    def fn_get():
        _app_list = get_by_names([app_name], org_id)
        if _app_list:
            return _app_list
        return

    return wait_for_res_deleted(name, fn_get, timeout)
