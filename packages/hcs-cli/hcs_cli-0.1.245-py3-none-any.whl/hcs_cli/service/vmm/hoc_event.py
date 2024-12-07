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
from datetime import datetime
from hcs_core.sglib.client_util import hdc_service_client

# Create a logger
logger = logging.getLogger("vmm")

_client = hdc_service_client("vm-manager")


def send(
    vm: dict,
    template_key_dict: dict,
    action: str,
    cmd_id: str,
    force_edge: str,
    regional_mqtt_port: str,
    update_type: str,
    status: str,
    error: str,
    verbose: bool,
):
    agent_mqtt_hoc_event = {"id": cmd_id, "type": "mqt:get:st", "version": "1", "source": "vmm"}

    data = {
        "utcTime": str(datetime.now().timestamp()),
        "orgId": vm.get("orgId"),
        "edgeId": template_key_dict.get("edge_deployment_id"),
        "templateId": vm.get("templateId"),
        "vmId": vm.get("id"),
        "agentVersion": vm.get("haiAgentVersion"),
        "powerState": vm.get("powerState"),
        "agentStatus": vm.get("agentStatus"),
        "lifecycleStatus": vm.get("lifecycleStatus"),
        "edgeMqttEndpointOnVm": vm.get("edgeMqttEndpoint"),
        "regionalMqttEndpointOnVm": vm.get("regionalMqttEndpoint"),
        "edgeMqttUrl": template_key_dict.get("edge_mqtt_url"),
        "regionalMqttHost": template_key_dict.get("regional_mqtt_url"),
        "vmhubUrl": template_key_dict.get("vmhub_url"),
        "runId": template_key_dict.get("run_id"),
        "action": action,
        "status": status,
    }

    if regional_mqtt_port:
        agent_mqtt_hoc_event["regionalMqttPort"] = regional_mqtt_port
    if force_edge:
        agent_mqtt_hoc_event["forceEdge"] = force_edge
    if update_type:
        agent_mqtt_hoc_event["updateType"] = update_type
    if error:
        agent_mqtt_hoc_event["error"] = error

    agent_mqtt_hoc_event["data"] = data
    # create array of events
    event_array = []
    event_array.append(agent_mqtt_hoc_event)
    # create hoc events request
    events_request = {}
    events_request["events"] = event_array
    if verbose:
        logger.info(events_request)
    try:
        ret = _client.post("/v1/agent/mqtt/hoc-events", events_request)
        return ret
    except Exception as error:
        logger.error(f"failed to send hoc event due to {error}")
