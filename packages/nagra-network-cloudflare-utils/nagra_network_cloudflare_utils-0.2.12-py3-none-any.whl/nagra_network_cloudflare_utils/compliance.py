import json
import logging
from pathlib import Path

import click
from cloudflare import Cloudflare
from glom import flatten, glom

from .schema import check_records

log = logging.getLogger("Compliance check")


def check_records_compliance(records_from_cloudflare, records_from_file):
    for record in records_from_file:
        if record in records_from_cloudflare:
            records_from_cloudflare.remove(record)
    return records_from_cloudflare


def extract_records_dict(data):
    return [
        r["value"]
        for r in flatten(glom(data, ("**.resources")))
        if r["type"] == "cloudflare_record" and "value" in r
    ]


def records_from_tf_output(file):
    with open(file) as f:
        data = json.load(f)
    values = extract_records_dict(data)
    records, _valid = check_records(values)
    return {r.id: r for r in records}


def records_from_cloudflare(cf, zone_id):
    cloudflare_records = [
        rec.model_dump() for rec in cf.dns.records.list(zone_id=zone_id, per_page=1000)
    ]
    cloudflare_records, _valid = check_records(cloudflare_records)
    return {r.id: r for r in cloudflare_records}


@click.command(
    "remove", help="Remove Cloudflare DNS records that are not defined in Terraform"
)
@click.option(
    "-t",
    "--token",
    type=str,
    # The lib automaticly consider this option
    # envvar="CLOUDFLARE_API_TOKEN",
    help="Cloudflare API token",
)
@click.option(
    "-z",
    "--zone",
    "zone_id",
    type=str,
    envvar="ZONE_ID",
    help="Cloudflare Zone to process",
)
@click.option(
    "-f",
    "--file",
    "statefile",
    type=Path,
    help="Terraform tfplan file (must be in json format)",
    default="plan.tfplan.json",
)
@click.option(
    "--test",
    type=bool,
    is_flag=True,
    help=("Do not delete, only display the records " "that would have been deleted"),
    default=False,
)
def remove_cloudflare_records(token, zone_id, statefile, test):
    cf_config = {}
    if token:
        cf_config["token"] = token
    cf = Cloudflare(**cf_config)
    cf_records = records_from_cloudflare(cf, zone_id)
    state_records = records_from_tf_output(statefile)
    records_to_remove = [
        r for r_id, r in cf_records.items() if r_id not in state_records
    ]
    records_to_remove.sort(key=lambda r: r.name)
    if not records_to_remove:
        log.warn("No record to remove")
    elif test:
        print(
            "The following records should be removed:\n{}".format(
                "\n".join(str(r) for r in records_to_remove)
            )
        )
    else:
        log.warn(
            "The following records will be removed:\n{}".format(
                "\n".join(str(r) for r in records_to_remove)
            )
        )
        for record in records_to_remove:
            cf.remove(zone_id, record.id)
        log.info("Records have been removed")
