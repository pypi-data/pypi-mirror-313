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
from hcs_cli.service.vmhub import otp as otp_service
from hcs_core.util import pki_util


@click.command()
@click.option(
    "--region",
    type=str,
    default=None,
    required=False,
    help="Specify region name",
)
@click.argument("resource-name", type=str, required=True)
@click.argument("otp", type=str, required=True)
def redeem(region: str, resource_name: str, otp: str):
    """Redeem OTP with CSR, receive resource cert."""

    otp_service.use_region(region)
    csr_pem, private_key_pem = pki_util.generate_CSR(resource_name)

    ret = otp_service.redeem(resource_name, otp, csr_pem)
    ret.private_key = private_key_pem
    return ret
