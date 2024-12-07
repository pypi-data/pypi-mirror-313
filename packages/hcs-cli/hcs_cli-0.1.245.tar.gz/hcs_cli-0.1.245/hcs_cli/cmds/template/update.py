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
import hcs_core.util.duration as duration
import hcs_cli.service.admin as admin
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent
from hcs_cli.support.patch_util import calculate_patch


@click.command()
@click.argument("template_id", type=str, required=False)
@click.option(
    "--update",
    "-u",
    type=str,
    multiple=True,
    required=True,
    help="Specify field and value pair to update. E.g. '-u sparePolicy.max=3'.",
)
@cli.org_id
@cli.wait
def update(template_id: str, update, org: str, wait: str, **kwargs):
    """Update an existing template"""

    org_id = cli.get_org_id(org)

    template_id = recent.require(template_id, "template")
    template = admin.template.get(template_id, org_id)

    if not template:
        return "Template not found: " + template_id

    allowed_fields = ["name", "description", "powerPolicy", "sparePolicy", "applicationProperties", "flags"]

    patch = calculate_patch(template, allowed_fields, update)

    if not patch:
        return template

    ret = admin.template.update(template_id, org_id, patch)
    if wait != "0":
        ret = admin.template.wait_for_ready(template_id, org_id, duration.to_seconds(wait))
    return ret
