from enum import Enum, unique


@unique
class InstallationRepositoriesActionEnum(str, Enum):
    ADDED = "ADDED"
    """A GitHub App installation was granted access to one or more repositories."""

    REMOVED = "removed"
    """Access to one or more repositories was revoked for a GitHub App installation."""
