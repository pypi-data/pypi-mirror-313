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
import json
import logging
import time
import uuid
from datetime import datetime
from enum import Enum
from hcs_cli.service import admin, inventory, vmhub, vmm
from hcs_cli.service.admin import VM
from hcs_cli.support.patch_util import calculate_patch
import hcs_core.ctxp.data_util as data_util

SLEEP_TIME_POWERON_VMS = 1
SLEEP_TIME_CERT_REFRESH_VMS = 1
SLEEP_TIME_MQTT_GET_UPDATE_VMS = 1
BATCH_SIZE = 2
FAILURE_THRESHOLD = 10
MIN_SUPPORTED_AGENT_VERSION = "24.2.0"

VMHUB_URL = "vmhub_url"
EDGE_DEPLOYMENT_ID = "edge_deployment_id"
EDGE_MQTT_URL = "edge_mqtt_url"
REGIONAL_MQTT_URL = "regional_mqtt_url"
REGIONAL_MQTT_PORT = "443"
LOCATION = "location"
RUN_ID = "run_id"

# Create a logger
logger = logging.getLogger("rootca_migrate")


@click.command(name="migrate", hidden="true")
@click.argument("target_org_id", type=str, required=True)
@click.argument("template_id", type=str, required=False)
@click.option("--verbose", "--v", type=bool, is_flag=True, required=False)
def migrate(target_org_id: str, template_id: str, verbose: bool):
    """cert refresh on all vms in org/template"""
    logger.info(f"Migrating to Omnissa cert:")
    logger.info("org: %s, template: %s", target_org_id, template_id)

    # declare all global variables
    global template_key_dict
    template_key_dict = {}
    global edge_url_update_failed_vms
    edge_url_update_failed_vms = []
    global regional_mqtt_url_update_failed_vms
    regional_mqtt_url_update_failed_vms = []

    # get key details from template and edgeDeployment
    template = None
    try:
        template = admin.template.get(template_id, target_org_id)
        template_key_dict = get_template_and_edge_details(template, target_org_id, verbose)
    except Exception as error:
        logger.error(error)
        return

    # disable powerPolicy on template
    power_policy_disabled_now = disable_power_policy_on_template(template, verbose)

    # each batch - powerOn all the VMs and migrate each vm
    page_num = 0
    while True:
        raw_list = inventory.vm.raw_list(template_id, org_id=target_org_id, size=BATCH_SIZE, page=page_num)
        page_num += 1
        total_pages = raw_list.get("totalPages")
        vms = raw_list.get("content")
        if verbose:
            log_vms_batch_details(raw_list)

        # powerOn all VMs in the batch
        power_on_vms(vms, target_org_id, template_id, verbose)
        # perform migration on all VMs in the batch
        try:
            perform_migration(vms, target_org_id, template_id, page_num, verbose)
        except Exception as error:
            if power_policy_disabled_now:
                enable_power_policy_on_template(template, verbose)
            else:
                logger.info(
                    f"powerPolicy on template {template_id} was disabled even before migration, so not enabled now."
                )

            return
        # check migration done on all batches in the template
        if page_num >= total_pages:
            if power_policy_disabled_now:
                enable_power_policy_on_template(template, verbose)
            else:
                logger.info(
                    f"powerPolicy on template {template_id} was disabled even before migration, so not enabled now."
                )
            logger.info(f"Finished root ca migration on org: %s, template: %s", target_org_id, template_id)
            return
    return


