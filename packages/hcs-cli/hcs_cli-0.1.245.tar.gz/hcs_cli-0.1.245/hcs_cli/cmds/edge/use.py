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
from hcs_cli.service.admin import edge


@click.command()
@click.argument("smart_search", type=str, required=False)
@click.option("--interactive/--fail-on-multi-match", type=bool, required=False, default=True)
def use(smart_search: str, interactive: bool):
    "Helper command to work with a specific edge, by smart search."

    org_id = recent.require(None, "org")
    if not smart_search:
        return recent.get("edge")
    if use_util.looks_like_id(smart_search):
        ret = edge.list(org_id, search=f"id $eq {smart_search}")
    else:
        ret = edge.list(org_id, search=f"name $like '{smart_search}'")
        if not ret:
            ret = edge.list(org_id, search=f"description $like '{smart_search}")

    return use_util.require_single(items=ret, resource_type="edge", name_field="name", interactive=interactive)
