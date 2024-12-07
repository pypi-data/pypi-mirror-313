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
@click.option(
    "--view/--output-only",
    "-v",
    type=bool,
    default=True,
    help="If view mode is specified, open browser to view the graph.",
)
@click.option("--for-deploy/--for-destroy", type=bool, default=True, help="Specify whether for deploy or for destroy.")
@click.option(
    "--resource",
    "-r",
    type=str,
    required=False,
    help="Specify a single resource in the plan to deploy. This includes deploying dependent resources.",
)
@click.option(
    "--include-dependencies/--single-resource-only",
    type=bool,
    default=False,
    required=False,
    help="Used with --resource. Specify whether to process related resources, or just the target resource.",
)
def graph(file, view: bool, for_deploy: bool, resource: str, include_dependencies: bool):
    """Generate a graph view of the deployment, in Graphviz format."""

    try:
        data, extra = plan_util.load_plan(file)
        g = plan.graph(data, extra, not for_deploy, resource, include_dependencies)
        if view:
            _view_graph(g.source)
        return g.source
    except (FileNotFoundError, plan.PlanException, plan.PluginException) as e:
        return str(e), 1


def _view_graph(src):
    import urllib.parse
    import webbrowser

    url = "https://dreampuf.github.io/GraphvizOnline/#" + urllib.parse.quote(src)
    webbrowser.open(url, new=0, autoraise=True)
