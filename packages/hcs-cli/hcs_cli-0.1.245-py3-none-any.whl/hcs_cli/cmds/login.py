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
import hcs_core.sglib as sglib
import hcs_core.ctxp as ctxp
from hcs_core.ctxp import recent
from hcs_core.sglib import login_support
from hcs_cli.support import profile as profile_support

# Login use cases:

# 1. Login scenario
# 1.1. As a new user, I want to login.
# 1.2. As a returning user, I want to re-login use the same auth method.
# 1.3. As a returning user, I want to re-login use a different auth method.
# 1.4. As a returning user, I want the system to avoid unnecessary login if the auth is not expired.
# 1.5. As a returning user, I want to re-login with a different org.

# 2. Login type
# 2.1. As a user, I want to login interactively with browser
# 2.2. As a user, I want to login with api-token
# 2.2. As a user, I want to login with refresh-token
# 2.2. As a user, I want to login with client id/secret
# 2.2. As a user, I want to login with bearer

# 3. Information
# 3.1. As a user, I want to get the login details (e.g. my permissions)
# 3.2. As a user, I want to get the access token, so I can use it with REST API.


@click.command()
@click.option(
    "--org",
    type=str,
    required=False,
    help="The CSP organization to login. If not specified, the user's default organization will be used.",
)
@click.option("--api-token", type=str, required=False, help="Login with a user CSP API token.")
@click.option("--client-id", type=str, required=False, help="Login with OAuth client ID/secret.")
@click.option("--client-secret", type=str, required=False, help="The OAuth client secret, used with --client-id.")
@click.option(
    "--browser/--auto", type=bool, default=False, help="Login with browser and remove other configured credentials."
)
@click.option(
    "--details/--no-details",
    "-d",
    default=False,
    help="If specified, return the detailed information about the authentication information, otherwise return only the access token.",
)
@click.option(
    "--refresh/--no-refresh",
    "-r",
    default=False,
    help="Used only in non-interactive mode. If specified, forcefully refresh the cached access token.",
)
def login(
    org: str, api_token: str, client_id: str, client_secret: str, browser: bool, details: bool, refresh: bool, **kwargs
):
    """Login Horizon Cloud Service.

    This command works with the current profile and will update the current profile. If no token is specified, a browser will be launched to login interactively.

    \b
    Examples:
        1. Login with configured credentials, otherwise do an interactive login using browser:
            hcs login
        2. Get login details:
            hcs login -d
        3. Login with CSP user API token:
            hcs login --api-token <your-csp-user-api-token>
        4. Login with OAuth client id/secret:
            hcs login --client-id <oauth-client-id> --client-secret <oauth-client-secret>
    """

    current_profile = _ensure_current_profile()
    csp = current_profile.csp

    err = _validate_auth_method(
        org=org, api_token=api_token, client_id=client_id, client_secret=client_secret, browser=browser
    )
    if err:
        return err

    # if org is specified
    if org:
        # update the profile
        csp.orgId = org
    else:  # no org id is specified.
        # try using the org_id from profile
        org = csp.orgId

    if api_token:
        _clear_credentials(csp)
        csp.apiToken = api_token
    elif client_id:
        _clear_credentials(csp)
        csp.clientId = client_id
        csp.clientSecret = client_secret
    elif browser:
        _clear_credentials(csp)
    else:
        # auto detect mode.
        pass

    interactive = not csp.apiToken and not csp.clientId

    # If this is interactive login, it's not ready on production yet. Raise error
    if interactive and not login_support.identify_client_id(csp.url):
        return ctxp.error(
            "The interactive login on the specified stack is not yet available. Try a different authentication method."
        )

    # If there's existing login info and the org ID is different, logout first
    existing_auth_data = ctxp.profile.auth.get()
    if existing_auth_data:
        ret = sglib.auth.details_from_token(existing_auth_data.token)
        if csp.orgId and ret["org"].id != csp.orgId:
            if not interactive:
                _echo("Switching to organization " + csp.orgId)
            ctxp.profile.auth.delete()

    oauth_token = sglib.auth.login(force_refresh=refresh)
    if not oauth_token:
        if interactive:
            oauth_token = _do_browser_login()
            if oauth_token:
                sglib.auth.use_oauth_token(oauth_token)
        if not oauth_token:
            return ctxp.error("Login failed")
    # else: the token still works

    ctxp.profile.save()

    auth_details = sglib.auth.details(get_org_details=details)
    if csp.orgId:
        if auth_details["org"].id != csp.orgId:
            return ctxp.error(
                "Org ID from auth info does not match org ID in the profile config. Use 'hcs profile edit' to fix."
            )
    else:
        # org id not specified in profile. Add it.
        csp.orgId = auth_details["org"].id
        ctxp.profile.save()

    recent.set("org", org)
    return auth_details if details else oauth_token["access_token"]


def _echo(msg):
    click.echo(click.style(msg, fg="yellow"), err=True)


def _do_browser_login():
    csp_config = ctxp.profile.current().csp
    org_id = csp_config.orgId

    _echo("Logging to HCS...")
    _echo(f"  CSP:          {csp_config.url}")
    _echo(f"  Organization: {org_id if org_id else '<default>'}")
    _echo(f"  Profile:      {ctxp.profile.name()}")
    _echo(
        f"A web browser has been opened at {csp_config.url}. Continue the login in the web browser, and return to this terminal."
    )
    token = login_support.login_via_browser(csp_config.url, org_id)
    if token:
        _echo("Success.")
        if not org_id:
            org_id = sglib.auth.get_org_id_from_token(token)
            _echo(f"Actual org ID: {org_id}")
    return token


def _ensure_current_profile():
    profile = ctxp.profile
    data = profile.current(exit_on_failure=False)
    if not data:
        profile_support.ensure_default_production_profile()
    return profile.current()


def _clear_credentials(csp):
    csp.apiToken = None
    csp.clientId = None
    csp.clientSecret = None


def _validate_auth_method(org: str, api_token: str, client_id: str, client_secret: str, browser: bool):
    # validation: API-token and org ID must not be specified together
    if org and api_token:
        return "Invalid arguments. CSP API user token is org-scoped. --org is not needed with --api-token.", 1

    # validation: must not specify duplicated auth methods
    ret = {}
    if api_token:
        ret["api_token"] = 1
    if client_id:
        ret["client_id/secret"] = 1
    if browser:
        ret["browser"] = 1

    if len(ret) > 1:
        return ctxp.error(f"Specify only one authenticate method. Currently specified: {list(ret.keys())}")

    if client_id and not client_secret or not client_id and client_secret:
        return ctxp.error("--client-id and --client-secret must be used in pair.")

    if client_id and not client_secret:
        return ctxp.error(f"Missing --client-secret, when --client-id is specified.")
