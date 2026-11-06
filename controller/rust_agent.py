import json
from pathlib import Path

from controller.executor import Executor


class RustAgent:
    def __init__(self, timeout=10):
        self.executor = Executor(timeout=timeout)
        self.binary = (
            Path(__file__).resolve().parent.parent
            / "rust-agent"
            / "target"
            / "release"
            / "infra-agent"
        )

    def collect(self):
        if not self.binary.is_file():
            return {
                "success": False,
                "metrics": {},
                "error": "Rust agent binary not found. Build it first."
            }

        result = self.executor.run([
            str(self.binary),
            "--json"
        ])

        if not result["success"]:
            return {
                "success": False,
                "metrics": {},
                "error": result["stderr"]
            }

        try:
            metrics = json.loads(result["stdout"])
        except json.JSONDecodeError as error:
            return {
                "success": False,
                "metrics": {},
                "error": str(error)
            }

        return {
            "success": True,
            "metrics": metrics,
            "error": ""
        }
