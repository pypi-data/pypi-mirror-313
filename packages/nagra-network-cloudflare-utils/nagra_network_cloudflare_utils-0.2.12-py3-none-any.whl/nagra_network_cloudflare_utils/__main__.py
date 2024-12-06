import logging

import click
from nagra_network_misc_utils.logger import set_default_logger

from nagra_network_cloudflare_utils.compliance import remove_cloudflare_records
from nagra_network_cloudflare_utils.dns_checker import check_csvfile, sort_csvfile
from nagra_network_cloudflare_utils.list_zones import list_zones

set_default_logger()
logging.getLogger().setLevel(logging.WARNING)


LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL,
    "error": logging.ERROR,
    "warn": logging.WARNING,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "notset": logging.NOTSET,
}


# Keep it as the main entry point
@click.group()
@click.option(
    "--log-level",
    type=click.Choice(
        ["critical", "fatal", "error", "warn", "warning", "info", "debug", "notset"]
    ),
    default="info",
)
def main(log_level):
    # This sets a convenient global handler for the logs
    set_default_logger()
    logging.getLogger().setLevel(LOG_LEVELS[log_level])


main.add_command(check_csvfile)
main.add_command(sort_csvfile)
main.add_command(remove_cloudflare_records)
main.add_command(list_zones)

if __name__ == "__main__":
    main()
