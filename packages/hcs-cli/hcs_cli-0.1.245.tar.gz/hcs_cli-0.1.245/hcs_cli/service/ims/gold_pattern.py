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

from httpx import HTTPStatusError
from hcs_core.sglib.client_util import hdc_service_client, default_crud, wait_for_res_status
from hcs_core.util.query_util import PageRequest

_client = hdc_service_client("images")
_crud_vsphere = default_crud(_client, "/v1/vsphere/gold-patterns", "gold-patterns")
_crud_nutanix = default_crud(_client, "/v1/nutanix/gold-patterns", "gold-patterns")


def _raise_if_unsupported_provider_error(ex):
    if not isinstance(ex, HTTPStatusError):
        raise ex
    if not ex.response:
        raise ex
    content = ex.response.text
    if not content or content.find("UNSUPPORTED_PROVIDER") < 0:
        raise ex


def get(id: str, org_id: str, **kwargs):
    ret = _crud_vsphere.get(id, org_id, **kwargs)
    try:
        if not ret:
            _crud_nutanix.get(id, org_id, **kwargs)
    except Exception as e:
        _raise_if_unsupported_provider_error(e)
        # else pass

    return _formalize_gold_pattern_model(ret)


def list(org_id: str, **kwargs):
    ret1 = _crud_vsphere.list(org_id, **kwargs)
    try:
        ret2 = _crud_nutanix.list(org_id, **kwargs)
    except HTTPStatusError as e:
        _raise_if_unsupported_provider_error(e)
        # else pass
        ret2 = []

    ret3 = []
    for r in ret1:
        ret3.append(_formalize_gold_pattern_model(r))
    for r in ret2:
        ret3.append(_formalize_gold_pattern_model(r))
    return ret2


def create(payload: dict, **kwargs):
    if _is_nutanix(payload):
        ret = _crud_nutanix.create(payload, **kwargs)
    else:
        ret = _crud_vsphere.create(payload, **kwargs)
    return _formalize_gold_pattern_model(ret)


def delete(**kwargs):
    _crud_vsphere.delete(**kwargs)
    try:
        _crud_nutanix.delete(**kwargs)
    except Exception as e:
        _raise_if_unsupported_provider_error(e)
        # else pass


def _formalize_gold_pattern_model(data):
    if data:
        return data["goldPattern"]
    return data


def _is_nutanix(payload):
    method = payload["goldPattern"]["goldPatternDetails"]["method"]
    return method.lower().find("nutanix") >= 0
