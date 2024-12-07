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
from hcs_cli.support.debug_util import resart_service
from hcs_cli.support.debug_util import get_service_full_name
from hcs_core.ctxp import recent
import subprocess
import json


@click.command()
@click.argument("service", type=str, required=True)
def prepare(service: str, **kwargs):
    """Prepare service k8s pod for debugging"""

    recent.set("k8s_service", service)

    service_full_name = get_service_full_name(service=service)

    # Define the patch operations
    patch_ops = [
        {"op": "replace", "path": "/spec/template/spec/containers/0/livenessProbe", "value": None},
        {"op": "replace", "path": "/spec/template/spec/containers/0/readinessProbe", "value": None},
        {"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["sleep", "8640000"]},
    ]

    print("Patched Operations: ", patch_ops)

    # Formulate the Kubernetes patch command
    patch_command = [
        "kubectl",
        "patch",
        f"{service_full_name}",
        "--type=json",
        "--patch",
        json.dumps(patch_ops),  # Convert patch_ops to JSON string
    ]

    # Execute the patch command and capture stdout/stderr
    try:
        result = subprocess.run(patch_command, capture_output=True, check=True, text=True)
        print("Command executed successfully:", result.stdout)
        resart_service(service_full_name=service_full_name)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e.stderr)
