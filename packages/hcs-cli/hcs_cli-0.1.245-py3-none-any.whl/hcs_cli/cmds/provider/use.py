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
from hcs_cli.service.admin import provider
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.constant import provider_labels


@click.command()
@click.argument("smart_search", type=str, required=False)
@click.option("--interactive/--fail-on-multi-match", type=bool, required=False, default=True)
def use(smart_search: str, interactive: bool):
    "Helper command to work with a specific object, by smart search."

    org_id = cli.get_org_id()

    if not smart_search:
        return recent.get("provider")

    ret = _list_all(org_id)
    ret = use_util.smart_search(ret, smart_search)
    return use_util.require_single(items=ret, resource_type="provider", name_field="name", interactive=interactive)


def _list_all(org_id: str):
    # list all
    ret = []
    for label in provider_labels:
        ret += provider.list(label, org_id)
    return ret
