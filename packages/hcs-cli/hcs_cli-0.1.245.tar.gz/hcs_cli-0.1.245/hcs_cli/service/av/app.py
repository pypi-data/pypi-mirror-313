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
from hcs_core.util import hcs_constants
from hcs_core.util.query_util import PageRequest
from hcs_core.util.query_util import with_query

log = logging.getLogger(__name__)
_client = hdc_service_client("av-appies")


def list_apps(org_id: str, **kwargs):
    def _get_page(query_string):
        url = hcs_constants.AV_GET_APPS_API_URL.format(query_string, org_id)
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def get_by_names(app_names: list, org_id: str, **kwargs):
    def _get_page(query_string):
        url = hcs_constants.AV_GET_APP_BY_NAME_API_URL.format(org_id, query_string)
        _names = ["'" + str(elem) + "'" for elem in app_names]
        _listToStr = ",".join(_names)
        url += hcs_constants.AV_GET_APP_BY_NAME_SEARCH_PARAM_API_URL + _listToStr
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def delete(app_name: str, org_id: str, **kwargs):
    _app_rec = get_by_names([app_name], org_id)
    if _app_rec:
        _app_id = _app_rec[0].get("id")
        url = hcs_constants.AV_DELETE_APP_API_URL.format(_app_id, org_id)
        url = with_query(url, **kwargs)
        return _client.delete(url, **kwargs)
