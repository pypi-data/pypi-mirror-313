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
import re

from hcs_core.ctxp import choose, util as cli_util
from hcs_cli.service import admin
from hcs_core.sglib import cli_options
from hcs_ext_daas import helper, order

_context = {}


@click.command()
def plan():
    """Interactive command to plan a DaaS tenant.
    This command generates a plan file which can be deployed using 'hcs plan apply -f'.
    It is an alternative way to create a tenant. The generated plan file can be modified
    to provide more flexibility."""

    cli_options.ensure_login()

    deployment_id = _input_tenant_deployment_id()
    return helper.prepare_plan_file(deployment_id, "v1/tenant.blueprint.yml", _collect_info)


def _input_tenant_deployment_id():
    pattern = re.compile("^(?=.{2,7}$)[a-zA-Z0-9][a-zA-Z0-9\\-]*$")
    while True:
        deployment_id: str = click.prompt("Tenant unique deployment ID", "tenant1")
        deployment_id = deployment_id.strip()
        # if deployment_id.isidentifier():
        if pattern.match(deployment_id):
            break
        click.echo(
            "Invalid input for deployment id. Enter between 2-7 characters with alphabet's, numbers, or -(hyphen)."
        )
    return deployment_id


def _collect_info(data):
    var = data["var"]
    _select_edge(var)
    _select_order_type(var)
    _input_user_emails(var)


_edges = []


def _select_edge(var):
    org_id = var["orgId"]
    global _edges
    _edges = admin.edge.list(org_id)
    titan_lite_infra = []
    edge_id = var["edgeId"]
    prev_selected = None
    for s in _edges:
        name = s["name"]
        if name.startswith("titanlite-"):
            titan_lite_infra.append(s)
            if edge_id == s["id"]:
                prev_selected = s

    fn_get_text = lambda s: f"{s['name']} ({s['hdc']['vmHub']['name']})"
    selected_edge = choose("Select edge", titan_lite_infra, fn_get_text, prev_selected)
    var["edgeId"] = selected_edge["id"]
    _context["provider_instance_id"] = selected_edge["providerInstanceId"]


def _select_order_type(var: dict):
    orders = {k: v for k, v in order.get().items() if k != "deleted" and v["edgeDeploymentId"] == var["edgeId"]}
    order_types = list(orders.keys())

    def fn_get_text(order_type: str):
        o = orders[order_type]
        num_apps = len(o["application"]["info"])
        desc = f'{o["template"]["type"]}/{o["image"]["os"]},{o["image"]["gen"]}, apps: {num_apps}'
        ret = f"{order_type} ({desc})"
        return ret

    var["orderType"] = choose("Select order type:", order_types, fn_get_text=fn_get_text)
    var["order"] = orders.get(var["orderType"])


def _input_user_emails(data):
    data["userEmails"] = cli_util.input_array("User emails", default=data["userEmails"])
