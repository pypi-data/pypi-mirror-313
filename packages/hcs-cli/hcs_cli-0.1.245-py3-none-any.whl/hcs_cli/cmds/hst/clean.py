from pathlib import Path

import click

from hcs_core import sglib
from hcs_core.ctxp import context, profile
import logging
from hcs_ext_hst.base import cfg_mgr_delegate
from hcs_ext_hst.cloud_agent_utils import clean_all_probes_on_cloud_agent


log = logging.getLogger(__name__)

client = None


def _client():
    global client
    if client is None:
        client = sglib.hcs_client(profile.current().hcs.url)


@click.group(invoke_without_command=True)
@click.option("--delete-outposts/--keep-outposts", default=True)
@click.option("--delete-probes", type=click.Choice(["all", "orphan", "none"]), default="all")
@click.option("--delete-reports/--keep-reports", default=True)
@click.option("--delete-local-logs/--keep-local-logs", default=True)
@click.option("--delete-local-states/--keep-local-states", default=True)
@click.option(
    "--cloud-region",
    type=str,
    default=None,
    help="Specify the region to delete the probes",
)
def clean(delete_outposts, delete_probes, delete_reports, delete_local_logs, delete_local_states, cloud_region):
    """Delete all Outposts, Probes, and Reports from the cloud. Delete local logs and state files."""

    if delete_outposts:
        _delete_impl("outposts")
        context.delete("outpost")

    if delete_probes == "all":
        _delete_impl("probes")
        if cloud_region:
            clean_all_probes_on_cloud_agent(cloud_region)
    elif delete_probes == "orphan":
        _delete_orphan_probes()
    else:
        pass

    if delete_reports:
        _delete_impl("reports")
    if delete_local_logs:
        _delete_local_logs()
    if delete_local_states:
        _delete_local_states()


def _delete_orphan_probes():
    log.info("Deleting orphan probes...")

    def filter(probe):
        return not probe.outpostIds

    _delete_impl("probes", filter)


def _delete_local_logs():
    # delete logs
    for p in Path("./logs").glob("hst-*.log"):
        log.info(f"Delete log: {p.name}")
        p.unlink()


def _delete_impl(type: str, fn_filter: callable = None):
    ctx = f"/synthetic-testing/v1/{type}"
    deleted = 0
    while True:
        page = _client().get(ctx + "?size=200")
        progress = 0
        for i in page.content:
            if fn_filter and not fn_filter(i):
                log.info(f"Skipping {type} {i.id}, {i.name}")
                continue
            log.info(f"Deleting {type} {i.id}, {i.name}")
            _client().delete(ctx + "/" + i.id)
            progress += 1
        if not progress:
            break
        deleted += progress
    log.info(f"Deleted {type} {deleted}")


def _delete_local_states():
    for p in Path(cfg_mgr_delegate.config_path).glob("*"):
        log.info(f"Delete state file: {p.absolute()}")
        p.unlink()
