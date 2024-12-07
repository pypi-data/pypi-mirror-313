import logging
from hcs_core.sglib.client_util import hdc_service_client

log = logging.getLogger(__name__)

_client = hdc_service_client("scm")


def health():
    return _client.get("/v1/health")


def recommend_power_policy(org_id: str, template_id: str):
    return _client.get(f"/v1/templates/{template_id}/power-policies?org_id={org_id}")
