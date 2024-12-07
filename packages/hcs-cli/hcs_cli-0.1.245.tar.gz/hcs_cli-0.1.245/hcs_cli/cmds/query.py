import click
from hcs_cli.service import graphql
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent, util
import sys
import json

# https://github.com/euc-eng/horizonv2-sg.graphql/tree/master/src/main/resources/schema


@click.group()
def query():
    """Query Horizon Cloud resources."""
    pass


@query.command()
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
def raw(file):
    """Query by raw payload.
    E.g. hcs query raw < payload.json"""
    with file:
        text = file.read()
    try:
        payload = json.loads(text)
    except Exception as e:
        msg = "Invalid template: " + str(e)
        return msg, 1

    return graphql.post(payload)


@query.command()
@cli.org_id
@click.option("--page", type=int, required=False, default=0)
@click.option("--size", type=int, required=False, default=10)
@click.argument("template-id", type=str, required=False)
def vms(org: str, page: int, size: int, template_id: str):
    """Query VMs."""

    org_id = cli.get_org_id(org)
    template_id = recent.require(template_id, "template")

    payload = {
        "operationName": "horizonInventoryVms",
        "variables": {
            "withUserDiskSize": False,
            "size": size,
            "page": page,
            "templateId": template_id,
            "orgId": org_id,
        },
        "query": """query horizonInventoryVms($orgId: String!, $templateId: String, $page: Int, $size: Int, $withUserDiskSize: Boolean! = false) {
            horizonInventoryVms(
                orgId: $orgId
                templateId: $templateId
                page: $page
                size: $size
            ) {
                orgId
                content {
                    id
                    cloudId
                    lifecycleStatus
                    image
                    error
                    privateIp
                    privateIpv6
                    powerState
                    snapshotId
                    vmSize
                    userDiskSize @include(if: $withUserDiskSize)
                    osDiskSize
                    osDiskType
                    az
                    id
                    cloudId
                    lifecycleStatus
                    image
                    error
                    privateIp
                    powerState
                    snapshotId
                    vmSize
                    osDiskSize
                    osDiskType
                    az
                    templateId
                    edgeDeploymentId
                    orgId
                    location
                    agentStatus
                    statusCode
                    subnet
                    viewAgentVersion
                    haiAgentVersion
                    normalizedAgentVersion
                    timestamp
                    publicKey
                    sessionPlacementStatus
                    maxSessions
                    vmFreeSessions
                    createdAt
                    updatedAt
                    updatedLoadIndexAt
                    loadIndex
                    vmAssignedSessions
                    lastAssignedTime
                    priority
                    templateType
                    agentLoginMode
                    sessions {
                        vmId
                        userId
                        dspecId
                        agentSessionGuid
                        agentSessionId
                        sessionType
                        templateType
                        clientId
                        sessionStatus
                        lastAssignedTime
                        lastLoginTime
                        username
                        entitlementId
                        orgId
                        __typename
                    }
                    deviceId
                    sessionCount
                    sessionOccupancyLoadThreshold
                    agentReportedLoadIndexThreshold
                    transientLoadThreshold
                    userDesktopMappings {
                        id
                        userId
                        userPrincipalName
                        userName
                        orgId
                        location
                        entitlementId
                        poolId
                        templateId
                        vmId
                        createdAt
                        updatedAt
                        disabled
                        __typename
                    }
                    vmTimeZone {
                        timeZone
                        dayLightDisabled
                        __typename
                    }
                    __typename
                }
                totalPages
                totalElements
                size
                __typename
            }
        }""",
    }

    return graphql.post(payload)


@query.command()
@cli.org_id
@click.option("--page", type=int, required=False, default=0)
@click.option("--size", type=int, required=False, default=10)
@click.argument("template-id", type=str, required=False)
def sessions(org: str, page: int, size: int, template_id: str):
    """Query sessions"""

    org_id = cli.get_org_id(org)
    template_id = recent.require(template_id, "template")

    payload = {
        "operationName": "horizonSessions",
        "variables": {"size": size, "page": page, "templateId": template_id, "orgId": org_id},
        "query": """query horizonSessions($orgId: String!, $templateId: String, $poolGroupId: String, $page: Int, $size: Int) {
            horizonSessions(
                orgId: $orgId
                templateId: $templateId
                poolGroupId: $poolGroupId
                page: $page
                size: $size
            ) {
                orgId
                content {
                    vmId
                    vmName
                    userId
                    agentSessionGuid
                    sessionType
                    templateType
                    templateId
                    sessionStatus
                    lastLoginTime
                    username
                    orgId
                    sessionStateDuration
                    viewClientProtocol
                    dspecId
                    __typename
                }
                totalPages
                totalElements
                size
                __typename
            }
        }""",
    }
    return graphql.post(payload)


# @query.command()
# @cli.org_id
# @click.option("--page", type=int, required=False, default=0)
# @click.option("--size", type=int, required=False, default=10)
# def edges(org: str, page: int, size: int):
#     """Query edges"""

#     org_id = cli.get_org_id(org)
#     payload = {
#         "operationName": "horizonEdges",
#         "variables": {
#             "size": size,
#             "page": page,
#             "orgId": org_id
#         },
#         "query": """query horizonEdges($orgId: String!, $size: Int, $page: Int) {
#             q1: horizonEdges(
#                 orgId: $orgId
#                 size: $size
#                 page: $page
#                 search: \"providerLabel $eq azure AND status $eq READY\"
#             ) {
#                 orgId
#                 content {
#                     uagDeployments {
#                         status
#                         __typename
#                     }
#                     __typename
#                 }
#                 __typename
#             }
#             q2: horizonEdges(
#                 orgId: $orgId
#                 size: $size
#                 page: $page
#                 search: \"providerLabel $eq view AND status $eq READY\"
#             ) {
#                 orgId
#                 content {
#                     uagDeployments {
#                         status
#                         __typename
#                     }
#                     __typename
#                 }
#                 __typename
#             }
#             q3: horizonEdges(
#                 orgId: $orgId
#                 size: $size
#                 page: $page
#                 search: \"providerLabel $eq vsphere AND status $eq READY\"
#             ) {
#                 orgId
#                 content {
#                     uagDeployments {
#                         status
#                         __typename
#                     }
#                     __typename
#                 }
#                 __typename
#             }
#             q4: horizonEdges(
#                 orgId: $orgId
#                 size: $size
#                 page: $page
#                 search: \"providerLabel $eq aws AND status $eq READY\"
#             ) {
#                 orgId
#                 content {
#                     uagDeployments {
#                         status
#                         __typename
#                     }
#                     __typename
#                 }
#                 __typename
#             }
#         }"""
#     }
#     return graphql.post(payload)
