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

import json
from typing import Any
from hcs_core.sglib.client_util import hdc_service_client

_client = hdc_service_client("lcm")


def get():
    return _client.get("/v1/health")


class template:
    @staticmethod
    def check_all(org_id: str):
        return _client.post(f"/v1/health/templates?org_id={org_id}")

    @staticmethod
    def check(org_id: str, template_id: str, **kwargs: Any):
        return _client.post(f"/v1/health/templates/{template_id}?org_id={org_id}")
