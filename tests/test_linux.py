import unittest
from unittest.mock import Mock

from linux.services import ServiceChecker
from linux.storage import StorageChecker
from linux.system_info import SystemInfo


class TestLinuxModules(unittest.TestCase):

    def setUp(self):
        self.executor = Mock()

    def test_service_success(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "200",
            "stderr": ""
        }

        result = ServiceChecker(self.executor).check(
            "server1", "nginx", 80
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["output"], "200")

    def test_storage_success(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "Filesystem Size Used Available",
            "stderr": ""
        }

        result = StorageChecker(self.executor).collect("server1")

        self.assertTrue(result["success"])
        self.assertIn("Filesystem", result["usage"][0])

    def test_system_info_success(self):
        self.executor.docker_exec.return_value = {
            "success": True,
            "stdout": "test-output",
            "stderr": ""
        }

        result = SystemInfo(self.executor).collect("server1")

        self.assertTrue(result["success"])
        self.assertIn("hostname", result["details"])
        self.assertIn("memory", result["details"])


if __name__ == "__main__":
    unittest.main()
