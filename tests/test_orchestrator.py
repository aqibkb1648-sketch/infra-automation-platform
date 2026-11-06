import unittest
from unittest.mock import patch

from controller.orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):

    @patch("controller.orchestrator.RustAgent")
    @patch("controller.orchestrator.Inventory")
    def test_orchestrator_initialization(
        self,
        mock_inventory,
        mock_rust_agent
    ):
        mock_inventory.return_value.get_servers.return_value = []

        mock_rust_agent.return_value.collect.return_value = {
            "success": True,
            "metrics": {},
            "error": ""
        }

        orchestrator = Orchestrator()
        results = orchestrator.run()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "wsl-host")
        self.assertEqual(results[0]["role"], "host")
        self.assertTrue(
            results[0]["checks"]["rust_agent"]["success"]
        )


if __name__ == "__main__":
    unittest.main()
