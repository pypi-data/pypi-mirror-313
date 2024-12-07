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
from hcs_core.ctxp import recent


@click.command()
@click.option("--provider", "-p", type=str, required=False, help="Provider instance ID")
@click.option("--name", type=str, required=True, help="Name of the image to create")
@click.option("--vm-uuid", type=str, required=True, help="VM UUID from the MOID browser")
@click.option("--snapshot-id", type=str, required=True, help="Snapshot ID from the MOID browser")
@click.option("--multi-session/--vdi", type=bool, required=True)
@cli.org_id
def create(provider: str, name: str, vm_uuid: str, snapshot_id: str, multi_session: bool, org: str, **kwargs):
    """Create a gold pattern"""

    org_id = cli.get_org_id(org)
    provider = recent.require(provider, "provider")

    payload = {
        "goldPattern": {
            "providerInstanceId": provider,
            "orgId": org_id,
            "goldPatternDetails": {
                "method": "ByVsphereVmAndSnapshotUuid",
                "data": {
                    "imageName": name,
                    "snapshotId": snapshot_id,
                    "masterVmId": vm_uuid,
                    "cloneType": "Instant_Clone",
                    "osType": "WINDOWS",
                    "multiSession": multi_session,
                    "gpuType": "NONE",
                },
            },
        }
    }
    org_id = cli.get_org_id(org)
    ret = ims.gold_pattern.create(payload, org_id=org_id)
    if ret:
        recent.set("gold-pattern", ret["id"])
    return ret
