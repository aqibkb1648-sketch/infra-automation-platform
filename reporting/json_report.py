import json
from datetime import datetime, timezone
from pathlib import Path


class JSONReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, results):
        report = {
            "project": "infra-automation-platform",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_nodes": len(results),
            "results": results
        }

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = self.output_dir / f"report-{timestamp}.json"

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return str(output_file)
