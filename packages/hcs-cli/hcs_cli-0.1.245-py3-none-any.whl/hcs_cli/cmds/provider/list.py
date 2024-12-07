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
from hcs_cli.service import admin
from hcs_core.ctxp import recent
import hcs_core.sglib.cli_options as cli
from hcs_cli.support.constant import provider_labels


@click.command()
@cli.org_id
@cli.limit
@cli.sort
@cli.search
@click.option(
    "--label",
    type=click.Choice(provider_labels),
    required=False,
    help="Specify the provider label",
)
def list(org: str, label: str, **kwargs):
    """List provider instances"""
    org_id = cli.get_org_id(org)

    if label:
        ret = admin.provider.list(label, org_id, **kwargs)
    else:
        # list all
        ret = []
        for label in provider_labels:
            ret += admin.provider.list(label, org_id, **kwargs)

    recent.helper.default_list(ret, "provider")

    return ret
