import click

from hcs_ext_hst.base.helper import print_profile, panic
from hcs_ext_hst import hst_test_installer


@click.group(invoke_without_command=True)
@click.option(
    "--group",
    help="Test groups to run, in a comma separated string of group names. If not specified, the default group will be used.",
)
@click.option("--parallel/--sequential", default=True, help="Whether to execute tests in parallel.")
@click.option(
    "--case",
    type=str,
    default=None,
    help="Optionally specify the name of the case to run. Could be relative path, or partial case name.",
)
def installer(group: str, parallel: bool, case: str):
    """Perform an integration test with the cloud. Do a basic test for the Windows installer."""
    print_profile()
    if group and case:
        panic("Group and case can not be specified together. Use only one of them.")
    success = hst_test_installer.test(group, parallel, case)
    if not success:
        panic("Windows client test failed", 199)
