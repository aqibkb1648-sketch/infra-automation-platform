
from controller.config import load_settings
from controller.inventory import Inventory
from controller.executor import Executor
from controller.rust_agent import RustAgent

from networking.dns import DNSChecker
from networking.connectivity import ConnectivityChecker
from networking.routing import RoutingChecker

from linux.services import ServiceChecker
from linux.storage import StorageChecker
from linux.system_info import SystemInfo


class Orchestrator:


    def __init__(self):
        self.settings = load_settings()

        timeout = self.settings["runtime"]["command_timeout"]
        network = self.settings["network"]

        self.inventory = Inventory()
        self.executor = Executor(timeout=timeout)
        self.rust_agent = RustAgent()

        self.dns = DNSChecker(
            self.executor,
            timeout=network["dns_timeout"]
        )

        self.connectivity = ConnectivityChecker(
            self.executor,
            ping_count=network["ping_count"]
        )

        self.routing = RoutingChecker(self.executor)
        self.services = ServiceChecker(self.executor)
        self.storage = StorageChecker(self.executor)
        self.system_info = SystemInfo(self.executor)

    def run(self):
        results = []
        servers = self.inventory.get_servers()

        for server in servers:
            container = server["container"]

            node_result = {
                "name": server["name"],
                "container": container,
                "role": server["role"],
                "checks": {}
            }

            node_result["checks"]["container"] = self.executor.run([
                "docker",
                "inspect",
                "--format",
                "{{.State.Running}}",
                container
            ])

            if (
                not node_result["checks"]["container"]["success"]
                or node_result["checks"]["container"]["stdout"] != "true"
            ):
                results.append(node_result)
                continue

            node_result["checks"]["system"] = (
                self.system_info.collect(container)
            )

            node_result["checks"]["storage"] = (
                self.storage.collect(container)
            )

            node_result["checks"]["routing"] = (
                self.routing.collect(container)
            )

            node_result["checks"]["dns"] = (
                self.dns.check(container, "example.com")
            )

            node_result["checks"]["connectivity"] = (
                self.connectivity.check(container, "127.0.0.1")
            )

            node_result["checks"]["services"] = [
                self.services.check(
                    container,
                    service["name"],
                    service["port"],
                    service.get("protocol", "tcp")
                )
                for service in server.get("services", [])
            ]

            results.append(node_result)

        # Cross-network connectivity test:
        # client1 -> router1 -> server1

        client = next(
            (server for server in servers if server["name"] == "client1"),
            None
        )

        if client:
            client_container = client["container"]

            network_path = {
                "name": "client1-to-server1",
                "container": client_container,
                "role": "network_path",
                "checks": {
                    "ping": self.connectivity.check(
                        client_container,
                        "10.10.20.2"
                    ),
                    "http": self.connectivity.check_http(
                        client_container,
                        "10.10.20.2",
                        80
                    )
                }
            }

            results.append(network_path)

        results.append({
            "name": "wsl-host",
            "container": None,
            "role": "host",
            "checks": {
                "rust_agent": self.rust_agent.collect()
            }
        })

        return results

