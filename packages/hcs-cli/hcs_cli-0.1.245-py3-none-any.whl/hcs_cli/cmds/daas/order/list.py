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
from hcs_core.ctxp import choose
from hcs_ext_daas import order

_context = {}
log = logging.getLogger(__file__)


@click.command("list")
@click.option("--interactive/--program", "-i", type=bool, default=False, help="Interactive list")
@click.option("--all/--no-all", type=bool, default=False, help="Optionally, include all deleted orders too")
def list_orders(interactive: bool, all: bool):
    all_orders = order.get()
    orders = {k: v for k, v in all_orders.items() if k != "deleted"}
    if all and all_orders.get("deleted"):
        for deleted_order in all_orders.get("deleted"):
            for k, v in deleted_order.items():
                orders[k + "-deleted-" + v["deleted_at"]] = v

    if interactive:
        if not orders:
            print("No orders found")
            return

        order_types = list(orders.keys())
        order_type = choose("Select order type to view:", order_types)
        return orders[order_type]
    else:
        return orders
