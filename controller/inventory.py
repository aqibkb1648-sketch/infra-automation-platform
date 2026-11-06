from pathlib import Path
import yaml


class Inventory:
    def __init__(self, config_path="config/servers.yml"):
        self.config_path = Path(config_path)
        self.data = self._load()

    def _load(self):
        if not self.config_path.is_file():
            raise FileNotFoundError(
                f"Inventory file not found: {self.config_path}"
            )

        with self.config_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        if not isinstance(data, dict):
            raise ValueError("Inventory must contain a YAML mapping.")

        servers = data.get("servers", [])

        if not isinstance(servers, list):
            raise ValueError("'servers' must be a YAML list.")

        names = set()

        for server in servers:
            if not isinstance(server, dict):
                raise ValueError("Each server entry must be a mapping.")

            for field in ("name", "container", "role"):
                if not server.get(field):
                    raise ValueError(
                        f"Server entry is missing required field: {field}"
                    )

            name = server["name"]

            if name in names:
                raise ValueError(f"Duplicate server name: {name}")

            names.add(name)

        return data

    def get_servers(self):
        return self.data.get("servers", [])

    def get_server(self, name):
        for server in self.get_servers():
            if server["name"] == name:
                return server

        return None
