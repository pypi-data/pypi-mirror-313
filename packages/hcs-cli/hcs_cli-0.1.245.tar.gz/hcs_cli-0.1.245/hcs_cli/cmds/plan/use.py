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
import os
from hcs_core.ctxp import recent
from hcs_cli.support import plan_util


@click.command()
@click.argument("file", type=str, required=False)
def use(file: str):
    """Set or show the default plan file to work with."""
    if file:
        plan_util.validate_plan_file(file)
        # use the file
        abs_path = os.path.abspath(file)
        recent.set("plan-file", abs_path)
    else:
        return recent.get("plan-file")
