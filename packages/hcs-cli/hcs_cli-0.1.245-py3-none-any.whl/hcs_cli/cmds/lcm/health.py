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
from hcs_cli.service.lcm import health as health
import hcs_core.sglib.cli_options as cli


@click.group("health")
def health_group():
    pass


@health_group.command()
def get(**kwargs):
    """Get service health info"""
    return health.get(**kwargs)


@health_group.command()
@click.argument("template", required=False)
@cli.org_id
def template(template: str, org: str, **kwargs):
    """Start template health check process for a single org."""
    org_id = cli.get_org_id(org)
    if template:
        return health.template.check(org_id, template, **kwargs)
    return health.template.check_all(org_id, **kwargs)
