import logging
from pathlib import Path


def setup_logger(log_dir="logs", level="INFO"):
    directory = Path(log_dir)
    directory.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("infra_automation")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        directory / "infra-automation.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
