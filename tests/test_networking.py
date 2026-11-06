
import unittest
from unittest.mock import Mock

from networking.dns import DNSChecker
from networking.connectivity import ConnectivityChecker
from networking.routing import RoutingChecker


class TestNetworking(unittest.TestCase):

    def setUp(self):
        self.executor = Mock()

    def test_dns_success(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "93.184.216.34 STREAM example.com",
            "stderr": ""
        }

        result = DNSChecker(self.executor).check(
            "client1", "example.com"
        )

        self.assertTrue(result["success"])
        self.assertIn(
            "93.184.216.34",
            result["resolved_addresses"][0]
        )

    def test_dns_failure(self):
        self.executor.docker_exec.return_value = {
            "success": False,
            "stdout": "",
            "stderr": "Name or service not known"
        }

        result = DNSChecker(self.executor).check(
            "client1", "invalid.example"
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["resolved_addresses"], [])

    def test_connectivity_success(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "2 packets transmitted, 2 received",
            "stderr": ""
        }

        result = ConnectivityChecker(self.executor).check(
            "client1", "127.0.0.1"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["source"], "client1")

    def test_http_success(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "200",
            "stderr": ""
        }

        result = ConnectivityChecker(self.executor).check_http(
            "client1", "10.10.20.2", 80
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["http_code"], "200")

    def test_http_not_found(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "404",
            "stderr": ""
        }

        result = ConnectivityChecker(self.executor).check_http(
            "client1", "10.10.20.2", 80
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["http_code"], "404")

    def test_http_connection_failure(self):
        self.executor.docker_exec.return_value = {
            "success": False,
            "stdout": "000",
            "stderr": "Connection refused"
        }

        result = ConnectivityChecker(self.executor).check_http(
            "client1", "10.10.20.2", 80
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["http_code"], "000")

    def test_routing_collection(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "default via 172.20.20.1 dev eth0",
            "stderr": ""
        }

        result = RoutingChecker(self.executor).collect("router1")

        self.assertTrue(result["success"])
        self.assertIn("default via", result["routes"][0])


if __name__ == "__main__":
    unittest.main()

