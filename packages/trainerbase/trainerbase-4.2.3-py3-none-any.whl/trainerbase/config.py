from pathlib import Path
from tomllib import load as load_toml
from typing import Final


CONFIG_FILE: Final[Path] = Path("./trainerbase.toml")


with CONFIG_FILE.resolve().open("rb") as trainerbase_toml:
    trainerbase_config = load_toml(trainerbase_toml)


config_warnings = []


try:
    process_config = trainerbase_config["process"]
except KeyError:
    # Legacy section support
    process_config = trainerbase_config["pymem"]
    process_config["names"] = process_config["process_names"]
    del trainerbase_config["pymem"]

    config_warnings.append(
        "Deprecated config! Use [process] section with field `name` instead of [pymem] with `process_names`"
    )


logging_config = trainerbase_config.get("logging")
