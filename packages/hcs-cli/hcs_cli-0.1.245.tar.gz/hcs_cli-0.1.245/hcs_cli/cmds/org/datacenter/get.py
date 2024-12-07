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
from hcs_cli.service.org_service import datacenter
from hcs_core.ctxp import recent


@click.command()
@click.argument("id", type=str, required=False)
def get(id: str):
    """Get datacenter by ID"""
    id = recent.require(id, "datacenter")
    ret = datacenter.get(id)
    if ret:
        return ret
    return ret, 1
