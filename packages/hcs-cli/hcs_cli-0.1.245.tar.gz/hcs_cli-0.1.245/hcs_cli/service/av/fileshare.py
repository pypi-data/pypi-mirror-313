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
from hcs_core.sglib.client_util import hdc_service_client, wait_for_res_status
from hcs_core.util.query_util import with_query
from hcs_core.util import hcs_constants

log = logging.getLogger(__name__)
_client = hdc_service_client("av-fileshare")


def get_av_fileshares(**kwargs):
    url = hcs_constants.AV_GET_FILESHARE_API_URL
    url = with_query(url, **kwargs)
    t = _client.get(url)
    return t


def wait_for(provider_instance_id: str, timeout: str = "30m"):
    name = "av-fileshare/" + provider_instance_id

    def fn_get_status(t):
        if t and t.get("content"):
            _status = t["content"][0].get("status")
        else:
            _status = ""
        return _status

    def fn_get_av_fs_info():
        return get_av_fileshares(
            search=f"name $eq staging-{provider_instance_id} AND providerInstanceId $eq {provider_instance_id}"
        )

    status_map = {"ready": hcs_constants.PROVISION_SUCCESS, "error": hcs_constants.PROVISION_FAILED, "transition": ""}
    return wait_for_res_status(
        resource_name=name, fn_get=fn_get_av_fs_info, get_status=fn_get_status, status_map=status_map, timeout=timeout
    )
