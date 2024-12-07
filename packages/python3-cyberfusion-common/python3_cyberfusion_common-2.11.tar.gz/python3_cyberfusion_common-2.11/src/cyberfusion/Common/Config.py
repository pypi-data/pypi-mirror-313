"""Helper for handling config files."""

import configparser
import os
from typing import Optional

from cached_property import cached_property


class CyberfusionConfig:
    """Abstract ConfigParser implementation for use in scripts."""

    def __init__(
        self,
        path: Optional[str] = None,
    ) -> None:
        """Set attributes."""
        self._path = path

    @property
    def path(self) -> str:
        """Set config file path."""
        if not self._path:
            self._path = os.path.join(
                os.path.sep, "etc", "cyberfusion", "cyberfusion.cfg"
            )

        return self._path

    @cached_property
    def config(self) -> configparser.ConfigParser:
        """Read config."""
        config = configparser.ConfigParser()

        with open(self.path, "r") as f:
            config.read_file(f)

        return config

    def get(self, section: str, key: str) -> str:
        """Retrieve config option."""
        return self.config.get(section, key)
