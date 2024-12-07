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

from hcs_core.sglib.client_util import hdc_service_client, wait_for_res_deleted, wait_for_res_status
from hcs_core.util.query_util import PageRequest, with_query

_imagemgmt_client = hdc_service_client("imagemgmt")
_ims_catalog_client = hdc_service_client("ims-catalog")


class version:
    def __init__(self, image_id: str, org_id: str):
        self._image_id = image_id
        self._org_id = org_id

    def get(self, id: str, **kwargs):
        url = with_query(f"/v1/images/{self._image_id}/versions/{id}?org_id={self._org_id}", **kwargs)
        return _ims_catalog_client.get(url)

    def list(self, **kwargs):
        def _get_page(query_string):
            url = f"/v1/images/{self._image_id}/versions?org_id={self._org_id}&" + query_string
            return _ims_catalog_client.get(url)

        return PageRequest(_get_page, **kwargs).get()

    # def create(image_id: str, payload: dict, org_id: str, **kwargs):
    #     url = f"/v1/images/{image_id}/versions?org_id={org_id}"
    #     url = with_query(url, **kwargs)
    #     return _client.post(url, json=payload)

    def delete(self, id: str, **kwargs):
        url = with_query(f"/v1/images/{self._image_id}/versions/{id}?org_id={self._org_id}", **kwargs)
        return _imagemgmt_client.delete(url)

    def wait_for_deleted(self, id: str, timeout: str = "10m"):
        name = "image_version/" + id

        def fn_get():
            return self.get(id)

        return wait_for_res_deleted(name, fn_get, timeout)

    def publish(self, id: str, version_publish_create_TO: dict):
        # https://cloud-sg.horizon.vmware.com/images/swagger-ui/index.html#/Images/publishVersionV2UsingPOST
        if version_publish_create_TO["orgId"] != self._org_id:
            raise Exception(
                f"Invalid payload. version_publish_create_TO orgId {version_publish_create_TO['orgId']} does not match API context {self._org_id}"
            )
        url = f"/v1/images/{self._image_id}/versions/{id}?action=publish"
        return _imagemgmt_client.post(url, version_publish_create_TO)

    def wait_for_publish_complete(self, id: str, timeout: str = "40m"):
        res_name = "version/" + id

        def fn_get():
            return self.get(id)

        status_map = {
            "ready": ["AVAILABLE"],
            "transition": [
                "IMPORT_COMPLETE",
                "IMPORT_IN_PROGRESS",
                "PENDING",
                "PUBLISH_IN_PROGRESS",
                "REPLICATION_IN_PROGRESS",
            ],
            "error": ["FAILED", "DELETING", "DISABLED", "PARTIALLY_AVAILABLE"],
        }
        wait_for_res_status(
            resource_name=res_name, fn_get=fn_get, get_status="status", status_map=status_map, timeout=timeout
        )
