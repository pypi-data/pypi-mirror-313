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
from hcs_cli.service.admin import VM
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def poweron(vm_path: str, org: str, wait: str, **kwargs):
    """Power on a VM."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    data = vm.get()
    if not data:
        return "VM not found", 1
    state = data["powerState"]
    if state == "PoweredOn":
        return data

    if state != "PoweringOn":
        vm.power_on()

    if wait == "0":
        return data
    return vm.wait_for_power_status("PoweredOn", wait)


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def poweroff(vm_path: str, org: str, wait: str, **kwargs):
    """Power off a VM."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    data = vm.get()
    state = data["powerState"]
    if state == "PoweredOff":
        return data

    if state != "PoweringOff":
        vm.power_off()

    if wait == "0":
        return data

    return vm.wait_for_power_status("PoweredOff", wait)


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def restart(vm_path: str, org: str, wait: str, **kwargs):
    """Restart a VM."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    vm.restart()

    if wait != "0":
        return vm.wait_for_power_status("PoweredOn", wait)
    return vm.get()


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def shutdown(vm_path: str, org: str, wait: str, **kwargs):
    """Shutdown a VM."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    vm.shutdown()

    if wait != "0":
        return vm.wait_for_power_status("PoweredOff", wait)
    return vm.get()


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def resize(vm_path: str, org: str, wait: str, **kwargs):
    """Resize a VM."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    vm.resize()

    if wait != "0":
        print("TODO: wait")

    return vm.get()


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def rebuild(vm_path: str, org: str, wait: str, **kwargs):
    """Rebuild a VM."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    vm.rebuild()

    if wait != "0":
        print("TODO: wait")
    return vm.get()


@click.command()
@click.argument("vm_path", type=str, required=False)
@cli.org_id
@cli.wait
def pair(vm_path: str, org: str, wait: str, **kwargs):
    """Retry pairing of the VM agent."""
    template_id, vm_id = parse_vm_path(vm_path)
    org_id = cli.get_org_id(org)
    vm = VM(org_id, template_id, vm_id)

    vm.pair()
    if wait != "0":
        print("TODO: wait")

    return vm.get()
