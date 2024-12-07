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
from hcs_core.util.query_util import PageRequest
from hcs_core.util import hcs_constants

log = logging.getLogger(__name__)
_client = hdc_service_client("av-entitlements")


def create(payload: dict):
    url = hcs_constants.AV_CREATE_APP_ENTITLEMENT_API_URL
    return _client.post(url, payload)


def get_by_app_id(data: dict, **kwargs):
    _to_str = ",".join([str(elem) for elem in data.get("data")["apps"]])

    def _get_page(query_string):
        url = hcs_constants.AV_GET_ENTITLEMENT_API_URL
        return _client.get(url)

    return PageRequest(_get_page, search=f"applicationId $in {_to_str}").get()


def delete(state: dict):
    _l_entitlementIds = [str(_rec.get("id")) for _rec in state]
    delete_payload = {"data": {"appEntitlementIds": _l_entitlementIds}}
    url = hcs_constants.AV_DELETE_ENTITLEMENT_API_URL
    return _client.post(url, delete_payload)
