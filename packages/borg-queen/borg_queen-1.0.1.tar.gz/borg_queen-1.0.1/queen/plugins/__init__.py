import os
import os.path

from queen import logs
from . import docker_volume, mysql, postgres

plugin_map = {
    "postgres": postgres.backup,
    "mysql": mysql.backup,
    "docker_volume": docker_volume.backup,
}


def backup(global_plugins_config, plugin_configs, project_name, temp_dir):
    # We want the borg archive to contain a top level directory called
    # "_queen", instead of some random path. We'll create a "_queen" directory
    # and add that to the archive.
    queen_dir = os.path.join(temp_dir, "_queen")
    os.mkdir(queen_dir)

    for plugin_name, plugin_config in plugin_configs.items():
        logs.logger.debug("processing %s plugin for %s" % (plugin_name, project_name))

        plugin_dir = os.path.join(queen_dir, plugin_name)
        os.mkdir(plugin_dir)

        # call plugin
        global_plugin_config = global_plugins_config.get(plugin_name, {})

        plugin_map[plugin_name](global_plugin_config, plugin_config, plugin_dir)

        logs.logger.debug("processed %s plugin for %s" % (plugin_name, project_name))
