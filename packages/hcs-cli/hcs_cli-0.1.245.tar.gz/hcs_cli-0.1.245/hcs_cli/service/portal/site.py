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
from hcs_core.sglib.client_util import hdc_service_client
from hcs_core.util.query_util import with_query

log = logging.getLogger(__name__)
_client = hdc_service_client("portal")


def create(payload: dict):
    url = "/v2/sites"
    return _client.post(url, payload)


def get(id: str, org_id: str):
    url = f"/v2/sites/{id}?org_id={org_id}"
    return _client.get(url)


def list(**kwargs):
    url = with_query("/v2/sites", **kwargs)
    return _client.get(url)


def delete(id: str, org_id: str):
    url = f"/v2/sites/{id}?org_id={org_id}"
    return _client.delete(url)


def find_by_name(name: str, org_id: str):
    sites = list(org_id=org_id)
    for s in sites:
        if s.get("name") == name:
            return s


def set_edge(site_id: str, org_id: str, edge_deployment_id: str):
    url = f"/v1/sites/{site_id}/edge/{edge_deployment_id}"
    return _client.put(url, {})
