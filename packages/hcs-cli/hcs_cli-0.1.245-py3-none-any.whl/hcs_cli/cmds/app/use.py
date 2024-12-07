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
from hcs_core.ctxp import recent
from hcs_core.sglib import cli_options as cli
from hcs_cli.service.app_management import manual_app
from hcs_cli.support import use_util


@click.command()
@click.argument("smart_search", type=str, required=False)
def use(smart_search: str):
    """Set or show the default object to work with."""

    if not smart_search:
        return recent.get("app")

    org_id = cli.get_org_id()

    items = manual_app.list(org_id)
    items = use_util.smart_search(items, smart_search)
    return use_util.require_single(items=items, resource_type="app")
