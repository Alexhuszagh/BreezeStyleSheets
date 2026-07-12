"""Project paths."""

from pathlib import Path


def package_dir() -> "Path":
    """Get the directory containing the current package."""
    return Path(__file__).parent.parent


def project_dir() -> "Path":
    """Get the directory containing the current project."""
    return package_dir().parent
