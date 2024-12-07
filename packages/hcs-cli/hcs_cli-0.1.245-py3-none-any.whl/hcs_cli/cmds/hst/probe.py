import sys

import click
import logging
from hcs_ext_hst.base import common_op
from hcs_ext_hst.base.helper import panic, reduce_log, print_data, exit_on_error
from hcs_ext_hst.base.outpost import Outpost
from hcs_ext_hst.base.probe import Probe

log = logging.getLogger(__name__)


@click.group()
def probe():
    """Commands for probe"""


@probe.command("del")
@click.option(
    "--search", type=str, help="Specify search criteria. Either search criteria or IDs must be specified, but not both."
)
@click.option(
    "--orphan-only/--any-probe",
    type=bool,
    default=False,
    help="If orphan-only is specified, only probes without outposts will be deleted.",
)
@click.argument("id", nargs=-1, type=str)
def probe_del(search: str, orphan_only: bool, id: list):
    """Delete probes"""
    reduce_log()

    if not search and not orphan_only and not id:
        panic("Either search criteria or ID must be specified.")
    if search and id:
        panic("Search criteria and ID must not be specified together.")
    if orphan_only and id:
        panic("--orphan-only mode can not be used with IDs")

    error_occured = False

    def _delete(probe_id, name):
        click.echo(f"       Deleting probe: {probe_id} {name}")
        try:
            common_op.probes.delete(probe_id)
        except Exception as e:
            click.secho(e, fg="bright_red")
            nonlocal error_occured
            error_occured = True

    if id:  # delete by IDs
        click.echo("Probes to delete: %d" % len(id))
        for i in id:
            _delete(i, "")
    else:  # delete by search
        items = common_op.probes.list(search)
        click.echo("Probes to delete: %d" % len(items))
        for p in items:
            name = p.testConfig.name
            if orphan_only and p.outpostIds:
                click.echo(f"Skip non-orphan probe: {p.id} {name}")
                continue
            _delete(p.id, name)

    if error_occured:
        sys.exit(1)


@probe.command("get")
@click.argument("id", nargs=1, type=str)
def probe_get(id: str):
    """Get information of a probe."""
    reduce_log()

    def fn():
        o = common_op.probes.get(id)
        print_data(o)

    exit_on_error(fn)


@probe.command("reg")
@click.option("--outpost", "-o", type=str, required=True, help="Specify the outpost IDs to associate with.")
@click.option("--template", "-t", type=str, required=True, help="Specify the case name to create for the outpost.")
def probe_reg(outpost: str, template: str):
    """Register a probe."""
    reduce_log()

    o = Outpost().use(outpost)
    p = Probe(outpost).create(template)
    print_data(p.data)


@probe.command("list")
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
def probe_list(search: str, first: bool, id_only: bool, output: str):
    """List probes."""
    reduce_log()

    if first:
        ret = common_op.probes.first(search)
        if not ret:
            return
        if id_only:
            ret = ret.id
    else:
        ret = common_op.probes.list(search)
        if ret and id_only:
            ret = list(map(lambda o: o.id, ret))

    print_data(ret, output)
