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
import hcs_core.sglib.cli_options as cli
from hcs_cli.service.vmhub import otp


@click.command()
@cli.org_id
@click.option(
    "--region",
    type=str,
    default=None,
    required=False,
    help="Specify region name",
)
@click.argument("resource-name", type=str, required=True)
def request(org: str, region: str, resource_name: str):
    """Request an one-time password for a specific resource"""
    org_id = cli.get_org_id(org)
    otp.use_region(region)
    return otp.request(org_id, resource_name)
