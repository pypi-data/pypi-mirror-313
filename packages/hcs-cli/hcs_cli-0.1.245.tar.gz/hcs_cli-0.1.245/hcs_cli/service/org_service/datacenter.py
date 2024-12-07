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

_client = hdc_service_client("org-service")


def get(id: str, **kwargs):
    url = with_query(f"/v1/datacenters/{id}", **kwargs)
    return _client.get(url)


def list(**kwargs):
    url = with_query(f"/v1/datacenters", **kwargs)
    return _client.get(url)


def create(payload):
    url = "/v1/datacenters"
    return _client.post(url, payload)


def find_by_org(orgId, **kwargs):
    url = with_query(f"/v1/datacenters/orgs/{orgId}", **kwargs)
    return _client.get(url)
