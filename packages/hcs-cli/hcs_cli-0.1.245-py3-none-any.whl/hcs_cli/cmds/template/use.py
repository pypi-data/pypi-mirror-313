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
from hcs_cli.support import use_util
from hcs_core.ctxp import recent
from hcs_core.sglib import cli_options as cli
from hcs_cli.service import admin


@click.command()
@cli.org_id
@click.argument("smart_search", type=str, required=False)
@click.option("--interactive/--fail-on-multi-match", type=bool, required=False, default=True)
def use(org: str, smart_search: str, interactive: bool):
    "Helper command to work with a specific template, by smart search."

    if not smart_search:
        return recent.get("template")
    org_id = cli.get_org_id(org)
    if use_util.looks_like_id(smart_search):
        ret = admin.template.get(smart_search, org_id)
    else:
        ret = admin.template.list(org_id, search=f"name $like '{smart_search}'")

    return use_util.require_single(items=ret, resource_type="template", interactive=interactive)
