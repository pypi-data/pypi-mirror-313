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

log = logging.getLogger(__name__)
_client = hdc_service_client("clouddriver")


def summary():
    return _client.get("/v1/providers/summary")


def info(provider: str):
    return _client.get(f"/v1/providers/{provider}/info")


def release(provider: str):
    return _client.delete(f"/v1/providers/{provider}")


def list_all(provider: str):
    return _client.post(f"/v1/providers/{provider}/tasks", [])


def get(provider: str, task_id: str):
    return _client.get(f"/v1/providers/{provider}/tasks/{task_id}")


def delete(provider: str, task_id: str):
    return _client.delete(f"/v1/providers/{provider}/tasks/{task_id}")
