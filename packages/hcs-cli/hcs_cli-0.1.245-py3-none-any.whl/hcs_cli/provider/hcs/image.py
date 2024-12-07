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

from hcs_cli.service import ims
from hcs_core.plan import actions
import time


def deploy(data: dict, state: dict, save_state) -> dict:
    image_catalog_request = data["import"]
    version_publish_create_TO = data["publish"]
    org_id = image_catalog_request["orgId"]
    img = refresh(data, state)

    if not img:
        image_catalog_representation = ims.images.create("import", image_catalog_request)
        stream_id = image_catalog_representation["streamId"]
        # The IMS API does not follow REST convention and has inconsistent return model
        # between the creation API and read APIs.
        # https://jira.eng.vmware.com/browse/HV-78267
        img = ims.images.get(stream_id, org_id)
    save_state(img)
    image_id = img["id"]

    img = ims.images.wait_for(image_id, org_id, ["IMPORT_COMPLETE", "AVAILABLE"])
    save_state(img)
    status = img["status"]
    if status == "IMPORT_COMPLETE":
        time.sleep(60)
        version_api = ims.version(image_id, org_id)
        versions = version_api.list()
        if not versions:
            raise Exception("No version found for image " + image_id)
        version_id = versions[0]["id"]
        version_api.publish(version_id, version_publish_create_TO)
        ims.images.wait_for(image_id, org_id, ["AVAILABLE"])
    elif status == "AVAILABLE":
        pass
    else:
        raise Exception("Broken logic. This is a regression.")
    return ims.images.get(image_id, org_id)


def refresh(data: dict, state: dict) -> dict:
    org_id = data["import"]["orgId"]
    img = None
    if state:
        image_id = state["id"]
        img = ims.images.get(image_id, org_id)
    if not img:
        existing_images = ims.images.list(org_id, search="name $eq " + data["import"]["streamName"])
        if existing_images:
            img = existing_images[0]
    return img


def decide(data: dict, state: dict):
    status = state["status"]
    status_to_action = {
        "AVAILABLE": actions.skip,
        "IMPORT_COMPLETE": actions.create,
        "DELETING": actions.recreate,
        "DISABLED": actions.recreate,
        "FAILED": actions.recreate,
        "IMPORT_COMPLETE": actions.create,
        "IN_PROGRESS": actions.create,
        "PARTIALLY_AVAILABLE": actions.skip,
        "PENDING": actions.create,
    }
    action = status_to_action.get(status)
    if not action:
        raise Exception(f"Unknown image status: {status}")
    return action


def destroy(data: dict, state: dict, force: bool) -> dict:
    org_id = data["import"]["orgId"]
    image_id = state["id"]
    ims.helper.delete_images([image_id], org_id, "15m")


def eta(action: str, data: dict, state: dict):
    if action == actions.create:
        return "60m"
    # when the image is in-process creating/publishing, the deletion needs
    # to start after the image is ready (at least with IMS today), which could take a considerable time.
    if action == actions.delete:
        return "60m"
