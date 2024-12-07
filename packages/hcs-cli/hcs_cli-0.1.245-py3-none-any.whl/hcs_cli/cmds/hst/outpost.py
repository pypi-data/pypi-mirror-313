import json
import sys
import traceback
import logging
import click

from hcs_ext_hst.base import common_op
from hcs_ext_hst.base.health_check import HealthCheck
from hcs_ext_hst.base.helper import smart_case_name, panic, reduce_log, print_data, exit_on_error
from hcs_ext_hst.base.outpost import Outpost
from hcs_ext_hst.base.probe import Probe

log = logging.getLogger(__name__)


def _parse_property_list(property_list: list) -> dict:
    if not property_list:
        return
    ret = {}
    for pair in property_list:
        parts = pair.split(":")
        if len(parts) != 2:
            panic("Invalid property: " + pair)
        ret[parts[0]] = parts[1]
    return ret


@click.group()
def outpost():
    """Commands for outpost"""


@outpost.command("reg")
@click.option("--name", type=str, default=None, help="Specify the outpost name.")
@click.option(
    "--property",
    "-p",
    type=str,
    multiple=True,
    help="Specify additional properties of the outpost, as colon separated key-value pair. Can be specified multiple times.",
)
def outpost_reg(name: str, property: list):
    """Register an outpost"""
    reduce_log()
    o = Outpost()
    if not name:
        name = "cli-" + o._test_id
    o.register(name, _parse_property_list(property))
    print(json.dumps(o.data, indent=4))


@outpost.command("del")
@click.option(
    "--search", type=str, help="Specify search criteria. Either search criteria or IDs must be specified, but not both."
)
@click.argument("id", nargs=-1, type=str)
def outpost_del(search: str, id: list):
    """Delete outposts"""
    reduce_log()

    items = _get_outposts(search, id)

    click.echo("Outposts to delete: %d" % len(items))
    has_error = False
    for i in items:
        if type(i) == str:
            outpost_id = i
            click.echo("Deleting outpost: " + outpost_id)
        else:
            outpost_id = i.id
            click.echo(f"Deleting outpost: {outpost_id}, {i.name}")
        try:
            common_op.outposts.delete(outpost_id)
        except:
            traceback.print_exc()
            has_error = True
    if has_error:
        sys.exit(1)


@outpost.command("idle")
@click.option("--case", type=str, default=None, help="Optionally specify the case name to create for the outpost.")
@click.option(
    "--renew/--reuse", type=bool, default=True, help="Whether to reuse the previous outpost, or recreate a new one."
)
@click.option("--name", type=str, default=None, help="Create outpost with the specified name.")
@click.option("--cloud-region", type=str, default=None, help="The region of creating cloud outpost.")
@click.option(
    "--property",
    "-p",
    type=str,
    multiple=True,
    help="Specify additional properties of the outpost, as colon separated key-value pair. Can be specified multiple times.",
)
@click.option("--silent/--verbose", type=bool, default=False, help="Control stdout")
@click.option(
    "--hive-mode/--sync-mode", type=bool, default=False, help="Hive mode will have the process in background."
)
def outpost_idle(case: str, renew: bool, name: str, cloud_region: str, property: list, silent: bool, hive_mode: bool):
    """This command registers an HST Outpost on the cloud, and launches an Outpost instance locally and pair with the cloud."""

    try:
        if not cloud_region:
            outpost = Outpost()
        else:
            outpost = Outpost(cloud_region=cloud_region)
        if renew:
            if name:
                name = name + "-" + outpost._test_id
            outpost.register(name, _parse_property_list(property))
        else:
            if name:
                panic("Can not specify name when reusing an outpost.")
            if property:
                panic("Can not specify property when reusing an outpost.")
            outpost.load_from_context()

        if case:
            Probe(outpost.id()).create(smart_case_name(case))

        outpost.launch(silent)

        if hive_mode:
            pass
        else:
            code = outpost.wait()
            log.info(f"Outpost exited with {code}")
    finally:
        if not hive_mode:
            outpost.kill()


@outpost.command("start")
@click.option("--key", "-k", type=str, default=None, help="Start and pair the outpost by pairing key.")
@click.option("--id", type=str, default=None, help="Start and pair the outpost by ID.")
def outpost_start(key: str, id: str):
    """Start a local outpost instance, pairing with an existing outpost record on the cloud."""
    try:
        outpost = Outpost()
        outpost.start(pairing_key=key, outpost_id=id)
        code = outpost.wait()
        log.info(f"Outpost exited with {code}")
    finally:
        outpost.kill()


@outpost.command("health")
@click.option(
    "--search", type=str, help="Specify search criteria. Either search criteria or IDs must be specified, but not both."
)
@click.option("--show-all/--show-error-only", type=bool, default=True)
@click.option("--output-table/--output-json", type=bool, default=False, help="Specify output format")
@click.argument("id", nargs=-1, type=str)
def outpost_health(search: str, show_all: bool, output_table: bool, id: list):
    """Check health of outposts, by running a dummy test on outposts."""
    reduce_log()

    items = _get_outposts(search, id)

    checker = HealthCheck(items, print_table=output_table, show_error_only=not show_all)
    ret, num_errors = checker.check()

    if not output_table:
        print_data(ret)

    if num_errors > 0:
        sys.exit(1)


def _get_outposts(search: str, ids: list) -> list:
    total_items = len(ids)

    if not search and total_items == 0:
        panic("Either search criteria or ID must be specified.")
    if search and total_items > 0:
        panic("Search criteria and ID must not be specified together.")

    if total_items:
        return ids
    return common_op.outposts.list(search)


@outpost.command("get")
@click.argument("id", nargs=1, type=str)
def outpost_get(id: str):
    """Get information of an outpost."""
    reduce_log()

    def fn():
        o = Outpost().use(id)
        print_data(o.data)

    exit_on_error(fn)


@outpost.command("list")
@click.option("--search", type=str, required=False, help="The search string. E.g. 'name $eq alice")
@click.option(
    "--first/--all",
    type=bool,
    required=False,
    default=False,
    help="Return the first element if any, instead of the full list.",
)
@click.option(
    "--id-only/--full-object",
    type=bool,
    required=False,
    default=False,
    help="Return only ID, instead of a the full object.",
)
@click.option(
    "--output", type=click.Choice(["json", "plain", "table"]), default="json", help="Specify the output format"
)
def outpost_list(search: str, first: bool, id_only: bool, output: str):
    """List outposts."""
    reduce_log()

    if first:
        ret = common_op.outposts.first(search)
        if not ret:
            return
        if id_only:
            ret = ret.id
    else:
        ret = common_op.outposts.list(search)
        if ret and id_only:
            ret = list(map(lambda o: o.id, ret))

    print_data(ret, output)
