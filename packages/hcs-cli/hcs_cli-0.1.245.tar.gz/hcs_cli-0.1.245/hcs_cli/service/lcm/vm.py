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
from hcs_core.util.query_util import PageRequest, with_query

_client = hdc_service_client("lcm")
_crud = default_crud(_client, "/v1/capacity", "capacity")


def delete(template_id: str, vm_id: str, org_id: str, force: bool = True):
    return _client.delete(f"/v1/capacity/{template_id}/vms/{vm_id}?org_id={org_id}&force={force}")


def get(template_id: str, vm_id: str, org_id: str):
    return _client.get(f"/v1/capacity/{template_id}/vms/{vm_id}?org_id={org_id}")


def put(template_id: str, vm_id: str, org_id: str, payload):
    return _client.put(f"/v1/capacity/{template_id}/vms/{vm_id}?org_id={org_id}", payload)


def get_pairing_info(template_id: str, vm_id: str, **kwargs):
    url = with_query(f"/v1/capacity/{template_id}/vms/{vm_id}/pairing-info", **kwargs)
    return _client.post(url)


def power_on(template_id: str, vm_id: str, org_id: str):
    return _client.post(f"/v1/capacity/{template_id}/vms/{vm_id}/powerOn?org_id={org_id}")


def power_off(template_id: str, vm_id: str, org_id: str):
    return _client.post(f"/v1/capacity/{template_id}/vms/{vm_id}/powerOff?org_id={org_id}")


def restart(template_id: str, vm_id: str, org_id: str):
    return _client.post(f"/v1/capacity/{template_id}/vms/{vm_id}/restart?org_id={org_id}")


def shutdown(template_id: str, vm_id: str, org_id: str):
    return _client.post(f"/v1/capacity/{template_id}/vms/{vm_id}/shutdown?org_id={org_id}")
