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
from hcs_core.util.query_util import PageRequest

_client = hdc_service_client("tsctl")


def list(namespace: str, search: str, **kwargs):
    def _get_page(query_string):
        url = f"/v1/namespaces/{namespace}/tasks?" + query_string
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def get(namespace: str, task_id: str, **kwargs):
    url = f"/v1/namespaces/{namespace}/tasks/{task_id}"
    return _client.get(url)


def delete(namespace: str, group: str, key: str):
    url = "/v1/operation/delete?force=true"
    body = {"group": group, "namespace": namespace, "taskKey": key}
    return _client.post(url, body)


def logs(namespace: str, **kwargs):
    def _get_page(query_string):
        url = f"/v1/namespaces/{namespace}/tasklog?" + query_string
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def lastlog(namespace: str, group: str, task_id: str, **kwargs):
    url = f"/v1/namespaces/{namespace}/groups/{group}/tasks/{task_id}/lastlog"
    return _client.get(url)
