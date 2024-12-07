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

from hcs_core.sglib.client_util import hdc_service_client
from hcs_core.util.query_util import with_query, PageRequest

_client = hdc_service_client("inventory")


def get(template_id: str, vm_id: str, org_id: str = None, **kwargs):
    url = f"/v1/{template_id}/{vm_id}"
    if org_id:
        url += "?org_id=" + org_id
    url = with_query(url, **kwargs)
    return _client.get(url)


def list(template_id: str, org_id: str, **kwargs):
    def _get_page(query_string):
        url = f"/v1/{template_id}?org_id={org_id}"
        if query_string:
            url += "&" + query_string
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def raw_list(template_id: str, org_id: str, **kwargs):
    url = f"/v1/{template_id}?org_id={org_id}"
    url = with_query(url, **kwargs)
    return _client.get(url)


def update(template_id: str, vm_id: str, org_id: str, body: dict, **kwargs):
    url = f"/v1/{template_id}/{vm_id}"
    if org_id:
        url += "?org_id=" + org_id
    url = with_query(url, **kwargs)
    return _client.patch(url, body)


def begin_adding_vms(template_id: str, org_id: str, vms: list, **kwargs):
    url = f"/v1/{template_id}/beginAddingVMs?org_id={org_id}"
    url = with_query(url, **kwargs)
    return _client.post(url, vms)


def finish_adding_vms(template_id: str, org_id: str, num_sessions: int, template_type: str, vms: list, **kwargs):
    url = f"/v1/{template_id}/finishAddingVMs?org_id={org_id}&numSessions={num_sessions}&templateType={template_type}"
    url = with_query(url, **kwargs)
    return _client.post(url, vms)
