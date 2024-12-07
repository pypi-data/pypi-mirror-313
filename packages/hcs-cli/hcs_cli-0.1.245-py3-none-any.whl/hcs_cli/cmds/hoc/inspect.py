import click
import hcs_core.sglib.cli_options as cli
import hcs_cli.service.hoc as hoc


@click.command()
@cli.org_id
@click.option("--template", "-t", required=False)
@click.option("--vm", "-v", required=False)
def inspect(org: str, template: str, vm: str):
    return hoc.inspect.inspect(org, template, vm)
