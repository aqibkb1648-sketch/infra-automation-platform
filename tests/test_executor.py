import subprocess
import unittest
from unittest.mock import patch

from controller.executor import Executor


class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.executor = Executor(timeout=5)

    @patch("controller.executor.subprocess.run")
    def test_successful_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["echo", "hello"],
            returncode=0,
            stdout="hello\n",
            stderr=""
        )

        result = self.executor.run(["echo", "hello"])

        self.assertTrue(result["success"])
        self.assertEqual(result["stdout"], "hello")

    @patch("controller.executor.subprocess.run")
    def test_failed_command(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["false"],
            returncode=1,
            stdout="",
            stderr="failed"
        )

        result = self.executor.run(["false"])

        self.assertFalse(result["success"])
        self.assertEqual(result["returncode"], 1)

    @patch(
        "controller.executor.subprocess.run",
        side_effect=subprocess.TimeoutExpired("sleep", 5)
    )
    def test_command_timeout(self, mock_run):
        result = self.executor.run(["sleep", "10"])

        self.assertFalse(result["success"])
        self.assertEqual(result["returncode"], -1)


if __name__ == "__main__":
    unittest.main()
