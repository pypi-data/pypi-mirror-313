from elasticsearch import Elasticsearch
import requests

# requests.packages.urllib3.disable_warnings()

from hcs_core.ctxp import profile, CtxpException

_client_map = {}


def client(region: str) -> Elasticsearch:
    global _client
    c = _client_map.get(region)
    if not c:
        hoc_config = profile.current().hoc
        if not hoc_config:
            raise CtxpException("Config not found: profile.hoc. Use 'hcs profile edit' to update.")
        es_config_map = hoc_config.es
        if not es_config_map:
            raise CtxpException("Config not found: profile.hoc.es. Use 'hcs profile edit' to update.")
        if region not in es_config_map:
            raise CtxpException(f"Config not found: profile.hoc.es.{region}. Use 'hcs profile edit' to update.")
        es_config = es_config_map[region]
        if not es_config.url:
            raise CtxpException("Config not found: profile.hoc.es.url. Use 'hcs profile edit' to update.")
        if not es_config.username:
            raise CtxpException("Config not found: profile.hoc.es.username. Use 'hcs profile edit' to update.")
        if not es_config.password:
            raise CtxpException("Config not found: profile.hoc.es.password. Use 'hcs profile edit' to update.")

        c = Elasticsearch(
            es_config.url,
            verify_certs=False,
            http_compress=True,
            max_retries=2,
            retry_on_timeout=True,
            http_auth=(es_config.username, es_config.password),
        )
        _client_map[region] = c
    return c
