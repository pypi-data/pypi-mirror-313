import click
import re
from hcs_core.sglib import cli_options as cli
from hcs_cli.service import hoc
from hcs_core.ctxp.timeutil import human_delta_to_iso


def _formalize_query_string(input_str):
    parts = re.split(r"(?= AND | OR )", input_str)

    for i in range(len(parts)):
        part = parts[i].strip()

        if ":" in part:
            key, value = part.split(":", 1)
            value = value.strip()

            if not (value.startswith('"') and value.endswith('"')):
                value = f'\\"{value}\\"'

            parts[i] = f"{key}:{value}"
        else:
            parts[i] = f'"{part}"'

    return " ".join(parts).strip()


@click.command()
@cli.org_id
@click.option(
    "--from",
    "from_param",
    type=str,
    required=False,
    default="-12h",
    help="Sepcify the from date. E.g. '-1d', or '-1h35m', or '-1w', or '2023-12-04T00:19:22.854Z'.",
)
@click.option(
    "--to",
    type=str,
    required=False,
    default="now",
    help="Sepcify the to date. E.g. 'now', or '-1d', or '-1h35m', or '-1w', or '2023-12-04T00:19:22.854Z'.",
)
@click.option("--service", "-s", type=str, required=True, help="Service name. E.g. inv, lcm")
@click.option("--type", "-t", type=str, required=True, help="Message type. E.g. us:rq:dt, us:rq:vm, us:res:vm")
@click.option(
    "--query",
    "-q",
    type=str,
    required=False,
    help="Additional query. E.g. 'data.d.vid:vm-001 AND data.d.tid:66e05866bc6a4b7401c1419d'",
)
def search(org: str, from_param: str, to: str, service: str, type: str, query: str):
    """Search HOC events.
    E.g. hcs hoc search -s inv -t us:rq:dt --from -1w -q data.d.s:ns
    """
    org_id = cli.get_org_id(org)
    payload = {
        "from": human_delta_to_iso(from_param),
        "to": human_delta_to_iso(to),
        "searchType": "SEARCH_HOC_EVENTS",
        "searchParams": {"search_src": service, "search_type": f'\\"{type}\\"'},
        "searchLocation": "US",
        "additionalFilters": f'AND data.d.oid:\\"{org_id}\\"',
    }

    if query:
        payload["additionalFilters"] += " AND " + _formalize_query_string(query)
    # return payload
    return hoc.search(payload)
