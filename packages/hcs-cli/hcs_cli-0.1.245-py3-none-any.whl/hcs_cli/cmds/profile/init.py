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
from hcs_core.ctxp import profile, panic
import hcs_cli.support.profile as profile_support


@click.command()
@click.option("--name", "-n", type=str, required=False, help="Name of the profile, if a non-default one is needed.")
@click.option("--dev/--no-dev", type=bool, default=False, help="Initialize default development profiles.")
@click.option("--feature-stack", "-fs", type=str, required=False, help="A profile for feature stack.")
@click.option("--org", type=str, required=False, help="Set initial property")
@click.option("--client-id", type=str, required=False, help="Set initial property")
@click.option("--client-secret", type=str, required=False, help="Set initial property")
@click.option("--api-token", type=str, required=False, help="Set initial property")
def init(name: str, dev: bool, feature_stack: str, org: str, client_id: str, client_secret: str, api_token: str):
    """Init profile.

    Examples:

        hcs profile init --name lab

        hcs profile init --feature-stack <name> --org <orgId> --client-id <id> --client-secret <secret>
    """

    profile_support.ensure_default_production_profile()

    def _override(data: dict):
        csp = data["csp"]
        if org:
            csp["orgId"] = org
        if client_id:
            csp["clientId"] = client_id
        if client_secret:
            csp["clientSecret"] = client_secret
        if api_token:
            csp["apiToken"] = api_token
        return data

    data = None
    if feature_stack:
        if not name:
            name = feature_stack
        data = profile_support.get_dev_profile_template()
        url = f"https://{feature_stack}.fs.devframe.cp.horizon.omnissa.com"
        data["hcs"]["url"] = url
        for r in data["hcs"]["regions"]:
            r["url"] = url
    elif name:
        data = profile_support.get_default_profile_template()
    if data:
        data = _override(data)
        profile.create(name, data, overwrite=True)
        return

    if dev:
        profile_support.ensure_dev_profiles()
        print()
        print("Next step:")
        print("  'hcs profile --help' : to know profile operations.")
        print("  'hcs profile use'    : to swtich profile.")
        print("  'hcs login --help'   : to complete authentication for the current profile.")
        return

    panic("Specify the target profile name by --name")
