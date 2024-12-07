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
import json
import logging
import time
from hcs_cli.service import iss
from hcs_cli.service import tsctl
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.param_util import parse_vm_path


@click.command(name="get-mqtt-endpoint")
@click.argument("target_org_id", type=str, required=True)
@click.argument("template_id", type=str, required=False)
@click.option("--vm_id", type=str, required=False)
@click.option("--wait", type=bool, required=False)
@click.option("--verbose", "--v", type=bool, is_flag=True, required=False)
def get(target_org_id: str, template_id: str, vm_id: str, wait: bool, verbose: bool):
    """Get template VM by path, e.g., template1/vm1."""

    print(f"Initiate get mqtt endpoint task for org: {target_org_id}, tmpl: {template_id}, vm: {vm_id}")
    ret = iss.mqtt.get(target_org_id, template_id, vm_id, **{"verbose": verbose})
    if verbose:
        print(f"{ret.status_code} - {ret}")

    if not ret:
        return "", 1
    if wait:
        while True:
            time.sleep(10)
            taskStatus = tsctl.task.lastlog(ret.namespace, ret.group, ret.taskKey)
            if "state" in taskStatus and taskStatus.state == "Error":
                print(f"Task is in {taskStatus.state} state - {taskStatus.error} ")
                print(json.dumps(taskStatus, indent=2))
                break
            if ("state" in taskStatus and taskStatus != "") or not "state" in taskStatus:
                continue
            print(json.dumps(taskStatus, indent=2))
            break
    print("Check values on HOC dashboard or in inventory db browser")
    return ret


@click.command(name="update-mqtt-endpoint")
@click.argument("target_org_id", type=str, required=True)
@click.argument("template_id", type=str, required=False)
@click.option("--vm_id", "--vm", type=str, required=False)
@click.option(
    "--update-type", "--u", type=click.Choice(["both", "regional", "edge"]), default="both", show_default=True
)
@click.option("--force_edge", "--fe", type=bool, is_flag=True, required=False)
@click.option("--wait", "--w", type=bool, is_flag=True, required=False)
@click.option("--verbose", "--v", type=bool, is_flag=True, required=False)
def update(
    target_org_id: str, template_id: str, vm_id: str, update_type: str, force_edge: bool, wait: bool, verbose: bool
):
    """Get template VM by path, e.g., template1/vm1."""

    print(
        f"Initiate get mqtt endpoint task for org: {target_org_id}, tmpl: {template_id}, vm: {vm_id}, update-type:{update_type}, forceEdge: {force_edge} "
    )
    try:
        ret = iss.mqtt.update(target_org_id, template_id, vm_id, update_type, force_edge, **{"verbose": verbose})

        if verbose:
            print(f"{ret.status_code} - {ret}")

        if not ret:
            return "", 1

        if wait:
            while True:
                time.sleep(10)
                taskStatus = tsctl.task.lastlog(ret.namespace, ret.group, ret.taskKey)
                if "state" in taskStatus and taskStatus.state == "Error":
                    print(f"Task is in {taskStatus.state} state - {taskStatus.error} ")
                    print(json.dumps(taskStatus, indent=2))
                    break
                if ("state" in taskStatus and taskStatus != "") or not "state" in taskStatus:
                    continue
                print(json.dumps(taskStatus, indent=2))
                break

    except Exception as e:
        print(e)
        return "", 1
    print(
        """Update mqtt endpoint task has been initiated. 
          Call get-mqtt-endpoint after a delay of few minutes to refresh mqtt endpoints in inventory db.
          Check values and errors on HOC dashboard or in inventory db browser"""
    )
    return ret
