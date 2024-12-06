import subprocess
import os
from abc import ABCMeta, abstractmethod

import tomlkit

from cyberfusion.YAVB.exceptions import EmailNameMissingError


class System(metaclass=ABCMeta):
    """Interface for systems."""

    @abstractmethod
    def __init__(self, directory: str) -> None:  # pragma: no cover
        """Set attributes."""
        self.directory = directory

    @property
    @abstractmethod
    def version(self) -> str:  # pragma: no cover
        """Get current version."""
        pass

    @abstractmethod
    def update(
        self,
        version: str,
        *,
        changelog_entry: str | None = None,
        full_name: str | None = None,
        email_address: str | None = None,
    ) -> None:  # pragma: no cover
        """Update system (version, changelog, etc.)"""
        pass


class Debian(System):
    """System."""

    def __init__(self, directory: str) -> None:
        """Set attributes."""
        self.directory = directory

    @property
    def version(self) -> str:
        """Get current version."""
        return subprocess.check_output(
            ["dpkg-parsechangelog", "-S", "version"], cwd=self.directory, text=True
        ).strip()

    def update(
        self,
        version: str,
        *,
        changelog_entry: str | None = None,
        full_name: str | None = None,
        email_address: str | None = None,
    ) -> None:
        """Update system (version, changelog, etc.)"""

        # Changelog entry must be set for dch to work non-interactively

        if not changelog_entry:
            changelog_entry = ""

            environment = {}
        else:
            if not email_address or not full_name:
                raise EmailNameMissingError

            environment = {"DEBEMAIL": email_address, "DEBFULLNAME": full_name}

        subprocess.check_output(
            [
                "dch",
                "--distribution",
                "unstable",
                "--newversion",
                version,
                changelog_entry,
            ],
            cwd=self.directory,
            env=environment,
            text=True,
        )


class PyProject(System):
    """System."""

    def __init__(self, directory: str) -> None:
        """Set attributes."""
        self.directory = directory

    @property
    def _contents(self) -> dict:
        """Get contents of pyproject.toml."""

        # Parsing and writing pyproject as regular TOML is fine, see:
        # https://discuss.python.org/t/common-parser-for-pyproject-toml/33269/2

        with open(os.path.join(self.directory, "pyproject.toml"), "r") as f:
            data = tomlkit.parse(f.read())

        return data

    @property
    def version(self) -> str:
        """Get current version."""
        return self._contents["project"]["version"]

    def update(
        self,
        version: str,
        *,
        changelog_entry: str | None = None,
        full_name: str | None = None,
        email_address: str | None = None,
    ) -> None:
        """Update system (version, changelog, etc.)"""
        contents = self._contents

        contents["project"]["version"] = version

        with open(os.path.join(self.directory, "pyproject.toml"), "w") as f:
            f.write(tomlkit.dumps(contents))
