"""Exceptions."""

from dataclasses import dataclass


@dataclass
class ExecutableNotFound(Exception):
    """Raise exception when executable not found."""

    name: str
