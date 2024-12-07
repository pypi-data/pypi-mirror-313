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

import builtins
from hcs_core.sglib.client_util import hdc_service_client, default_crud, wait_for_res_status
from hcs_core.util.query_util import PageRequest

_imagemgmt_client = hdc_service_client("imagemgmt")
_ims_catalog_client = hdc_service_client("ims-catalog")
_crud = default_crud(_ims_catalog_client, "/v1/images", "image")

list = _crud.list
get = _crud.get
delete = _crud.delete
wait_for_deleted = _crud.wait_for_deleted


def create(action: str, image_catalog_request: dict):
    # https://cloud-sg.horizon.vmware.com/images/swagger-ui/index.html#/Images/createImageCatalogUsingPOST

    # POST https://cloud-sg.horizon.vmware.com/imagemgmt/v1/images?action=import
    return _imagemgmt_client.post("/v1/images?action=" + action, image_catalog_request)


def wait_for(image_id: str, org_id: str, expected_status):
    res_name = "image/" + image_id
    fn_get = lambda: get(image_id, org_id)
    unexpected_status = set(
        [
            "IMPORT_COMPLETE",
            "AVAILABLE",
            "FAILED",
            "DELETING",
            "DISABLED",
            "REPLICATION_IN_PROGRESS",
            "PARTIALLY_AVAILABLE",
        ]
    )
    status_map = {
        "ready": expected_status,
        "transition": ["IN_PROGRESS", "PUBLISH_IN_PROGRESS", "PENDING"],
        "error": builtins.list(unexpected_status - set(expected_status)),
    }
    return wait_for_res_status(
        resource_name=res_name, fn_get=fn_get, get_status="status", status_map=status_map, timeout="60m"
    )
