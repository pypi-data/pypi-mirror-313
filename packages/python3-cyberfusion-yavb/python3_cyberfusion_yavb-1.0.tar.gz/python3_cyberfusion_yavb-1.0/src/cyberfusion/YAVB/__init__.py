from typing import Optional

import typer
from cyberfusion.YAVB.enums import System, SemanticVersioningVersion
from cyberfusion.YAVB.systems import Debian, PyProject
from cyberfusion.YAVB.utilities import (
    increment_semver_version,
    convert_string_to_versioninfo,
)
import glob

app = typer.Typer()


@app.command()  # type: ignore[misc]
def main(
    systems_names: list[System] = typer.Option(
        ...,
        "--system",
        help="What to bump version in. 'Debian' must run on Debian (if needed, use the Docker container as described in the README).",
    ),
    bump_type: SemanticVersioningVersion = typer.Option(
        ...,
        "--bump",
        help="How to increment SemVer version. If the current version deviates from the SemVer standard, it is coerced as much as possible (e.g. adding missing parts, removing excess parts, etc.)",
    ),
    directories: list[str] = typer.Option(
        ...,
        "--directory",
        help="Directories containing software projects. Globbing is allowed (e.g. wildcards).",
    ),
    changelog_entry: Optional[str] = typer.Option(
        None,
        "--changelog",
        help="Entry to add to new version's changelog (ignored for systems that don't support changelogs)",
    ),
    email_address: Optional[str] = typer.Option(
        None,
        "--email",
        help="Email address (may be required when --changelog is set, depending on system)",
    ),
    full_name: Optional[str] = typer.Option(
        None,
        "--name",
        help="Full name (may be required when --changelog is set, depending on system)",
    ),
) -> None:
    """Bump version of project in given systems."""

    # Expand directories to allow wildcards. We must do this in-program rather
    # than relying on the shell, as Docker containers don't use bash.

    globbed_directories = []

    for directory in directories:
        globbed_directories.extend(glob.glob(directory))

    for globbed_directory in globbed_directories:
        for system_name in systems_names:
            if system_name == System.DEBIAN:
                system = Debian(globbed_directory)
            else:
                system = PyProject(globbed_directory)

            current_version = convert_string_to_versioninfo(system.version)

            version = str(increment_semver_version(current_version, bump_type))

            system.update(
                version,
                changelog_entry=changelog_entry,
                full_name=full_name,
                email_address=email_address,
            )