def get_template_and_edge_details(template: dict, org_id: str, verbose: bool):
    logger.info(f"Getting key details from template and edgeDeployment:")
    if not template:
        err = "Template object not found. exited migration."
        raise ValueError(err)
    if template.get("templateType") == "FLOATING":
        err = "Template {0} is {1} type. migration is not supported.".format(
            template["id"], template.get("templateType")
        )
        raise ValueError(err)

    vmhub_url = data_util.deep_get_attr(template, "hdc.vmHub.url", raise_on_not_found=False)
    edge_deployment_id = data_util.deep_get_attr(template, "edgeDeploymentId", raise_on_not_found=False)
    location = data_util.deep_get_attr(template, "location", raise_on_not_found=False)
    if not vmhub_url:
        err = "vmhub url is missing on template {0}. exited migration.".format(template["id"])
        raise ValueError(err)
    if not edge_deployment_id:
        err = "edgeDeploymentId is missing on template {0}. exited migration.".format(template["id"])
        raise ValueError(err)

    edge = admin.edge.get(edge_deployment_id, org_id)
    if not edge:
        err = "edgeDeployment object is not found. edgeId {0} and org {1}".format(edge_deployment_id, org_id)
        raise ValueError(err)
    regional_mqtt_url = data_util.deep_get_attr(edge, "privateEndpointDetails.dnsRecord", raise_on_not_found=False)
    edge_mqtt_url = data_util.deep_get_attr(edge, "fqdn", raise_on_not_found=False)

    d = dict()
    d[VMHUB_URL] = vmhub_url
    d[EDGE_DEPLOYMENT_ID] = edge_deployment_id
    d[LOCATION] = location
    d[EDGE_MQTT_URL] = edge_mqtt_url
    d[REGIONAL_MQTT_URL] = regional_mqtt_url
    d[RUN_ID] = str(datetime.now().strftime("%m%d%Y%H%M%S"))
    if verbose:
        logger.info("Key details from template & edge: %s", d)
    return d


def enable_power_policy_on_template(template: dict, verbose: bool):
    return power_policy_on_template(template, True, verbose)


def disable_power_policy_on_template(template: dict, verbose: bool):
    return power_policy_on_template(template, False, verbose)


def power_policy_on_template(template: dict, enable: bool, verbose: bool):
    # enable/disable powerPolicy on template
    action = "Enable" if enable else "Disable"
    template_id = template["id"]
    target_org_id = template["orgId"]
    if verbose:
        logger.info(f"{action} powerPolicy on template {template_id}")
    try:
        data_util.deep_get_attr(template, "powerPolicy", raise_on_not_found=True)
        enabled = data_util.deep_get_attr(template, "powerPolicy.enabled", raise_on_not_found=True)
        if enabled != None and enabled == False:
            logger.info(f"powerPolicy already disabled on template {template_id}")
            return False
    except:
        logger.info(f"powerPolicy doesn't exist on template {template_id}")
        return False

    allowed_fields = ["name", "description", "powerPolicy", "sparePolicy", "applicationProperties", "flags"]
    field = "powerPolicy.enabled=true" if enable else "powerPolicy.enabled=false"
    patch = calculate_patch(template, allowed_fields, [field])
    admin.template.update(template_id, target_org_id, patch)
    admin.template.wait_for_ready(template_id, target_org_id, 60)
    logger.info(f"{action}d powerPolicy on template {template_id}")
    return True


def power_on_vms(vms: dict, target_org_id: str, template_id: str, verbose: bool):
    poweron_vms = []
    poweron_failed_vms = []
    agent_version_chk_failed_vms = []
    for vm in vms:
        log_vm_info(target_org_id, template_id, vm["id"])
        if not is_valid_agent_version(vm.get("haiAgentVersion")):
            agent_version_chk_failed_vms.append(vm)
            vmm.hoc_event.send(
                vm,
                template_key_dict,
                Action.AGENT_VERSION.name,
                vm["id"],
                None,
                None,
                None,
                HocStatus.FAILURE.value,
                None,
                verbose,
            )
        if vm["powerState"] in ["PoweredOff", "Unknown"]:
            vmObj = VM(target_org_id, template_id, vm["id"])
            try:
                vmObj.power_on()
                poweron_vms.append(vm)
            except Exception as e:
                poweron_failed_vms.append(vm)
                vmm.hoc_event.send(
                    vm,
                    template_key_dict,
                    Action.POWER_ON.name,
                    vm["id"],
                    None,
                    None,
                    None,
                    HocStatus.FAILURE.value,
                    e,
                    verbose,
                )

    if verbose:
        logger.info(f"vms being powered on: %d", len(poweron_vms))
        for vm in poweron_vms:
            logger.info(f"vm %s - powerState: %s", vm.get("id"), vm.get("powerState"))

        logger.info(f"vms failed to power on: %d", len(poweron_failed_vms))
        for vm in poweron_failed_vms:
            logger.warn(f" vm %s - powerOn operation failed, powerState: %s", vm.get("id"), vm.get("powerState"))

        logger.info(f"vms with invalid agent version: %d", len(agent_version_chk_failed_vms))
        for vm in agent_version_chk_failed_vms:
            logger.warn(
                f"vm %s - hai version check failed haiAgentVersion: %s", vm.get("id"), vm.get("haiAgentVersion")
            )

    # sleep for vms to poweredOn
    if len(poweron_vms) > 0:
        logger.info(f"sleep for %d minutes to powerOn on all poweredOff vms", SLEEP_TIME_POWERON_VMS)
        time.sleep(10 * SLEEP_TIME_POWERON_VMS)

    # remove failed vms from processing further
    for vm in poweron_failed_vms:
        vms.remove(vm)
    for vm in agent_version_chk_failed_vms:
        vms.remove(vm)


