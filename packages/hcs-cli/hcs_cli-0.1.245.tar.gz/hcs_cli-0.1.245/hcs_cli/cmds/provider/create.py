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
import sys
from hcs_core.ctxp import recent
from hcs_cli.service import admin
from hcs_core.ctxp import panic
from hcs_core.ctxp.data_util import load_data_file
import hcs_core.sglib.cli_options as cli


@click.command()
@cli.org_id
@click.option(
    "--label",
    "-l",
    type=str,
    required=False,
    help="Provider label. E.g. Azure, vSphere. Default: Azure.",
)
@click.option("--name", "-n", type=str, required=False, help="Name of the provider.")
@click.option(
    "--data",
    "-d",
    type=str,
    required=False,
    multiple=True,
    help="key-value separated by '='. This parameter can be specified multiple times.",
)
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the payload file name. If not specified, STDIN will be used.",
)
def create(org: str, label: str, name: str, data, file: str):
    """Create a provider instance.

    Examples:

        hcs provider create -n nanw-test1 -d subscriptionId=a2ef2de8-f2b5-43da-bf68-2b182dd5f928 -d directoryId=45a54f44-5305-4388-97a6-aa39bc8b451b -d region=westus2 -d applicationId=<app-id> -d applicationKey=<app-key>

        hcs provider create --file path/to/payload.json

        hcs provider create < path/to/payload.json
    """

    default_payload = {
        "orgId": None,
        "providerLabel": None,
        "name": None,
        "edgeGatewayNeeded": True,
        "providerDetails": {"method": "ByAppRegistration", "data": {}},
    }

    if file:
        payload = load_data_file(file)
        if not payload:
            payload = default_payload
    else:
        payload = default_payload

    data_obj = payload["providerDetails"]["data"]

    # Override org id, if specified explicitly on args.
    # Otherwise override using default, if not in payload.
    if org:
        payload["orgId"] = org
    else:
        if not payload.get("orgId"):
            payload["orgId"] = cli.get_org_id()

    # Override properties
    for d in data:
        k, v = d.split("=")
        data_obj[k] = v

    if label:
        payload["providerLabel"] = label
    else:
        label = payload.get("providerLabel")
        if not label:
            label = "AZURE"
            payload["providerLabel"] = label

    if name:
        payload["name"] = name

    _validate(label, data_obj)

    ret = admin.provider.create(label, payload)
    if ret:
        recent.set("provider", ret["id"])
        return ret
    return "", 1


def _validate(label: str, data: dict):
    def _ensure_key_matches(required_keys, actual_keys):
        s1 = set(required_keys)
        s2 = set(actual_keys)
        missing = s1 - s2
        if missing:
            panic(f"Missing data: {missing}")
        extra = s2 - s1
        if extra:
            panic(f"Unexpected data: {extra}")

    label = label.upper()
    if label == "AZURE":
        required_keys = ["subscriptionId", "directoryId", "applicationId", "applicationKey", "region"]
        _ensure_key_matches(required_keys, data.keys())
    elif label == "VSPHERE":
        pass
    else:
        panic("Provider is not supported by CLI yet: " + label)
