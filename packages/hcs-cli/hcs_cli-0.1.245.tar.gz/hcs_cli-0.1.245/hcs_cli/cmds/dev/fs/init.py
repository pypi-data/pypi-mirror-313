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
import subprocess
from hcs_cli.service import org_service
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import profile


@click.command()
@cli.org_id
def init(org: str, **kwargs):
    """Init feature stack org, org details, and"""
    org_id = cli.get_org_id(org)
    feature_stack_url = profile.current().hcs.url

    _get_client_credential_from_secret_and_update_profile()
    _update_feature_stack(feature_stack_url)
    _init_org(org_id)
    _restart_services()


def _update_feature_stack(url):
    pass


def _get_client_credential_from_secret_and_update_profile():
    # TODO
    pass


def _init_org(org_id):
    feature_stack_url = profile.current().hcs.url
    payload1 = {
        "locations": ["US"],
        "geoLocation": {"coordinates": [-122.143936, 37.468319], "type": "Point"},
        "name": "feature-stack-dc",
        "regions": ["westus2", "eastus2", "westus", "eastus", "westus3", "us-west-1"],
        "providerRegions": {"aws": ["us-west-1"], "azure": ["westus2", "eastus2", "westus", "eastus", "westus3"]},
        "url": feature_stack_url,
        "edgeHubUrl": "https://horizonv2-em.devframe.cp.horizon.omnissa.com",
        "edgeHubRegionCode": "us",
        "dnsUris": [
            "/subscriptions/bfd75b0b-ffce-4cf4-b46b-ecf18410c410/resourceGroups/horizonv2-sg-dev/providers/Microsoft.Network/dnszones/featurestack.devframe.cp.horizon.omnissa.com"
        ],
        "vmHubs": [
            {
                "awsRegions": ["us-west-1"],
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


def exec(cmd):
    subprocess.call(cmd.split(" "))


def _restart_services():
    exec("kubectl rollout restart deployment portal-deployment")
    exec("kubectl rollout restart statefulset vmhub-statefulset")
    exec("kubectl rollout restart statefulset connection-service-statefulset")
    exec("kubectl rollout restart statefulset clouddriver-statefulset")
    exec("kubectl rollout restart deployment infra-vsphere-twin-deployment")


_services = [
    "ad-twin-deployment",
    "admin-deployment",
    "agent-manager-deployment",
    "aggregator-service-deployment",
    "aims-deployment",
    "app-catalog-deployment",
    "app-management-deployment",
    "appblast-deployment",
    "auth-deployment",
    "clouddriver-statefulset",
    "connection-service-statefulset",
    "consumption-deployment",
    "credentials-deployment",
    "deployer-deployment",
    "diagnostic-container-deployment",
    "egpu-azure-module-deployment",
    "egpu-azure-twin-deployment",
    "egpu-manager-deployment",
    "graphql-deployment",
    "image-engine-deployment",
    "images-deployment",
    "ims-catalog-deployment",
    "infra-azure-module-deployment",
    "infra-azure-twin-deployment",
    "infra-deployment",
    "infra-vsphere-discovery-deployment",
    "infra-vsphere-module-deployment",
    "infra-vsphere-twin-deployment",
    "inv-status-sync-deployment",
    "inventory-deployment",
    "kafka-standalone",
    "lcm-deployment",
    "license-features-deployment",
    "license-usage-tracker-deployment",
    "mongodb-standalone",
    "mqtt-server-0",
    "org-service-deployment",
    "pki-deployment",
    "portal-client-deployment",
    "portal-deployment",
    "provider-deployment",
    "redis-standalone",
    "rx-service-deployment",
    "scheduler-control-service-deployment",
    "sg-uag-module-deployment",
    "sg-uag-twin-deployment",
    "smart-capacity-management-deployment",
    "unmanaged-devices-deployment",
    "vims-deployment",
    "vm-manager-deployment",
    "vmhub-statefulset",
    "vsphere-partitions-deployment",
]

_service_dependency = {"lcm": ["inventory", "credentials"], "admin": ["lcm"], "portal": ["admin"]}


def _tailor(for_service: str):
    pass
