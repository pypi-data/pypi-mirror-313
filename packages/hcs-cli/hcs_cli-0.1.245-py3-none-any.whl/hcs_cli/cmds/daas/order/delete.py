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


@click.command()
def delete():
    if not order.get():
        raise Exception("No orders found to delete")

    orders = {k: v for k, v in order.get().items() if k != "deleted"}
    order_types = list(orders.keys())
    order_type = choose("Select order type to delete:", order_types)
    while True:
        query = input("Confirm deletion of order type '{}' with yes or no : ".format(order_type))
        if query == "" or not query.lower() in ["yes", "no"]:
            print("Please answer with yes or no!")
        else:
            break

    if query == "yes":
        order.remove(order_type)
        print(f"Successfully deleted order type {order_type}")
