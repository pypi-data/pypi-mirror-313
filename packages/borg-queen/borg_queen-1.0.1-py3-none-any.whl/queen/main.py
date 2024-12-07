import sys

import sentry_sdk

from . import backup, logs, parsing
from .exceptions import QueenException


def main():
    args = parsing.parse_arguments(sys.argv[1:])

    config = parsing.parse_config()
    sentry_sdk.init(config.sentry_dsn)
    logs.config(config.log_directory, config.log_stdout)

    # parse sites
    site_configs = []
    for site_config_path in args["site_configs"]:
        try:
            site_config = parsing.parse_site(site_config_path)
        except QueenException as e:
            logs.logger.exception("error parsing %s" % site_config_path)
            sentry_sdk.capture_exception(e)
            continue

        site_configs.append(site_config)

    # backup sites
    logs.logger.info("beginning backup")

    for site_config in site_configs:
        project_name = site_config["project_name"]

        try:
            logs.logger.debug("beginning backup for %s" % project_name)
            backup.site(config, site_config, args["interactive"])
            logs.logger.debug("completed backup for %s" % project_name)
        except QueenException as e:
            logs.logger.exception("failed backup for %s" % project_name)
            sentry_sdk.capture_exception(e)

    logs.logger.info("completed backup")
