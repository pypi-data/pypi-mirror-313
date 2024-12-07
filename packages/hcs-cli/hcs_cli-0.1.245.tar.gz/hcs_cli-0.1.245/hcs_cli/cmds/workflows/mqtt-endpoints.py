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
import time
from hcs_cli.service import iss
from hcs_cli.service import admin
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path
from hcs_cli.service.org_service import details


@click.command(name="get-latest-mqtt-endpoints-allorgs")
@cli.limit
@cli.search
def get(**kwargs):
    allOrgs = details.list(org_id=None, **kwargs)
    # recent.helper.default_list(allOrgs, "org-details")
    print(f"There are {len(allOrgs)} orgs")
    failed = False
    for org in allOrgs:
        print(
            f"-- Processing org - id: {org.orgId}, name: {org.orgName}, cName: {org.customerName}, cType: {org.customerType}"
        )
        try:
            templates = admin.template.list(org_id=org.orgId, **kwargs)
            print(f" {org.orgId} has {len(templates)} templates")
            for t in templates:
                print(f" Get mqtt endpoints for template name: {t.name}")
                try:
                    ret = iss.mqtt.get(org.orgId, t.id, None)
                except Exception as err:
                    print(f"Unexpected {err=}, {type(err)=}")
                    failed = True
                print("\n")
                sleepSec = t.reportedStatus.provisionedVMs / 100
                print(
                    f"There are {t.reportedStatus.provisionedVMs} provisioned VMs, so sleep {sleepSec}s before next template"
                )
                time.sleep(sleepSec)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}, move on to next org. Hit CTRL+C or CMD+C to break")
            failed = True
            continue
        print("\n")

    return 1 if failed else 0
