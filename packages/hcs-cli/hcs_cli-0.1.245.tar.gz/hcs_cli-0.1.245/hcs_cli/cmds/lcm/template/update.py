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

import random
import click
import hcs_core.util.duration as duration
import hcs_cli.service.lcm as lcm
import hcs_core.sglib.cli_options as cli
import hcs_core.ctxp.data_util as data_util
from hcs_core.ctxp import recent


@click.command()
@click.argument("template_id", type=str, required=False)
@click.option(
    "--update",
    "-u",
    type=str,
    multiple=True,
    required=True,
    help="Specify field and value pair to update. E.g. '-f sparePolicy.max=3'.",
)
@cli.org_id
@cli.wait
def update(template_id: str, update, org: str, wait: str, **kwargs):
    """Update an existing template"""

    org_id = cli.get_org_id(org)

    template_id = recent.require(template_id, "template")
    template = lcm.template.get(template_id, org_id)

    if not template:
        return "Template not found: " + template_id

    need_update = False
    for u in update:
        k, v = u.split("=")
        current_value = data_util.deep_get_attr(template, k)
        if str(current_value) == str(v):
            continue
        data_util.deep_set_attr(template, k, v)
        need_update = True

    if not need_update:
        return template

    ret = lcm.template.update(template)
    if wait != "0":
        ret = lcm.template.wait(template_id, org_id, duration.to_seconds(wait))
    return ret


def _rand_id(n: int):
    return "".join(random.choices("abcdefghijkmnpqrstuvwxyz23456789", k=n))


def _create_zerocloud_provider(org_id: str):
    data = {"name": "nanw-test-" + _rand_id(4), "orgId": org_id, "type": "ZEROCLOUD"}

    return lcm.provider.create(data)
