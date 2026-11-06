import tempfile
import unittest
from pathlib import Path

import yaml

from controller.inventory import Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "servers.yml"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_config(self, data):
        with self.config_path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(data, file)

    def test_load_servers(self):
        self.write_config({
            "servers": [
                {
                    "name": "server1",
                    "container": "clab-lab01-server1",
                    "role": "server"
                }
            ]
        })

        inventory = Inventory(self.config_path)

        self.assertEqual(len(inventory.get_servers()), 1)
        self.assertEqual(
            inventory.get_servers()[0]["name"],
            "server1"
        )

    def test_get_server(self):
        self.write_config({
            "servers": [
                {
                    "name": "server1",
                    "container": "clab-lab01-server1",
                    "role": "server"
                }
            ]
        })

        inventory = Inventory(self.config_path)

        self.assertIsNotNone(inventory.get_server("server1"))
        self.assertIsNone(inventory.get_server("unknown"))

    def test_duplicate_server_names(self):
        self.write_config({
            "servers": [
                {
                    "name": "server1",
                    "container": "container1",
                    "role": "server"
                },
                {
                    "name": "server1",
                    "container": "container2",
                    "role": "server"
                }
            ]
        })

        with self.assertRaises(ValueError):
            Inventory(self.config_path)


if __name__ == "__main__":
    unittest.main()
