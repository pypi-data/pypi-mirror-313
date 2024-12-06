import csv
import logging
from io import StringIO
from pathlib import Path

import click
from nagra_network_misc_utils.gitlab import add_mr_comment, post_git_diff

from .schema import check_records, sort_records

log = logging.getLogger("Record checker")


@click.command(
    "check",
    help="Check that the CSV file is compliant with Terraform module",
)
@click.option(
    "-f",
    "--file",
    type=Path,
    help="Name of the file to check",
    default="dns_records.csv",
)
def check_csvfile(file: Path):
    if not file.is_file():
        log.warn("File does not exist. Ignoring validation")
        return
    if file.suffix != ".csv":
        log.warn("File must be a .csv file")
        return
    with open(file) as f:
        try:
            check_records(csv.DictReader(f))
        except Exception as e:
            log.error(e)
            add_mr_comment(str(e))
            exit(1)
    log.info(f"File {file} is valid")


@click.command(
    "sort",
    help="Sort the CSV file",
)
@click.option(
    "-f",
    "--file",
    type=Path,
    help="Name of the file to check",
    default="dns_records.csv",
)
def sort_csvfile(file: Path):
    header = ("name", "type", "content", "ttl", "proxied")
    content = file.read_text()

    # Sort file
    records = list(csv.DictReader(StringIO(content), fieldnames=header))
    records = records[1:]  # Remove header
    records = sort_records(records)
    output_buffer = StringIO()
    writer = csv.DictWriter(
        output_buffer,
        fieldnames=header,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(records)
    result = output_buffer.getvalue()

    # Dump file
    file.write_text(result)
    # Report difference in git if needed
    post_git_diff()
    # Exit with error status code if a difference is detected
    if result != content:
        logging.info("File was not correctly sorted")
        exit(1)