def perform_migration(vms: dict, target_org_id: str, template_id: str, batch_num: int, verbose: bool):
    logger.info(f"Perform get MQTT & cert refresh calls on batch {batch_num}")
    for vm in vms:
        cmd_id = str(uuid.uuid4())
        try:
            vmhub.mqtt.get(
                target_org_id,
                template_key_dict[EDGE_DEPLOYMENT_ID],
                template_id,
                vm["id"],
                cmd_id,
                template_key_dict[VMHUB_URL],
                verbose,
            )
            time.sleep(10 * SLEEP_TIME_MQTT_GET_UPDATE_VMS)
            u_vm = inventory.get(template_id, vm["id"], target_org_id)
            vmm.hoc_event.send(
                u_vm,
                template_key_dict,
                Action.GET.name,
                cmd_id,
                None,
                None,
                None,
                HocStatus.SUCCESS.value,
                None,
                verbose,
            )
        except Exception as error:
            u_vm = inventory.get(template_id, vm["id"], target_org_id)
            vmm.hoc_event.send(
                u_vm,
                template_key_dict,
                Action.GET.name,
                cmd_id,
                None,
                None,
                None,
                HocStatus.FAILURE.value,
                error,
                verbose,
            )
        if verbose:
            log_vm_info(target_org_id, template_id, vm["id"])

        try:
            vmhub.mqtt.refresh_cert(
                target_org_id,
                template_key_dict[EDGE_DEPLOYMENT_ID],
                template_id,
                vm["id"],
                template_key_dict[REGIONAL_MQTT_URL],
                REGIONAL_MQTT_PORT,
                template_key_dict[VMHUB_URL],
                verbose,
            )
            time.sleep(10 * SLEEP_TIME_CERT_REFRESH_VMS)
            cmd_id = str(uuid.uuid4())
            vmhub.mqtt.get(
                target_org_id,
                template_key_dict[EDGE_DEPLOYMENT_ID],
                template_id,
                vm["id"],
                cmd_id,
                template_key_dict[VMHUB_URL],
                verbose,
            )
            time.sleep(10 * SLEEP_TIME_MQTT_GET_UPDATE_VMS)
            u_vm = inventory.get(template_id, vm["id"], target_org_id)
            vmm.hoc_event.send(
                u_vm,
                template_key_dict,
                Action.GET_POST_CERT_REF.name,
                cmd_id,
                None,
                None,
                None,
                HocStatus.SUCCESS.value,
                None,
                verbose,
            )
        except Exception as error:
            u_vm = inventory.get(template_id, vm["id"], target_org_id)
            vmm.hoc_event.send(
                u_vm,
                template_key_dict,
                Action.GET_POST_CERT_REF.name,
                cmd_id,
                None,
                None,
                None,
                HocStatus.FAILURE.value,
                error,
                verbose,
            )
        if verbose:
            log_vm_info(target_org_id, template_id, vm["id"])

        # invoke update mqtt call
        try:
            cmd_id = str(uuid.uuid4())
            force_edge = False
            vmhub.mqtt.update(
                target_org_id,
                template_key_dict[EDGE_DEPLOYMENT_ID],
                template_id,
                vm["id"],
                cmd_id,
                template_key_dict[EDGE_MQTT_URL],
                template_key_dict[VMHUB_URL],
                force_edge,
                verbose,
            )
            time.sleep(10 * SLEEP_TIME_MQTT_GET_UPDATE_VMS)
            log_vm_info(target_org_id, template_id, vm["id"])
            u_vm = inventory.get(template_id, vm["id"], target_org_id)
            vmm.hoc_event.send(
                u_vm,
                template_key_dict,
                Action.GET_POST_UPDATE.name,
                cmd_id,
                str(force_edge),
                str(REGIONAL_MQTT_PORT),
                "EDGE",
                HocStatus.SUCCESS.value,
                None,
                verbose,
            )
        except Exception as error:
            u_vm = inventory.get(template_id, vm["id"], target_org_id)
            vmm.hoc_event.send(
                u_vm,
                template_key_dict,
                Action.GET_POST_UPDATE.name,
                cmd_id,
                str(force_edge),
                str(REGIONAL_MQTT_PORT),
                "EDGE",
                HocStatus.FAILURE.value,
                error,
                verbose,
            )

        # check if migration succeeded
        if (
            vm.get("regionalMqttEndpoint") is None
            or vm.get("regionalMqttEndpoint") != template_key_dict[REGIONAL_MQTT_URL]
        ):
            regional_mqtt_url_update_failed_vms.append(vm)
        elif vm.get("edgeMqttEndpoint") is None or vm.get("edgeMqttEndpoint") != template_key_dict[EDGE_MQTT_URL]:
            edge_url_update_failed_vms.append(vm)
        total_failed_vms = len(regional_mqtt_url_update_failed_vms) + len(edge_url_update_failed_vms)
        if total_failed_vms >= FAILURE_THRESHOLD:
            err = "Exiting the script execution. Failure threshold(limit: {0}) reached: {1}".format(
                FAILURE_THRESHOLD, total_failed_vms
            )
            logger.error(err)
            for f_vm in regional_mqtt_url_update_failed_vms:
                logger.warn(
                    f"vm {f_vm.get('id')} - regional mqtt url is not updated. regionalMqttEndpoint on vm is {f_vm.get('regionalMqttEndpoint')}"
                )
            for f_vm in edge_url_update_failed_vms:
                logger.warn(
                    f"vm {f_vm.get('id')} - edge mqtt url not updated. edgeMqttEndpoint on vm is {f_vm.get('edgeMqttEndpoint')}"
                )
            raise ValueError(err)


