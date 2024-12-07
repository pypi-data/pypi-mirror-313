from hcs_core.sglib import auth


def prepare(data: dict):
    # check login
    auth.oauth_client()
