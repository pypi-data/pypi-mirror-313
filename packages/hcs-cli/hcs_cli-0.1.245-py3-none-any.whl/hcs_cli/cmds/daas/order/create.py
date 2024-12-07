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

import logging
import re
import click
from hcs_ext_azure.provider import _az_facade as az
from hcs_cli.service import admin
from hcs_core.ctxp import choose
from hcs_core.sglib import cli_options
from hcs_ext_daas import helper, infra, order, order_util

log = logging.getLogger(__file__)


@click.command()
def create():
    cli_options.ensure_login()
    az.set_subscription(infra.get()["var"]["provider"]["subscriptionId"])
    order_type = _input_order_type()
    order_def = helper.prepare_order_definition(order_type, "v1/tenant-order.var.yml", _collect_info)
    order.add({order_def["orderType"]: order_def["var"]})
    log.info("Successfully created order type '%s'", order_type)


def _prompt(text: str, default=None, is_secret: bool = False) -> str:
    t = click.prompt(text=text, default=default, hide_input=is_secret, show_default=not is_secret)
    return t.strip()


def _input_order_type():
    pattern = re.compile("^(?=.{3,16}$)[a-zA-Z0-9][a-zA-Z0-9_\\-]*$")
    orders = {k: v for k, v in order.get().items() if k != "deleted"}
    order_types = list(orders.keys())
    while True:
        order_type: str = click.prompt("Enter order type ", "tl-tenant-order1")
        order_type = order_type.strip()
        # if deployment_id.isidentifier():
        if not pattern.match(order_type):
            click.echo("Invalid input for order type. Enter between 3-16 characters with alphabet's, numbers, -, or _.")
            continue

        if order_type in order_types:
            click.echo("Order with same name exists. Use a different name.")
            continue

        if len(order_type) < 3:
            click.echo("Order with same name exists. Use a different name.")
            continue

        break
    return order_type


def _collect_info(data):
    # _fill_info_from_infra()
    var = data["var"]
    _select_edge(var)
    order_util.configure_desktops(var)
    order_util.configure_apps(var)


def _select_edge(var):
    org_id = var["orgId"]
    edges = admin.edge.list(org_id)
    titan_lite_infra = []
    edge_id = var["edgeDeploymentId"]
    prev_selected = None
    for s in edges:
        name = s["name"]
        if name.startswith("titanlite-"):
            titan_lite_infra.append(s)
            if edge_id == s["id"]:
                prev_selected = s

    fn_get_text = lambda s: f"{s['name']} ({s['hdc']['vmHub']['name']})"
    selected_edge = choose("Select edge", titan_lite_infra, fn_get_text, prev_selected)
    var["edgeDeploymentId"] = selected_edge["id"]
    var["providerInstanceId"] = selected_edge["providerInstanceId"]
