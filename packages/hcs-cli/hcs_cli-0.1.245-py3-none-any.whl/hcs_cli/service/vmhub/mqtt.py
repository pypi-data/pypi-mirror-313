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

import logging
from hcs_core.sglib import hcs_client

# Create a logger
logger = logging.getLogger("vmhub")


def _client(url: str):
    if not url.endswith("/"):
        url += "/"
    url += "vmhub"
    return hcs_client(url)


def get(org_id: str, edge_id: str, template_id: str, vm_id: str, cmd_id: str, vmhub_url: str, verbose: bool):
    bulk_agent_command_request = {
        "command": "GET_ENDPOINT_PROPERTIES",
        "agentCommandRequests": [
            {"edgeId": edge_id, "templateId": template_id, "vmIds": [vm_id], "payload": {"ID": cmd_id, "orgId": org_id}}
        ],
    }
    logger.info(f"vm {vm_id} - making get mqtt API call")
    if verbose:
        logger.info(bulk_agent_command_request)
    ret = _client(vmhub_url).post("/agent/command", bulk_agent_command_request)
    return ret


def update(
    org_id: str,
    edge_id: str,
    template_id: str,
    vm_id: str,
    cmd_id: str,
    edge_mqtt_url: str,
    vmhub_url: str,
    force_edge: bool,
    verbose: bool,
):
    bulk_agent_command_request = {
        "command": "UPDATE_MQTT_ENDPOINTS",
        "agentCommandRequests": [
            {
                "edgeId": edge_id,
                "templateId": template_id,
                "vmIds": [vm_id],
                "payload": {
                    "ID": cmd_id,
                    "orgId": org_id,
                    "UPDATE_TYPE": "EDGE",
                    "FORCEEDGE": force_edge,
                    "EDGE": edge_mqtt_url,
                },
            }
        ],
    }
    logger.info(f"vm {vm_id} - making update mqtt API call")
    if verbose:
        logger.info(bulk_agent_command_request)
    ret = _client(vmhub_url).post("/agent/command", bulk_agent_command_request)
    return ret


def refresh_cert(
    org_id: str,
    edge_id: str,
    template_id: str,
    vm_id: str,
    mqtt_endpoint: str,
    mqtt_port: str,
    vmhub_url: str,
    verbose: bool,
):
    refresh_certificate_request = {
        "orgId": org_id,
        "edgeDeploymentId": edge_id,
        "templateId": template_id,
        "vmIds": [vm_id],
        "mqttServerPort": mqtt_port,
    }
    if mqtt_endpoint:
        refresh_certificate_request["mqttEndpoint"] = mqtt_endpoint
    logger.info(f"vm {vm_id} - making cert refresh API call")
    if verbose:
        logger.info(refresh_certificate_request)
    ret = _client(vmhub_url).post("/credentials/refresh-certificate", refresh_certificate_request)
    return ret
