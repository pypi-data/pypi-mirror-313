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
import click
from hcs_ext_azure.provider import _az_facade as az
from hcs_core.ctxp import choose
from hcs_core.sglib import cli_options
from hcs_ext_daas import helper, infra, order, order_util

log = logging.getLogger(__file__)


@click.command()
def update():
    cli_options.ensure_login()
    az.set_subscription(infra.get()["var"]["provider"]["subscriptionId"])
    orders = {k: v for k, v in order.get().items() if k != "deleted"}
    order_types = list(orders.keys())
    order_type = choose("Select order type to update:", order_types)
    # Start order update
    order_def_update = helper.prepare_order_definition(
        order_type, "v1/tenant-order.var.yml", _collect_info, orders[order_type]
    )

    order_def_update["var"]["edgeDeploymentId"] = orders[order_type]["edgeDeploymentId"]
    order_def_update["var"]["providerInstanceId"] = orders[order_type]["providerInstanceId"]
    order.add({order_def_update["orderType"]: order_def_update["var"]})


def _prompt(text: str, default=None, is_secret: bool = False) -> str:
    t = click.prompt(text=text, default=default, hide_input=is_secret, show_default=not is_secret)
    return t.strip()


def _collect_info(data):
    # _fill_info_from_infra()
    var = data["var"]
    order_util.configure_desktops(var)
    order_util.configure_apps(var)
