from semver import VersionInfo

from cyberfusion.YAVB import SemanticVersioningVersion
import semver


def increment_semver_version(
    current_version: VersionInfo, type_: SemanticVersioningVersion
) -> VersionInfo:
    """Increment SemVer version by given type."""
    if type_ == SemanticVersioningVersion.MAJOR:
        return current_version.bump_major()
    elif type_ == SemanticVersioningVersion.MINOR:
        return current_version.bump_minor()

    return current_version.bump_patch()


def convert_string_to_versioninfo(version: str) -> VersionInfo:
    """Convert version represented as string to semver.VersionInfo."""

    # Fix missing patch version (e.g. 1.0; quite common)

    if version.count(".") == 1:
        version += ".0"

    # Fix missing minor + patch version (e.g. 1; less common)

    elif version.count(".") == 0:
        version += ".0.0"

    # Fix excess of parts; just remove the rest (e.g. 1.2.3.4 -> 1.2.3)

    elif version.count(".") > 2:
        version = ".".join(version.split(".")[:3])  # 3 = point, minor, major

    return semver.VersionInfo.parse(version)