def log_vm_info(target_org_id: str, template_id: str, vm_id: str):
    vm = inventory.get(template_id, vm_id, target_org_id)
    logger.info(
        f"vm %s - powerState: %s, haiAgentVersion: %s, regionalMqttEndpoint: %s, edgeMqttEndpoint: %s",
        vm["id"],
        vm["powerState"],
        vm.get("haiAgentVersion"),
        vm.get("regionalMqttEndpoint"),
        vm.get("edgeMqttEndpoint"),
    )


def is_valid_agent_version(agent_version: str):
    if agent_version is None or not agent_version:
        return False
    av_arr = agent_version.split(".")
    msav_arr = MIN_SUPPORTED_AGENT_VERSION.split(".")
    index = 0
    while index < len(av_arr) and index < len(msav_arr):
        if int(av_arr[index]) == int(msav_arr[index]):
            index += 1
            continue
        elif int(av_arr[index]) > int(msav_arr[index]):
            return True
        else:
            return False

    if len(av_arr) >= len(msav_arr):
        return True
    else:
        return False


def log_vms_batch_details(vms_response: dict):
    batch_num = vms_response.get("number")
    total_batches = vms_response.get("totalPages")
    total_vms = vms_response.get("totalElements")
    vms_on_current_batch = vms_response.get("numberOfElements")
    logger.info(
        f"batch information: batch_num: {batch_num + 1}, total_batches: {total_batches}, batch_size: {BATCH_SIZE},  total_vms: {total_vms}, vms_on_current_batch: {vms_on_current_batch}"
    )


class Action(Enum):
    GET = 1
    GET_POST_CERT_REF = 2
    GET_POST_UPDATE = 3
    POWER_ON = 4
    AGENT_VERSION = 5


class HocStatus(str, Enum):
    SUCCESS = "su"
    FAILURE = "fl"
