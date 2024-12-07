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
import hcs_cli.service.scm as scm
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent


@click.command
def health():
    return scm.health()


@click.command
@cli.org_id
@click.argument("template-id", required=False)
def recommend_power_policy(org: str, template_id: str):
    org = cli.get_org_id(org)
    template_id = recent.require(template_id, "template")
    print(org, template_id)
    return scm.recommend_power_policy(org_id=org, template_id=template_id)
