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
import hcs_core.ctxp as ctxp
from hcs_ext_daas import infra


@click.command()
def get():
    """Get the shared infrastructure config."""
    return infra.get()


@click.command()
def file():
    """Get the infrastructure config file path."""
    return infra.file()


@click.command()
def edit():
    """Launch text editor to edit the config file directly"""
    file = infra.file()
    ctxp.util.launch_text_editor(file)
