"""
Copyright 2023-2024 VMware Inc.
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

from hcs_core.sglib.client_util import hdc_service_client, default_crud

_client = hdc_service_client("synthetic-testing")
_crud = default_crud(_client, "/v1/probes", "probe")

list = _crud.list
get = _crud.get
delete = _crud.delete
create = _crud.create
update = _crud.update


def schedule_now(id: str, org_id: str, outpost_ids: list):
    payload = {"outpostIds": outpost_ids}
    url = f"/v1/probes/{id}/schedule-now"
    if org_id:
        url += "?orgId=" + org_id
    return _client.post(url, payload)
