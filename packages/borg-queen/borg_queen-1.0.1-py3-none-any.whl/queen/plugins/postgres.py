import dataclasses
import os
import urllib.parse

from queen import exceptions, processes


def _make_connection_string(database, *, user, password, host, port):
    query_params = {}
    if user is not None:
        query_params["user"] = user

    if password is not None:
        query_params["password"] = password

    if host is not None:
        query_params["host"] = host

    if port is not None:
        query_params["port"] = port

    encoded_query = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    url = urllib.parse.quote(database)
    if encoded_query:
        url = f"{url}?{encoded_query}"

    return f"postgresql:///{url}"


@dataclasses.dataclass(frozen=True)
class Config:
    database: str
    user: str = None
    password: str = None
    host: str = None
    port: int = None
    pg_dump: list = dataclasses.field(default_factory=lambda: ["pg_dump"])

    @property
    def connection_string(self):
        return _make_connection_string(
            self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )


def _parse_config(global_config, config_dict):
    merged_config = {**global_config, **config_dict}

    if "database" not in merged_config:
        raise exceptions.QueenException("missing database from postgres config")

    if "pg_dump" in merged_config:
        if not isinstance(merged_config["pg_dump"], list):
            raise exceptions.QueenException("pg_dump must be a list")

    supported_fields = [f.name for f in dataclasses.fields(Config)]
    extra_keys = merged_config.keys() - supported_fields
    if extra_keys:
        extra_keys_str = ", ".join(sorted(extra_keys))
        raise exceptions.QueenException(
            "unsupported fields for postgres config: %s" % extra_keys_str
        )

    return Config(**merged_config)


def backup(global_config, config_dicts, out_dir):
    for config_dict in config_dicts:
        # Legacy config. Can't really test it, since legacy config didn't allow
        # specification of host, port etc.
        if isinstance(config_dict, str):  # pragma: no cover
            config_dict = {"database": config_dict}

        config = _parse_config(global_config, config_dict)

        args = config.pg_dump + ["--format", "custom", config.connection_string]

        # Pipe pg_dump's output through our process and write it ourselves,
        # since it may not have permissions to write it to the out_dir.
        dump_name = os.path.join(out_dir, "%s.pgdump" % config.database)
        with open(dump_name, "wb") as dump_file:
            processes.run(args, stdout=dump_file)
