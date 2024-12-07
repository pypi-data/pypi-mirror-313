import os.path

from queen import exceptions, processes


def backup(global_config, config_dicts, out_dir):
    for config_dict in config_dicts:
        merged_config = {**global_config, **config_dict}

        if "name" not in merged_config:
            raise exceptions.QueenException("missing name from docker_volume config")

        volume = merged_config["name"]
        image = merged_config.get("image", "alpine")

        docker_run_args = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{volume}:/mnt",
            "--log-driver",
            "none",
            image,
        ]
        tar_args = ["tar", "cf", "-", "-C", "/mnt", "."]

        args = docker_run_args + tar_args

        tarball_path = os.path.join(out_dir, f"{volume}.tar")

        with open(tarball_path, "wb") as tarball_file:
            processes.run(args, stdout=tarball_file)
