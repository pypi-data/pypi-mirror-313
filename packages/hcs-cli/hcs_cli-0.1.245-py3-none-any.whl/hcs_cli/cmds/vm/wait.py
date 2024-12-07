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
@click.option(
    "--property",
    "-p",
    type=str,
    required=False,
    help="Field and value to wait for. E.g. '-p powerState=PoweredOn,PoweredOff'. If not specified, wait for agent ready.",
)
@click.option("--timeout", "-t", type=str, required=False, default="5m", help="Timeout. Examples: '2m', '30s', '1h30m'")
@click.option(
    "--fail-fast/--fail-timeout",
    "-f",
    type=bool,
    default=True,
    required=False,
    help="Stop waiting if the template reached to non-expected terminal states, e.g. waiting for ERROR but template is READY, or waiting for READY and template is ERROR.",
)
def wait(vm_path: str, org: str, property: str, timeout: str, fail_fast: bool, **kwargs):
    """Wait for a specific VM.

    Examples:
        'hcs vm wait --property agentStatus=AVAILABLE,ERROR --timeout 5m',
        'hcs vm wait --property powerState=PoweredOn --timeout 30s'
    """
    org_id = cli.get_org_id(org)
    template_id, vm_id = parse_vm_path(vm_path)

    if property:
        field, expected_values = _parse_property_target(property)
    else:
        field = "agentStatus"
        expected_values = ["AVAILABLE"]

    vm = VM(org_id, template_id, vm_id)
    return vm.wait_for(field, expected_values=expected_values, timeout=timeout, fail_fast=fail_fast)


def _parse_property_target(property_arg: str):
    k, v = property_arg.split("=")
    return k, v.split(",")
