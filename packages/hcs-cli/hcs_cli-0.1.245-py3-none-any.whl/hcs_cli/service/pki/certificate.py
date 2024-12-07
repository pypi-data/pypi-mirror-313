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

from hcs_core.sglib.client_util import hdc_service_client

_client = hdc_service_client("pki")


def test():
    print("TODO: test. Migrate that from pki-util here")


def get_org_cert(org_id: str):
    return _client.get(f"/certificate/v1/orgs/{org_id}")


def delete_org_cert(org_id: str):
    return _client.delete(f"/certificate/v1/orgs/{org_id}")


def sign_resource_cert(org_id: str, csr: str, validity_in_days: int):
    headers = {"Content-Type": "text/plain"}
    return _client.post(
        f"/certificate/v1/orgs/{org_id}/resource?includeChain=true&validityInDays={validity_in_days}",
        text=csr,
        headers=headers,
    )


def get_root_ca():
    return _client.get(f"/certificate/v1/root-ca")
