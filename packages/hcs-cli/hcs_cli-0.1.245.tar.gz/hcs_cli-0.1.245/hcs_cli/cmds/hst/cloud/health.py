import click

from hcs_ext_hst.base.helper import print_profile, panic, reduce_log
from hcs_ext_hst import hst_test_cloudhealth


@click.group(invoke_without_command=True)
@click.option("--show-all/--show-error-only", type=bool, default=True)
@click.option("--output-table/--output-json", type=bool, default=True, help="Specify output format")
@click.option(
    "--regions",
    type=str,
    required=False,
    help="Specify target regions (separated by comma). If not specified, all regions will be tested.",
)
def cloudhealth(show_all: bool, output_table: bool, regions: str):
    """Test cloud agent health"""
    print_profile()
    reduce_log()
    try:
        success = hst_test_cloudhealth.test(show_all, output_table, regions)
        if not success:
            panic("Cloud health test failed", 299)
    except Exception as e:
        panic(f"Cloud health test failed: {str(e)}", 299)
