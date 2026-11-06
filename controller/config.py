
import yaml
from pathlib import Path


def load_settings(config_path=None):
    if config_path is None:
        config_path = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "settings.yml"
        )

    config_path = Path(config_path)

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Settings file not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        settings = yaml.safe_load(file)

    if not isinstance(settings, dict):
        raise ValueError("Invalid settings configuration")

    required_sections = [
        "application",
        "runtime",
        "network",
        "reporting"
    ]

    for section in required_sections:
        if section not in settings:
            raise ValueError(
                f"Missing settings section: {section}"
            )

    return settings

