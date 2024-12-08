from enum import Enum, unique


@unique
class InstallationActionEnum(str, Enum):
    CREATED = "created"
    """Someone installed a GitHub App on a user or organization account."""

    DELETED = "deleted"
    """Someone uninstalled a GitHub App from their user or organization account."""

    NEW_PERMISSION_ACCEPTED = "new_permission_accepted"
    """Someone granted new permissions to a GitHub App."""

    SUSPEND = "suspend"
    """Someone blocked access by a GitHub App to their user or organization account."""

    UNSUSPEND = "unsuspend"
    "A GitHub App that was blocked from accessing a user or organization account was given access the account again."
