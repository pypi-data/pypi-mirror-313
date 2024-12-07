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
import hcs_cli.service.org_service as org_service
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import profile


@click.command()
@cli.org_id
def initfs(org: str, **kwargs):
    """Init feature stack org, org details, and"""
    org_id = cli.get_org_id(org)

    feature_stack_url = profile.current().hcs.url
    payload1 = {
        "locations": ["US"],
        "geoLocation": {"coordinates": [-122.143936, 37.468319], "type": "Point"},
        "name": "feature-stack-dc",
        "regions": ["westus2", "eastus2", "westus", "eastus", "westus3"],
        "url": feature_stack_url,
        "edgeHubUrl": "https://horizonv2-em.devframe.cp.horizon.vmware.com",
        "edgeHubRegionCode": "us",
        "dnsUris": [
            "/subscriptions/bfd75b0b-ffce-4cf4-b46b-ecf18410c410/resourceGroups/horizonv2-sg-dev/providers/Microsoft.Network/dnszones/kedar.devframe.cp.horizon.vmware.com"
        ],
        "vmHubs": [
            {
                "azureRegions": ["westus2", "eastus2", "westus", "eastus", "westus3"],
                "name": "default",
                "url": feature_stack_url,
                "vmHubGeoPoint": {"type": "Point", "coordinates": [-132.143936, 38.468319]},
                "privateLinkServiceIds": [
                    "/subscriptions/bfd75b0b-ffce-4cf4-b46b-ecf18410c410/resourceGroups/horizonv2-sg-dev/providers/Microsoft.Network/privateLinkServices/vernemq-featurestack"
                ],
            }
        ],
    }
    try:
        ret = org_service.datacenter.create(payload1)
        print(ret)
    except Exception as e:
        print(e)

    payload2 = {
        "customerName": "nanw-dev",
        "customerType": "INTERNAL",
        "orgId": org_id,
        "wsOneOrgId": "pseudo-ws1-org-id",
    }
    try:
        ret = org_service.details.create(payload2)
        print(ret)
    except Exception as e:
        print(e)

    payload3 = {"location": "US", "orgId": org_id}
    try:
        ret = org_service.orglocationmapping.create(payload3)
        print(ret)
    except Exception as e:
        print(e)
