#!/usr/bin/env -S python3 -W ignore

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


import sys
import json
import click
import os.path as path
import logging

_script_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), "."))
_module_dir = _script_dir
if __name__ == "__main__":
    _cli_dir = path.dirname(_module_dir)
    sys.path.append(_cli_dir)

import hcs_core.ctxp as ctxp
from hcs_core.ctxp.util import panic, CtxpException
import hcs_core.ctxp.cli_options as cli_options

# -----------------------------------------------------------
import hcs_core.ctxp.logger as logger

logger.setup()
logging.getLogger("charset_normalizer").setLevel(logging.WARN)
logging.getLogger("csp").setLevel(logging.INFO)
logging.getLogger("context").setLevel(logging.WARN)
logging.getLogger("init").setLevel(logging.WARN)
logging.getLogger("profile").setLevel(logging.WARN)
logging.getLogger("httpx").setLevel(logging.WARN)
# logging.getLogger("hcs_core.sglib.login_support").setLevel(logging.DEBUG)
# logging.getLogger("login_support").setLevel(logging.DEBUG)
# -----------------------------------------------------------


@click.group()
@click.version_option(package_name="hcs-cli")
@click.option("--profile", "-p", type=str, required=False, help="Specify the profile to use. Optional.")
@click.option("--no-upgrade-check", is_flag=True, default=False, help="Check new version of HCS CLI.")
@click.option("--no-telemetry", is_flag=True, default=False, help="Send telemetry")
def cli(profile: str, no_upgrade_check: bool, no_telemetry: bool, **kwargs):

    if not no_upgrade_check:
        from hcs_core.util.versions import check_upgrade

        check_upgrade()

    if not no_telemetry:
        pass  # TODO

    if profile:
        ctxp.profile._active_profile_name = profile

    # ensure the default profile is available during fresh start
    if ctxp.profile.name() == "default":
        import hcs_cli.support.profile as profile_support

        profile_support.ensure_default_production_profile()


def main():
    commands_dir = path.join(_module_dir, "cmds")
    config_path = path.join(_module_dir, "config")
    ctxp.init(cli_name="hcs", main_cli=cli, commands_dir=commands_dir, config_path=config_path)


# def _on_http_error(e):
#     try:
#         err = json.loads(e.response.text)
#     except:
#         err = {"message": str(e), "response": e.response.text, "resource": str(e.request.url)}
#     text = json.dumps(err, indent=4)
#     panic(text)


if __name__ == "__main__":
    main()
