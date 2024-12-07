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
import hcs_core.plan as plan
import hcs_cli.support.plan_util as plan_util


@click.command()
@click.option("--file", "-f", type=click.File("rt"), required=False, help="Specified the plan file.")
@click.option("--summary/--details", "-s/-d", type=bool, default=True)
@click.argument("resource", type=str, required=False)
def output(file, summary: bool, resource: str):
    """Show resource output data."""

    data, extra = plan_util.load_plan(file)
    input_dict, output_dict = plan.get_deployment_data(data, extra, resource)

    if resource:
        if resource not in output_dict:
            return f"Resource '{resource}' is not found in output.", 1
        v = None
        if resource in output_dict:
            v = output_dict[resource]
        if summary:
            return plan_util.resource_output_to_display(v)
        return v

    if summary:
        ret = {}
        for k in output_dict:
            v = output_dict[k]
            if v:
                ret[k] = plan_util.resource_output_to_display(v)
    else:
        ret = output_dict
    return ret
