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

_client = hdc_service_client("admin")


def list(label: str, org_id: str, **kwargs):
    def _get_page(query_string):
        url = f"/v2/providers/{label}/instances?org_id={org_id}&{query_string}"
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def get(label: str, id: str, org_id: str, **kwargs):
    url = f"/v2/providers/{label}/instances/{id}?org_id={org_id}"
    url = with_query(url, **kwargs)
    return _client.get(url)


def create(label: str, payload):
    return _client.post(f"/v2/providers/{label}/instances", json=payload)


def delete(label: str, id: str, org_id: str, **kwargs):
    url = f"/v2/providers/{label}/instances/{id}?org_id={org_id}"
    url = with_query(url, **kwargs)
    return _client.delete(url)


def list_golden_images(id: str, org_id: str, **kwargs):
    url = f"/v2/providers/vsphere/instances/{id}/golden-images?org_id={org_id}"
    url = with_query(url, **kwargs)
    return _client.get(url)


def list_vsphere_dcs(id: str, org_id: str, **kwargs):
    url = f"/v2/providers/vsphere/instances/{id}/datacenters?org_id={org_id}"
    url = with_query(url, **kwargs)
    return _client.get(url)
