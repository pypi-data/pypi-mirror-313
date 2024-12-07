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
from hcs_cli.service import admin, ims
from hcs_core.ctxp import choose, util as cli_util
from hcs_ext_daas import helper

_context = {}


@click.command(hidden=True)
def create():
    """Create a tenant from a configuration file.
    This command"""
    deployment_id = _input_tenant_deployment_id()
    """Interactive command to plan a DaaS tenant."""
    return helper.prepare_plan_file(deployment_id, "v1/tenant.blueprint.yml", _collect_info)


def _input_tenant_deployment_id():
    pattern = re.compile("^[a-zA-Z0-9][a-zA-Z0-9_\\-]*$")
    while True:
        deployment_id: str = click.prompt("Tenant unique deployment ID", "tenant1")
        deployment_id = deployment_id.strip()
        # if deployment_id.isidentifier():
        if pattern.match(deployment_id):
            break
        click.echo("Invalid deployment ID. Use only alphabetics, numbers, -, or _.")
    return deployment_id


def _collect_info(data):
    # _fill_info_from_infra()
    var = data["var"]
    _select_edge(var)
    _config_desktop(var)
    _input_user_emails(var)


def _select_edge(var):
    org_id = var["orgId"]
    edges = admin.edge.list(org_id)
    titan_lite_infra = []
    edge_id = var["edgeId"]
    prev_selected = None
    for s in edges:
        name = s["name"]
        if name.startswith("titanlite-"):
            titan_lite_infra.append(s)
            if edge_id == s["id"]:
                prev_selected = s

    fn_get_text = lambda s: f"{s['name']} ({s['hdc']['vmHub']['name']})"
    selected_edge = choose("Select edge", titan_lite_infra, fn_get_text, prev_selected)
    var["edgeId"] = selected_edge["id"]
    _context["provider_instance_id"] = selected_edge["providerInstanceId"]


def _config_desktop(var: dict):
    org_id = var["orgId"]

    def _select_image_and_vm_sku():
        images = ims.helper.get_images_by_provider_instance_with_asset_details(_context["provider_instance_id"], org_id)
        fn_get_text = lambda d: f"{d['name']}: {d['description']}"
        prev_selected_image = None
        if var["desktop"]["streamId"]:
            for i in images:
                if i["id"] == var["desktop"]["streamId"]:
                    prev_selected_image = i
                    break
        selected_image = choose("Select image:", images, fn_get_text, selected=prev_selected_image)
        var["desktop"]["streamId"] = selected_image["id"]

        fn_get_text = lambda m: f"{m['name']}"
        selected_marker = choose("Select marker:", selected_image["markers"], fn_get_text)
        var["desktop"]["markerId"] = selected_marker["id"]

        image_asset_details = selected_image["_assetDetails"]["data"]

        # search = f"capabilities.HyperVGenerations $in {image_asset_details['generationType']}"
        # vm_skus = admin.azure_infra.get_compute_vm_skus(data['provider']['id'], limit=200, search=search)
        # prev_selected_vm_sku = None
        # if data['desktop']['vmSkuName']:
        #     selected_vm_sku_name = data['desktop']['vmSkuName']
        # else:
        #     selected_vm_sku_name = image_asset_details['vmSize']
        # if selected_vm_sku_name:
        #     for sku in vm_skus:
        #         if sku['id'] == selected_vm_sku_name:
        #             prev_selected_vm_sku = sku
        #             break

        # fn_get_text = lambda d: f"{d['data']['name']} (CPU: {d['data']['capabilities']['vCPUs']}, RAM: {d['data']['capabilities']['MemoryGB']})"

        # selected = choose("Select VM size:", vm_skus, fn_get_text, selected=prev_selected_vm_sku)
        # data['desktop']['vmSkuName'] = selected['data']['name']
        var["desktop"]["vmSkuName"] = image_asset_details["vmSize"]

    def _select_desktop_type():
        types = ["FLOATING", "MULTI_SESSION"]
        var["desktop"]["templateType"] = choose("Desktop type:", types)

    _select_image_and_vm_sku()
    _select_desktop_type()


def _input_user_emails(data):
    data["userEmails"] = cli_util.input_array("User emails", default=data["userEmails"])
