import os

from queen import processes


def backup(global_config, config_dicts, out_dir):
    for config_dict in config_dicts:
        merged_config = {**global_config, **config_dict}

        database = merged_config["database"]

        args = ["mysqldump"]

        if "host" in merged_config:
            args.append(f"--host={merged_config['host']}")

        if "port" in merged_config:
            args.append(f"--port={merged_config['port']}")

        if "user" in merged_config:
            args.append(f"--user={merged_config['user']}")

        if "password" in merged_config:
            args.append(f"--password={merged_config['password']}")

        args.append(database)

        dump_name = os.path.join(out_dir, "%s.dump.sql" % database)

        # Pipe mysqldump's output through our process and write it ourselves,
        # since it may not have permissions to write it to the out_dir.
        with open(dump_name, "wb") as dump_file:
            processes.run(args, stdout=dump_file)
