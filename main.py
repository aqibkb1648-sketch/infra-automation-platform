
import argparse
import sys

from controller.config import load_settings
from controller.orchestrator import Orchestrator
from reporting.json_report import JSONReporter
from reporting.logger import setup_logger


def main():
    settings = load_settings()

    application = settings["application"]
    runtime = settings["runtime"]
    reporting = settings["reporting"]

    parser = argparse.ArgumentParser(
        description=application["name"]
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f'{application["name"]} {application["version"]}'
    )

    parser.parse_args()

    logger = setup_logger(
        log_dir=reporting["log_dir"],
        level=runtime["log_level"]
    )

    try:
        logger.info("Starting infrastructure checks")

        orchestrator = Orchestrator()
        results = orchestrator.run()

        reporter = JSONReporter(
            output_dir=reporting["output_dir"]
        )

        report_path = reporter.generate(results)

        containers = [
            node for node in results
            if node["container"] is not None
        ]

        running_containers = sum(
            1 for node in containers
            if node["checks"].get(
                "container", {}
            ).get("stdout") == "true"
        )

        host = next(
            (node for node in results if node["role"] == "host"),
            None
        )

        rust_success = (
            host is not None
            and host["checks"]["rust_agent"]["success"]
        )

        logger.info("Checks completed")
        logger.info("Containers: %s", len(containers))
        logger.info(
            "Running containers: %s/%s",
            running_containers,
            len(containers)
        )
        logger.info(
            "Rust agent: %s",
            "PASS" if rust_success else "FAIL"
        )
        logger.info("JSON report: %s", report_path)

        print(f"\nReport saved: {report_path}")
        print(
            f"Running containers: "
            f"{running_containers}/{len(containers)}"
        )
        print(
            f"Rust agent: {'PASS' if rust_success else 'FAIL'}"
        )

    except Exception:
        logger.exception("Infrastructure checks failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

