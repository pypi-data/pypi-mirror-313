import os.path
from dataclasses import dataclass
from typing import Dict

import toml

from queen.exceptions import QueenException

CONFIG_PATH = "/etc/queen/queen.toml"


@dataclass(frozen=True)
class Config:
    repo_prefix: str
    sentry_dsn: str
    log_directory: str
    log_stdout: bool
    borg_env: Dict[str, str]
    plugins: dict


def parse_config():
    try:
        with open(CONFIG_PATH) as f:
            contents = f.read()
    except FileNotFoundError:
        raise QueenException(f"{CONFIG_PATH}: No such file or directory")

    parsed = toml.loads(contents)

    repo_prefix = parsed.get("repo_prefix")
    if repo_prefix is None:
        raise QueenException("'repo_prefix' key is required")

    if "@" not in repo_prefix:
        # Local repo. Convert to absolute, since we may invoke borg with a
        # different cwd
        repo_prefix = os.path.abspath(repo_prefix)

    sentry_dsn = parsed.get("sentry_dsn")
    if sentry_dsn is None:
        raise QueenException("'sentry_dsn' key is required")

    log_stdout = parsed.get("logging", {}).get("use_stdout")
    if log_stdout is None:
        log_stdout = False

    log_directory = parsed.get("logging", {}).get("directory")
    if log_directory is None:
        log_directory = ""
        if not log_stdout:
            raise QueenException(
                "'logging.directory' key is required or set 'logging.set_stdout' to true"
            )
    elif not os.path.isabs(log_directory):
        raise QueenException("'logging.directory' must be absolute")

    borg_env = parsed.get("borg_env", {})
    if not isinstance(borg_env, dict):
        raise QueenException("'borg_env' must be a table")

    plugins = parsed.get("plugins", {})
    if not isinstance(plugins, dict):
        raise QueenException("'plugins' must be a table")

    for key, plugin_config in plugins.items():
        if not isinstance(plugin_config, dict):
            raise QueenException(f"'plugins.{key}' must be a table")

    return Config(
        repo_prefix=repo_prefix,
        sentry_dsn=sentry_dsn,
        log_directory=log_directory,
        log_stdout=log_stdout,
        borg_env=borg_env,
        plugins=plugins,
    )
