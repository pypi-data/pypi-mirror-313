import sys

import click

from hcs_ext_hst.base.helper import print_profile, panic
from hcs_ext_hst import hst_test_main


@click.group(invoke_without_command=True)
@click.option(
    "--group",
    help="Test groups to run, in a comma separated string of group names. If not specified, the default group will be used.",
)
@click.option(
    "--case",
    type=str,
    default=None,
    help="Optionally specify the name of the case to run. Could be relative path, or partial case name.",
)
@click.option(
    "--list/--run",
    type=bool,
    required=False,
    default=False,
    help="List test cases without actual run.",
)
@click.option("--parallel/--sequential", default=True, help="Whether to execute tests in parallel.")
@click.option(
    "--cleanup/--no-cleanup",
    default=True,
    help="If cleanup, the records and logs will be deleted upon successful run. Default: True",
)
@click.option(
    "--outpost",
    type=str,
    default=None,
    help="Specify the outpost to run the tests. Values: 1. 'local' - create a new local outpost. 2. 'cloud/<region>' - create a cloud outpost with the region, e.g. 'cloud/westus2'. 3. 'reuse/<existing-outpost-id>' - reuse an existing outpost. If not specified, the 'local' mode will be used.",
)
@click.option(
    "--longrun/--single-run", default=False, help="Long-run mode will run the test forever until an error occured."
)
def test(group: str, case: str, list: bool, parallel: bool, cleanup: bool, outpost: str, longrun: bool):
    """Perform an integration test with the cloud. If outpost is not specified, a local Outpost instance will be launched and paired."""
    print_profile()

    if group and case:
        panic("Group and case can not be specified together. Use only one of them.")

    if list:
        hst_test_main.list()
        return

    while True:
        success = hst_test_main.test(
            group_names=group,
            case_name=case,
            parallel=parallel,
            cleanup=cleanup,
            outpost_mode=outpost,
        )
        if not success:
            sys.exit(11)
        if not longrun:
            break
