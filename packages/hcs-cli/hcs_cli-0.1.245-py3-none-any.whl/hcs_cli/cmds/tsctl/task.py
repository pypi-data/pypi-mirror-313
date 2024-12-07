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
from hcs_core.ctxp import CtxpException
from hcs_cli.service import tsctl
import hcs_core.sglib.cli_options as cli


@click.command()
def list_namespaces(**kwargs):
    """List namespaces"""
    return tsctl.list_namespaces()


@click.group(name="task")
def task_cmd_group():
    pass


@task_cmd_group.command()
@click.option("--namespace", "-n", type=str, required=True)
@click.option("--search", "-s", type=str, required=True)
@cli.search
def list(namespace: str, search: str, **kwargs):
    """List tasks"""
    return tsctl.task.list(namespace, search, **kwargs)


@task_cmd_group.command()
@click.option("--namespace", "-n", type=str, required=True)
@click.option("--id", "-i", type=str, required=True)
def get(namespace: str, id: str, **kwargs):
    """Get task by ID"""
    return tsctl.task.get(namespace, id, **kwargs)


@task_cmd_group.command()
@click.option("--namespace", "-n", type=str, required=False)
@click.option("--group", "-g", type=str, required=False)
@click.option("--key", "-k", type=str, required=False)
@click.argument("smart_path", type=str, required=False)
def delete(namespace: str, group: str, key: str, smart_path: str, **kwargs):
    """Delete task by ID"""
    return tsctl.task.delete(namespace, group, key, **kwargs)


@task_cmd_group.command()
@click.option("--namespace", "-n", type=str, required=True)
@cli.search
def logs(namespace: str, **kwargs):
    """List logs by task"""
    return tsctl.task.logs(namespace, **kwargs)


@task_cmd_group.command()
@click.option("--namespace", "-n", type=str, required=True)
@click.option("--group", "-g", type=str, required=True)
@click.option("--id", "-i", type=str, required=True)
@cli.search
def lastLog(namespace: str, group: str, id: str, **kwargs):
    """List logs by task"""
    return tsctl.task.lastlog(namespace, group, id, **kwargs)


def _parse_task_param(namespace: str, group: str, key: str, smart_path: str):
    if smart_path:
        if namespace:
            raise CtxpException("Task path is provided, so argument '--namespace' must not be specified.")
        if group:
            raise CtxpException("Task path is specified, so argument '--group' must not be specified.")
        if key:
            raise CtxpException("Task path is specified, so argument '--key' must not be specified.")

        parts = smart_path.split("/")
        if len(parts) != 3:
            raise CtxpException("Invalid task path. Valid example: <namespace>/<group>/<key>")

    if not namespace:
        raise CtxpException()
