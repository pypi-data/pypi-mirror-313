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
from hcs_cli.service import ims
import hcs_core.sglib.cli_options as cli


@click.command()
@click.option("--image", "-i", type=str, required=False, help="Image ID")
@cli.org_id
def list(image: str, org: str, **kwargs):
    """List image versions"""

    org_id = cli.get_org_id(org)
    if image:
        return ims.version(image, org_id).list(**kwargs)

    images = ims.images.list(org_id)
    ret = []
    for i in images:
        image_id = i["id"]
        ret.extend(ims.version(image_id, org_id).list())
    return ret
