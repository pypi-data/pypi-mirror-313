import toml

from queen.exceptions import QueenException


def parse_site(site_path):
    """parse a site config"""
    with open(site_path) as f:
        data = f.read()

    config = toml.loads(data)

    if "passphrase" not in config:
        raise QueenException("'passphrase' key is required")

    if "project_name" not in config:
        raise QueenException("'project_name' key is required")

    return config
