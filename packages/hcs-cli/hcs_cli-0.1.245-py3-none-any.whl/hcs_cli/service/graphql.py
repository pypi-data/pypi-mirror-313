import logging
from hcs_core.sglib.client_util import hdc_service_client

log = logging.getLogger(__name__)


# Use a delay-initialized instance.
# It's because the dependent commands (cmd "query") is a top level command.
# The initialization of the client requires profile initialization.
# Profile initialization for top level commands should be avoided.
def _client():
    return hdc_service_client("graphql")


def post(payload: dict):
    return _client().post("/", json=payload)
