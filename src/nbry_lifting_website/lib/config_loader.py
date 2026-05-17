"""Config loader for TOML files."""

import tomllib
from pathlib import Path
from typing import Any


class ConfigLoader:
    """Loads TOML configuration files from a directory."""

    def __init__(self, config_dir: Path | str):
        """Initialize with config directory path.

        Args:
            config_dir: Path to the configuration directory
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")
        if not self.config_dir.is_dir():
            raise NotADirectoryError(
                f"Config path is not a directory: {self.config_dir}"
            )

    def load(self, filename: str) -> dict[str, Any]:
        """Load a TOML file and return parsed data.

        Args:
            filename: Relative path to TOML file (e.g., "program.toml" or "blocks/accumulation.toml")

        Returns:
            Parsed TOML data as dict

        Raises:
            FileNotFoundError: If the file doesn't exist
            tomllib.TOMLDecodeError: If the file is not valid TOML
        """
        file_path = self.config_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(file_path, "rb") as f:
            return tomllib.load(f)
