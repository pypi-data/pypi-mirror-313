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
from hcs_core.ctxp import panic
from hcs_cli.service.pki import certificate
import hcs_core.sglib.cli_options as cli


@click.command()
@cli.org_id
@cli.confirm
def delete(org: str, confirm: bool):
    """Delete the signing certificate of a specific org"""

    if not confirm:
        panic('Delete an org certificate will impact some service. Specify "--confirm" to perform the deletion.')
    org_id = cli.get_org_id(org)
    return certificate.delete_org_cert(org_id)
