import json
import logging

import click
from cloudflare import Cloudflare

log = logging.getLogger("Compliance check")


@click.command("list", help="List Cloudflare Zones")
@click.option(
    "-t",
    "--token",
    type=str,
    # The lib automaticly consider this option
    # envvar="CLOUDFLARE_API_TOKEN",
    help="Cloudflare API token",
)
@click.option(
    "-j",
    "--json",
    "json_format",
    type=str,
    is_flag=True,
    default=False,
    help="Cloudflare API token",
)
def list_zones(token, json_format):
    cf_config = {}
    if token:
        cf_config["token"] = token
    cf = Cloudflare(**cf_config)
    zones = [z.model_dump() for z in cf.zones.list()]
    if json_format:
        print(json.dumps(zones, indent=4))
    else:
        for z in zones:
            print("{name} (ID: {id})".format(**z))
