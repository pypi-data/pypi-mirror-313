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

from hcs_core.sglib.client_util import hdc_service_client, default_crud
from hcs_core.util.query_util import with_query, PageRequest

_client = hdc_service_client("org-service")
_crud = default_crud(_client, "/v1/org-details", "org-details")
# get = _crud.get
create = _crud.create
# list = _crud.list


def list(**kwargs):
    def _get_page(query_string):
        url = with_query(f"/v1/org-details?{query_string}")
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def get(org_id: str, **kwargs):
    url = with_query(f"/v1/org-details/{org_id}", **kwargs)
    return _client.get(url)


# def mark_for_deletion(org_id: str, **kwargs):
#     url = with_query(f"/v1/org-details/{org_id}/markedForDeletion", **kwargs)
#     return _client.patch(url, {})
