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

import sys
import click
import hcs_core.plan as plan
import hcs_cli.support.plan_util as plan_util
from hcs_core.ctxp.util import error_details


@click.command()
@click.option("--file", "-f", type=click.File("rt"), required=False, help="Specified the plan file.")
@click.argument("resource", type=str, required=False)
@click.option(
    "--include-dependencies/--single-resource-only",
    type=bool,
    default=False,
    required=False,
    help="Used with --resource. Specify whether to process related resources, or just the target resource.",
)
@click.option(
    "--parallel/--sequential",
    type=bool,
    default=True,
    required=False,
    help="Specify deployment mode, parallel or sequential.",
)
@click.option(
    "--show-progress/--show-plain-log",
    type=bool,
    default=True,
    help="Control output format, interactive progress or plain logs.",
)
@click.option(
    "--details/--silent",
    "-d/-s",
    type=bool,
    default=True,
    help="Used with single resource deployment. If show details, will return the resource output.",
)
def apply(file, resource: str, include_dependencies: bool, parallel: bool, show_progress: bool, details: bool):
    """Apply a plan, create/update resources."""
    data, extra = plan_util.load_plan(file)
    concurrency = 10 if parallel else 1

    job_view = None
    if show_progress and sys.stdout.isatty():
        from hcs_core.util.job_view import JobView

        job_view = JobView.create_async()
        plan.attach_job_view(job_view)
    try:
        ret = plan.apply(
            data,
            additional_context=extra,
            target_resource_name=resource,
            include_dependencies=include_dependencies,
            concurrency=concurrency,
        )
    except (FileNotFoundError, plan.PlanException, plan.PluginException) as e:
        return error_details(e), 1
    finally:
        if job_view:
            job_view.close()

    if ret and details:
        return ret
