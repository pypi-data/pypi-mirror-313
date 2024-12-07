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

import click
import httpx
from hcs_cli.service import ims
import hcs_core.sglib.cli_options as cli


@click.command()
@click.option("--image", "-i", type=str, required=False, help="Image ID")
@click.argument("id", type=str, required=True)
@cli.org_id
@cli.wait
def delete(image: str, id: str, org: str, wait: str, **kwargs):
    """Delete image version by ID"""

    org_id = cli.get_org_id(org)
    if image:
        _delete_impl(image, id, org_id, wait)
    else:
        images = ims.images.list(org_id=org_id)
        for i in images:
            image_id = i["id"]
            v = ims.version(image_id, org_id)
            if v.get(id):
                return _delete_impl(image_id, id, org_id, wait)


def _delete_impl(image_id: str, version_id: str, org_id: str, wait: str):
    v = ims.version(image_id, org_id)
    ret = None
    try:
        ret = v.delete(version_id)
        if not ret:
            return
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 422:
            pass
        else:
            raise
    if wait == "0":
        return ret
    v.wait_for_deleted(version_id)
