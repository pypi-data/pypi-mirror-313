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
from hcs_core.sglib.client_util import hdc_service_client, default_crud

log = logging.getLogger(__name__)
_client = hdc_service_client("portal")
_crud = default_crud(_client, "/v3/pools", "pool")

create = _crud.create
get = _crud.get
update = _crud.update


def list(org_id: str, exclude_disabled_pools: bool = False, include_internal_pools: bool = True, **kwargs):
    return _crud.list(
        org_id, exclude_disabled_pools=exclude_disabled_pools, include_internal_pools=include_internal_pools, **kwargs
    )


def delete(id: str, org_id: str, delete: bool = True, disassociateAction: str = "FORCEFUL", **kwargs):
    return _crud.delete(id, org_id, delete=delete, disassociateAction=disassociateAction, **kwargs)
