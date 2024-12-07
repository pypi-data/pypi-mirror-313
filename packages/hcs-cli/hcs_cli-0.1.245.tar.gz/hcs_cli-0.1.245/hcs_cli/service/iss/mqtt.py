"""
Copyright 2023-2024 Omnissa Inc.
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
from hcs_core.sglib.client_util import hdc_service_client
from hcs_core.util.query_util import with_query, PageRequest

_client = hdc_service_client("inv-status-sync")


def get(org_id: str, template_id: str, vm_id: str, **kwargs):
    url = f"/v1/ops/get-mqtt-endpoints"
    verbose = kwargs.pop("verbose", False)
    url = with_query(url, **kwargs)

    payloadBodyCmn = f'''
        "orgId" : "{org_id}",
        "templateId" : "{template_id}"'''

    payloadBody = (
        f'''{payloadBodyCmn},
        "vmId" : "{vm_id}"'''
        if vm_id
        else payloadBodyCmn
    )

    payload = f"""
    {{
        {payloadBody}
    }}
    """
    if verbose:
        print(f"POST: {url}")
        print(payload)

    payloadJson = json.loads(payload)
    return _client.post(url, payloadJson)


def update(org_id: str, template_id: str, vm_id: str, udpate_type: str, force_edge: bool, **kwargs):
    url = f"/v1/ops/update-mqtt-endpoints"
    verbose = kwargs.pop("verbose", False)
    url = with_query(url, **kwargs)

    payloadBodyCmn = f'''
        "orgId" : "{org_id}",
        "templateId" : "{template_id}",
        "forceEdge" : "{force_edge}",
        "updateType" : "{udpate_type}"'''

    payloadBody = (
        f'''{payloadBodyCmn},
        "vmId" : "{vm_id}"'''
        if vm_id
        else payloadBodyCmn
    )

    payload = f"""
    {{
        {payloadBody}
    }}
    """
    if verbose:
        print(f"POST: {url}")
        print(payload)
    payloadJson = json.loads(payload)
    return _client.post(url, payloadJson)
