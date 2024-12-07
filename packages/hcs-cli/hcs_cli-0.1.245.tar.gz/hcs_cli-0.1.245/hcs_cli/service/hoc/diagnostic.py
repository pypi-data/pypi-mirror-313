import logging
from hcs_core.sglib.client_util import hdc_service_client

log = logging.getLogger(__name__)


def _client():
    return hdc_service_client("hoc-diagnostic")


def search(payload: dict):
    return _client().post("/v1/data/search", json=payload)
