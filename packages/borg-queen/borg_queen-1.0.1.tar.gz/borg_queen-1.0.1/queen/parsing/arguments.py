import argparse
import os
import os.path
import sys

SITE_CONFIG_DIR = "/etc/queen/sites.d/"


def _discover_sites(site_config_dir):
    if os.path.exists(site_config_dir):
        for conf_file in sorted(os.listdir(site_config_dir)):
            if conf_file.endswith(".toml"):
                yield os.path.join(site_config_dir, conf_file)


def parse_arguments(argv):
    """parse queen's command line arguments"""
    parser = argparse.ArgumentParser(description="Take backups using Borg")

    site_config_help = (
        "Backup using the supplied config file instead of those in %s" % SITE_CONFIG_DIR
    )
    parser.add_argument("-s", "--site-config", help=site_config_help)

    raw_args = parser.parse_args(argv)

    args = {
        "interactive": sys.stdout.isatty(),
    }

    # site configs
    if raw_args.site_config is not None:
        site_configs = [raw_args.site_config]
    else:
        site_configs = list(_discover_sites(SITE_CONFIG_DIR))
    args["site_configs"] = site_configs

    return args
