from enum import StrEnum


class System(StrEnum):
    """Systems."""

    DEBIAN = "debian"
    PYPROJECT = "pyproject"


class SemanticVersioningVersion(StrEnum):
    """Semantic versioning versions."""

    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"
