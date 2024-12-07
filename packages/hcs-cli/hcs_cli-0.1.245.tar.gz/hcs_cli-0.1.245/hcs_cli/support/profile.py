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

from hcs_core.ctxp import data_util
from hcs_core.ctxp import config, profile, CtxpException


# _default = {
#     "prod": [
#         {
#             "env": "prod-na-cp102"
#             "alias": "prod-us"
#             "description": ""
#             "azure-reion": "WestUS2"
#             "primary": ""
#             "portal-url":[

#             ]
#             - https://cloud.vmwarehorizon.com/
#             - https://cloud-sg.horizon.vmware.com
#             hdc:
#             url: https://cloud-sg-us.horizon.vmware.com
#             regions:
#             - name: EastUS2
#                 url: https://cloud-sg-us-r-eastus2.horizon.vmware.com
#                 mqtt: https://cloud-sg-us-r-eastus2-mqtt.horizon.vmware.com
#             - name: WestUS2
#                 url: https://cloud-sg-us-r-westus2.horizon.vmware.com
#                 mqtt: https://cloud-sg-us-r-westus2-mqtt.horizon.vmware.com
#             edgehub:
#             url: https://hv2-cloud-us-2.horizon.vmware.com
#             "hcs": {
#                 "url": "https://cloud-sg-us.horizon.vmware.com",
#                 "regions": [
#                     {
#                         "name": "EastUS2",
#                         "url": "https://cloud-sg-us-r-eastus2.horizon.vmware.com",
#                         "mqtt": "https://cloud-sg-us-r-eastus2-mqtt.horizon.vmware.com"
#                     },
#                     {
#                         "name": "WestUS2",
#                         "url": "https://cloud-sg-us-r-westus2.horizon.vmware.com",
#                         "mqtt": "https://cloud-sg-us-r-westus2-mqtt.horizon.vmware.com"
#                     }
#                 ]
#             },
#             "csp": {
#                 "url": "https://console.cloud.vmware.com",
#                 "orgId": None,
#                 "apiToken": None,
#                 "clientId": None,
#                 "clientSecret": None
#             }
#         }
#     ]

# }

_hcs_envs = config.get("hcs-deployments.yaml")


def _is_production_env(hdc_url: str) -> bool:
    for env in _hcs_envs["prod"]:
        if env.hdc.url == hdc_url:
            return True


def _get_csp_url(hdc_url: str) -> str:
    if _is_production_env(hdc_url):
        return "https://connect.omnissa.com"
    return "https://console-stg.cloud.vmwservices.com"


def ensure_default_production_profile():
    doc = get_default_profile_template()
    _ensure_profile("default", doc, interactive=False)


def _find_config(name):
    for stack in _hcs_envs["prod"]:
        if stack.env == name:
            return _profile_data_from_stack(stack)
    for stack in _hcs_envs["staging"]:
        if stack.env == name:
            return _profile_data_from_stack(stack)
    for stack in _hcs_envs["dev"]:
        if stack.env == name:
            return _profile_data_from_stack(stack)
    CtxpException("Configuration not found: " + name)


def get_default_profile_template():
    return _find_config("prod-na-cp102")


def get_dev_profile_template():
    return _find_config("sg-master")


def _profile_data_from_stack(stack):
    return {
        "hcs": {"url": stack.hdc.url, "regions": stack.regions},
        "csp": {
            "url": _get_csp_url(stack.hdc.url),
            "orgId": None,
            "apiToken": None,
            "clientId": None,
            "clientSecret": None,
        },
    }


def _ensure_profile(name, data, interactive: bool = True, hard_reset: bool = False):
    existing = profile.get(name)
    if existing:
        if hard_reset:
            profile.write(name, data)
            if interactive:
                print("Profile reset: " + name)
        else:
            if data_util.deep_apply_default(existing, data):
                profile.write(name, existing)
                if interactive:
                    print("Profile created: " + name)
            else:
                if interactive:
                    print("Profile unchanged: " + name)
    else:
        profile.create(name, data, False)
        if interactive:
            print("Profile created: " + name)


def _ensure_ops_profile(hard_reset: bool):
    payload = profile.get("prod-us")
    payload.csp.orgId = "bf35820f-a12f-4828-ba7f-c72171ff3084"  # Horizon Cloud Production Internal
    payload.hoc = _hcs_envs["hoc"]
    _ensure_profile("ops", payload, interactive=True, hard_reset=hard_reset)


def ensure_dev_profiles(hard_reset: bool = False):
    items = []
    items += _hcs_envs["prod"]
    items += _hcs_envs["staging"]
    items += _hcs_envs["dev"]

    for stack in items:
        name = stack.alias or stack.env
        doc = _profile_data_from_stack(stack)
        _ensure_profile(name, doc, interactive=True)
    _ensure_profile("nightly", profile.get("integration"), interactive=True, hard_reset=hard_reset)

    _ensure_ops_profile(hard_reset)
