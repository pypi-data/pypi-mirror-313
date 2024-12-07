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

import time
import httpx
from . import images, image_copies
from .version import version


def get_images_by_provider_instance_with_asset_details(providerInstanceId: str, org_id: str):
    all_images = images.list(org_id)
    copies = image_copies.list(
        org_id, include_catalog_details=True, search=f"providerInstanceId $eq {providerInstanceId}"
    )
    ret = []
    for copy in copies:
        imageId = copy["catalogDetails"]["imageId"]
        for image in all_images:
            if image["id"] == imageId:
                # add additional info
                image["_assetDetails"] = copy["assetDetails"]
                ret.append(image)
                break
    return ret


def delete_images(image_ids: list[str], org_id: str, timeout: str):
    def del_impl(image_id: str):
        version_api = version(image_id, org_id)
        versions = version_api.list()
        everything_ok = True
        for v in versions:
            s = v["status"]
            if s == "DELETING":
                continue
            # AVAILABLE, DELETING, DISABLED, FAILED, IMPORT_COMPLETE, IMPORT_IN_PROGRESS, PARTIALLY_AVAILABLE, PENDING, PUBLISH_IN_PROGRESS, REPLICATION_IN_PROGRESS
            try:
                version_api.delete(v["id"])
            except httpx.HTTPStatusError:
                everything_ok = False
        return everything_ok

    to_delete = list(image_ids)

    while True:
        temp = list(to_delete)
        for image_id in temp:
            if del_impl(image_id):
                to_delete.remove(image_id)
        if not to_delete:
            break
        time.sleep(60)

    if timeout == "0":
        return

    for image_id in image_ids:
        images.wait_for_deleted(image_id, org_id, timeout)  # todo: timeout
