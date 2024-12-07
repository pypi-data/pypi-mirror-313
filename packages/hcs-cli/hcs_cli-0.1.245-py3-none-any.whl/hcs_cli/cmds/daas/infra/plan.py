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
import hcs_core.ctxp as ctxp
from hcs_core.ctxp import choose
from hcs_ext_azure.provider import _az_facade as az
from hcs_ext_daas import infra, helper, cidr_util
from hcs_cli.service import admin
from hcs_core.sglib import cli_options

file_name = ".plan.yml"


@click.command()
def plan():
    """Interactive setup for shared infrastructure."""

    cli_options.ensure_login()

    deployment_id = _input_deployment_id()
    # modes = ["Create default infrastructure (automatic)", "Reuse existing infrastructure (manual)"]
    # mode = choose("Name of the infrastructure:", modes, selected=modes[0])

    # if mode == modes[0]:
    #     _create_default_infra(deployment_id)
    # else:
    #     _reuse_existing_infra(deployment_id)

    _create_default_infra(deployment_id)


def _input_deployment_id():
    pattern = re.compile("^[a-zA-Z0-9][a-zA-Z0-9_\\-]*$")
    while True:
        deployment_id = _prompt("Unique name of the infrastructure", default="starter1")
        # if deployment_id.isidentifier():
        if pattern.match(deployment_id):
            break
        click.echo("Invalid name ID. Use only alphabetics, numbers, -, or _.")
    return deployment_id


def _prompt(text: str, default=None, is_secret: bool = False) -> str:
    t = click.prompt(text=text, default=default, hide_input=is_secret, show_default=not is_secret)
    return t.strip()


def _create_default_infra(name):
    def collect_information(data):
        var = data["var"]
        org_id = var["orgId"]
        _select_region(var)
        _select_provider(var, org_id)
        _select_managed_identity(var)
        _input_vnet_cidr(var["network"])
        _config_desktop_default(var["desktop"])
        infra.set(data)

    return helper.prepare_plan_file(name, "v1/infra-green.blueprint.yml", collect_information)


def _reuse_existing_infra(name):
    def collect_information(data):
        var = data["var"]
        org_id = var["orgId"]
        _select_region(var)
        _select_provider(var, org_id)
        _select_managed_identity(var)
        _select_vnet(var["network"])
        _config_desktop_default(var["desktop"])
        infra.set(data)

    return helper.prepare_plan_file(name, "v1/infra-reuse.blueprint.yml", collect_information)


def _input_vnet_cidr(network):
    cidr: str = None
    while True:
        cidr = _prompt("vNet CIDR (/16):", default=network["cidr"] or "10.0.0.0/16")
        cidr = cidr.strip()
        reserved_cidrs = ["169.254.0.0/16", "172.30.0.0/16", "172.31.0.0/16", "192.0.2.0/24"]
        conflict, conflict_to = cidr_util.overlaps([cidr], reserved_cidrs)
        if conflict:
            click.echo("The specified CIDR conflicts to reserved CIDR " + conflict_to)
        else:
            break
    network["cidr"] = cidr


def _select_region(var):
    locations = az.locations()
    selected = None
    for loc in locations:
        if loc["name"] == "eastus":
            selected = loc
            break
    fn_get_text = lambda loc: loc["regionalDisplayName"] + f" ({loc['name']})"
    region = choose("Select location:", locations, fn_get_text, selected)
    var["region"] = region["name"]


def _select_managed_identity(var):
    identities = list(az.managed_identity_client().user_assigned_identities.list_by_subscription())
    fn_get_text = lambda i: i.name
    selected = choose("Select managed identity:", identities, fn_get_text)
    var["edge"]["managedIdentityId"] = selected.id


def _select_provider(var: dict, org_id: str):
    providers = admin.provider.list("azure", org_id)
    region = var["region"]
    filter_by_region = lambda p: p["providerDetails"]["data"]["region"] == region
    providers = list(filter(filter_by_region, providers))
    if providers:

        def _is_create_new(p):
            return isinstance(p, str)

        def fn_provider_text(p):
            if _is_create_new(p):
                return p
            return f"{p['providerDetails']['data']['region']}, {p['name']}/{p['id']}"

        providers.append("<Create New Provider>")
        p = choose("Select region and provider", providers, fn_provider_text)
        if not p:
            return
        if not _is_create_new(p):
            var["provider"]["id"] = p["id"]
            subscription_id = p["providerDetails"]["data"]["subscriptionId"]
            var["provider"]["subscriptionId"] = subscription_id
            az.set_subscription(subscription_id)
            return p
    else:
        click.echo(f"No provider configured for region {region}. Need to create a new provider.")
    del var["provider"]["id"]
    _input_azure_sp(var["provider"])


def _input_azure_sp(data):
    data["subscriptionId"] = _prompt("Azure subscription ID", default=data["subscriptionId"])
    data["directoryId"] = _prompt("Azure Directory ID", default=data["directoryId"])
    data["applicationId"] = _prompt("Azure service principle application ID", default=data["applicationId"])
    data["applicationKey"] = _prompt(
        "Azure service principle application key", default=data["applicationKey"], is_secret=True
    )

    az.login(data["applicationId"], data["applicationKey"], data["directoryId"])
    az.set_subscription(data["subscriptionId"])


def _select_vnet(data):
    vnets = az.network.vnet.list()
    fn_get_text = lambda vnet: f"{vnet['name']} ({','.join(vnet['addressSpace']['addressPrefixes'])})"
    vnet = choose("Select vNet:", vnets, fn_get_text)
    data["vNetId"] = vnet["id"]

    while True:
        tenant_cidrs = ctxp.util.input_array("Tenant CIDRs", default=data["tenantCIDRs"])
        if not tenant_cidrs:
            return
        err = _validate_cidr(tenant_cidrs, vnet["addressSpace"]["addressPrefixes"])
        if err:
            click.echo(err)
        else:
            break
    data["tenantCIDRs"] = tenant_cidrs


def _validate_cidr(input, limit):
    is_subnet, problem = cidr_util.subnets_of(input, limit)
    if not is_subnet:
        return f"The specified CIDR {problem} is not subnet of vNet address spaces: {limit}"
    reserved_cidrs = [
        "172.17.0.0/26",  # docker bridge
        "192.170.0.0/21",  # podCidr
        "192.169.0.0/27",  # serviceCidr
    ]
    overlap, problem = cidr_util.overlaps(input, reserved_cidrs)
    if overlap:
        return f"The specified address {problem} conflict to reserved address spaces: {reserved_cidrs}"


def _config_desktop_default(data):
    groups = az.aad.group.list()
    fn_get_text = lambda g: g["displayName"]
    prev = None
    for g in groups:
        if g["displayName"] == data["userGroup"]:
            prev = g
    click.echo(
        "To allow user login, they must have either 'Virtual Machine User Login' role or 'Virtual Machine Administrator Login' role."
    )
    selected = choose("Select a user group with one of the above roles:", groups, fn_get_text, selected=prev)
    data["userGroup"] = selected["displayName"]
