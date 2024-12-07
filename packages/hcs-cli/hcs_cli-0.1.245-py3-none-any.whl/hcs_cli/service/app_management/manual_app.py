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
from hcs_core.sglib.client_util import hdc_service_client, default_crud

_client = hdc_service_client("app-management")
_crud = default_crud(_client, "/v1/apps/manual", "apps/manual")
get = _crud.get
list = _crud.list
delete = _crud.delete


def create(application: dict, icon=None):
    text = json.dumps(application)
    files = {"application": ("application", text, "application/json")}
    return _crud.upload(files=files)
