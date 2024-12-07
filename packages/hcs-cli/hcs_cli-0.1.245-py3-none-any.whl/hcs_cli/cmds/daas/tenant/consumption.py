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
from hcs_core.sglib import cli_options
from hcs_core.ctxp import error


@click.command()
@click.argument("deployment-id", type=str, required=True)
def consumption(deployment_id):
    """Get the consumption information of the tenant."""

    # print(org_id, deployment_id)

    return error("The consumption service is not available on production yet.")
