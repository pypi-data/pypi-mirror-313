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
from . import uag

_client = hdc_service_client("admin")


def list_resources_by_provider(resource_type: str, provider_instance_id: str, limit: int = 10, **kwargs):
    def _get_page(query_string):
        url = f"/v2/{resource_type}?" + query_string
        return _client.get(url)

    search = f"providerInstanceId $eq {provider_instance_id}"
    return PageRequest(_get_page, search=search, limit=limit, **kwargs).get()


def get_uags_by_edge(edge_id: str, org_id: str):
    uags = uag.list(org_id)
    ret = []
    for u in uags:
        if u["edgeDeploymentId"] == edge_id:
            ret.append(u)
    return ret
