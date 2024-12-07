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

from hcs_core.plan import actions, PluginException
from hcs_cli.service import admin, portal
from hcs_core.plan import context


def deploy(data: dict, state: dict, save_state) -> dict:
    org_id = data["orgId"]

    if not state:
        deployment = admin.edge.create(data)
        save_state(deployment)
    else:
        deployment = state
    id = deployment["id"]
    providerLabel = data.get("providerLabel")

    is_ready = lambda s: s in [
        "CREATE_PENDING",
        "CREATING",
        "READY",
        "POST_PROVISIONING_CONFIG_IN_PROGRESS",
        "UPDATE_PENDING",
        "UPDATING",
        "UPGRADE_PENDING",
        "UPGRADING",
    ]
    is_error = lambda s: s.endswith("_FAILED") or s in [
        # 'CREATE_FAILED',
        "DELETED",
        # 'DELETE_FAILED',
        "DELETE_PENDING",
        "DELETING",
        "FORCE_DELETE_PENDING",
        "FORCE_DELETING",
        "FORCE_REPAIR_ACCEPTED",
        "FORCE_REPAIR_PENDING",
        # CONNECT_PENDING,
        # CREATE_ACCEPTED,
        # CREATE_FAILED,
        # CREATE_PENDING,
        # CREATING,
        "DELETED",
        #'DELETE_FAILED',
        "DELETE_PENDING",
        "DELETING",
        "FORCE_DELETE_PENDING",
        "FORCE_DELETING",
        "FORCE_REPAIR_ACCEPTED",
        "FORCE_REPAIR_PENDING",
        #'MIGRATE_FAILED',
        "MIGRATE_PENDING",
        "MIGRATING",
        # POST_PROVISIONING_CONFIG_IN_PROGRESS,
        # READY,
        "REPAIRING",
        "REPAIR_ACCEPTED",
        #'REPAIR_FAILED',
        "REPAIR_PENDING",
        #'UPDATE_FAILED',
        #'UPDATE_PENDING',
        #'UPDATING',
        #'UPGRADE_FAILED',
        #'UPGRADE_PENDING',
        #'UPGRADING',
    ]
    is_transition = lambda s: s.endswith("ING") or s in [
        "CREATE_ACCEPTED",
    ]

    if providerLabel == "vsphere":
        polling_interval = "5s"
        timeout = "2m"
    else:
        # azure
        polling_interval = "1m"
        timeout = "20m"

    try:
        deployment = admin.edge.wait_for(
            id,
            org_id,
            is_ready=is_ready,
            is_error=is_error,
            is_transition=is_transition,
            polling_interval=polling_interval,
            timeout=timeout,
        )
    except Exception as e:
        deployment = admin.edge.get(id, org_id)
        save_state(deployment)
        raise PluginException("Error waiting for edge deployment. Status=" + deployment["status"]) from e

    site_id = data.get("siteId")
    if site_id:
        portal.site.set_edge(site_id, org_id, id)

    _workaround_edge_connection_string(data, deployment)

    return deployment


def _workaround_edge_connection_string(data: dict, edge):
    org_id = data["orgId"]
    providerLabel = data.get("providerLabel")
    if providerLabel == "vsphere" or providerLabel == "nutanix":
        if edge.get("deploymentModeDetails", {}).get("type") == "UNMANAGED":
            pass
        else:
            connection_string = admin.edge.get_connection_string(edge["id"], org_id)
            # context.set('edge_connection_string', edge_connection_string)
            edge["connectionString"] = connection_string
    return edge


def refresh(data: dict, state: dict) -> dict:
    edge = None
    org_id = data["orgId"]
    if state:
        id = state.get("id")
        if id:
            edge = admin.edge.get(id, org_id)
    if not edge:
        edges = admin.edge.list(org_id, search=f'name $eq {data["name"]}')
        if edges:
            edge = edges[0]

    if edge:
        _workaround_edge_connection_string(data, edge)
    return edge


def decide(data: dict, state: dict):
    if state["status"] in ["READY"]:
        return actions.skip
    # https://gitlab.eng.vmware.com/horizonv2-sg/admin/-/blob/master/src/main/java/com/vmware/horizon/admin/model/edgedeployment/EdgeDeploymentV2Status.java


def destroy(data: dict, state: dict, force: bool) -> dict:
    id = state["id"]
    org_id = data["orgId"]
    admin.edge.safe_delete(id, org_id, "20m")


def eta(action: str, data: dict, state: dict):
    providerLabel = data.get("providerLabel")

    if action == actions.create:
        if providerLabel == "vsphere":
            return "1m"
        if providerLabel == "azure":
            return "15m"
        return "15m"
    if action == actions.delete:
        if providerLabel == "vsphere":
            return "15s"
        if providerLabel == "azure":
            return "10m"
        return "10m"
