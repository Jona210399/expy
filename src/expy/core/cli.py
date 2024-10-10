from argparse import ArgumentParser
from pathlib import Path


def parse_config_path(default: Path | None = None) -> Path:
    """If a default config path is provided a script can be run without the config argument."""
    parser = ArgumentParser()
    kwargs = {
        "type": Path,
        "required": not bool(default),
        "help": "Path to the config file",
    }
    if default:
        kwargs["default"] = default

    parser.add_argument(
        "--config",
        **kwargs,
    )
    args = parser.parse_args()
    return args.config
