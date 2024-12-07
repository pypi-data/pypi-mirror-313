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

import base64
from hcs_core.sglib.client_util import regional_service_client

_region_name = None


def use_region(region_name: str):
    global _region_name
    _region_name = region_name


def _client():
    return regional_service_client(_region_name, "vmhub")


def request(org_id: str, resource_name: str) -> str:
    mqtt_endpoint_request = {
        # 'mqttEndpoint': '',
        "orgId": org_id,
        "vmId": resource_name,
    }
    ret = _client().post("/credentials/generate-otp", mqtt_endpoint_request)
    return ret


def redeem(resource_name: str, otp: str, csr: str):
    base64_encoded_csr = base64.b64encode(csr.encode("ascii")).decode("ascii")

    credentials_request = {"vmId": resource_name, "otp": otp, "clientCsr": base64_encoded_csr}
    return _client().post("/credentials", credentials_request)
