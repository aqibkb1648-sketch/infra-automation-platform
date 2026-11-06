import json
import tempfile
import unittest
from pathlib import Path

from reporting.json_report import JSONReporter


class TestJSONReporter(unittest.TestCase):

    def test_generate_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            reporter = JSONReporter(output_dir=temp_dir)

            results = [
                {
                    "name": "server1",
                    "role": "server",
                    "checks": {}
                }
            ]

            report_path = reporter.generate(results)

            self.assertTrue(Path(report_path).is_file())

            with open(report_path, encoding="utf-8") as file:
                report = json.load(file)

            self.assertEqual(report["total_nodes"], 1)
            self.assertEqual(
                report["results"][0]["name"],
                "server1"
            )
            self.assertIn("generated_at", report)


if __name__ == "__main__":
    unittest.main()
