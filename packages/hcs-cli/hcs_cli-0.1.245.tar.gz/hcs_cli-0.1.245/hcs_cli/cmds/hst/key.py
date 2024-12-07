import json

import click
import logging

import hcs_ext_hst.base.cfg_mgr_delegate as cfg_mgr_delegate
import hcs_ext_hst.base.helper as helper

log = logging.getLogger(__name__)


@click.group()
def key():
    pass


@key.command("decode")
@click.argument("id", nargs=-1, type=str)
def decode(id: list):
    """Print details of the pairing key stored. Optionally specify test ID to decode pairing key for the test instance."""
    helper.reduce_log()
    if id:
        cfg_mgr_delegate.enable_multi_node(id[0])
    pairing_key = cfg_mgr_delegate.try_read_pairing_key()
    if not pairing_key:
        click.echo("Pairing key not found")
        return

    decoded = helper.decode_pairing_key(pairing_key)
    click.echo(json.dumps(decoded, indent=4))
