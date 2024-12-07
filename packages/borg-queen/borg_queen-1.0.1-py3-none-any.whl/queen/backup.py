import os
import os.path
from copy import copy
from tempfile import TemporaryDirectory

from . import logs, plugins, processes
from .exceptions import QueenSubprocessException


def _environ_with_pass(passphrase):
    new_environ = copy(os.environ)
    new_environ["BORG_PASSPHRASE"] = passphrase
    return new_environ


def _ensure_repo(path, passphrase):
    # We can't easily detect if the repo exists, especially over SSH. We'll
    # always create the repo and parse borg's stderr to check that.
    args = ["borg", "init", "-e", "repokey", str(path)]
    code, stderr = processes.launch(args, env=_environ_with_pass(passphrase))

    is_successful = code == 0
    repo_exists = code == 2 and "repository already exists" in stderr

    if not (is_successful or repo_exists):
        raise QueenSubprocessException(args, code, stderr)


def _create_archive(repo_path, passphrase, borg_env, paths, temp_dir, interactive):
    args = ["borg", "create"]

    if interactive:
        args.append("--progress")
        runner = processes.run_interactive
    else:
        runner = processes.run

    # add a trailing Z on the archive name, since borg's {utcnow} is a naive
    # ISO-8601 datetime.
    archive_name = "%s::{utcnow}Z" % repo_path
    args.append(archive_name)

    args += paths

    env = _environ_with_pass(passphrase)
    env.update(borg_env)
    kwargs = {
        "env": env,
    }
    if temp_dir is not None:
        kwargs["cwd"] = temp_dir

    runner(args, **kwargs)


def site(config, site_config, interactive):
    project_name = site_config["project_name"]
    passphrase = site_config["passphrase"]

    # Ensure repo exists.
    repo_path = os.path.join(config.repo_prefix, project_name)
    _ensure_repo(repo_path, passphrase)

    paths = []

    # add paths
    if "paths" in site_config:
        # paths += site_config["paths"]
        for path in site_config["paths"]:
            if os.path.exists(path):
                paths.append(path)
            else:
                logs.logger.warning(f"skipping missing path for {project_name}: {path}")

    # process plugins
    if "plugins" in site_config:
        temp_dir = TemporaryDirectory()

        plugins.backup(config.plugins, site_config["plugins"], project_name, temp_dir.name)
        paths.append("_queen")
    else:
        temp_dir = None

    logs.logger.debug("creating archive for %s" % project_name)
    _create_archive(
        repo_path,
        passphrase,
        config.borg_env,
        paths,
        temp_dir.name if temp_dir else None,
        interactive,
    )
    logs.logger.debug("created archive for %s" % project_name)

    if temp_dir:
        temp_dir.cleanup()
