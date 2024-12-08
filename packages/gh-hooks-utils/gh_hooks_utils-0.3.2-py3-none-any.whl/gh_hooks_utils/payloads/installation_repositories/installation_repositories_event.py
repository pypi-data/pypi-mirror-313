from pydantic import BaseModel, Field

from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..repository_selection_enum import RepositorySelectionEnum
from ..user import User
from .installation_repositories_action_enum import (
    InstallationRepositoriesActionEnum,
)

_ENTERPRISE_DESCRIPTION = """An enterprise on GitHub. Webhook payloads contain
the enterprise property when the webhook is configured on an enterprise account
or an organization that's part of an enterprise account."""

_ORG_DESCRIPTION = """A GitHub organization. Webhook payloads contain the
organization property when the webhook is configured for an organization, or
when the event occurs from activity in a repository owned by an organization."""

_REPOS_ADDED_DESCRITPION = """An array of repository objects, which were added
to the installation."""

_REPOS_REMOVED_DESCRIPTION = """An array of repository objects, which were
removed from the installation."""

_REPO_DESCRIPTION = """The repository on GitHub where the event occurred.
Webhook payloads contain the repository property when the event occurs from
activity in a repository."""

_REPO_SELECTION = """Describe whether all repositories have been selected or
there's a selection involved"""

_SENDER_DESCRIPTION = "A GitHub user."


class InstallationRepositoriesEvent(BaseModel):
    """Activity relating to which repositories a GitHub App installation can access.

    All GitHub Apps receive this event by default. You cannot manually subscribe to this event.

    Availability for installation:
        *GitHub Apps
    """

    action: InstallationRepositoriesActionEnum
    enterprise: Enterprise | None = Field(
        None,
        description=_ENTERPRISE_DESCRIPTION,
    )
    installation: Installation | None = None
    organization: Organization | None = Field(
        None, description=_ORG_DESCRIPTION
    )
    repositories_added: list[Repository] = Field(
        ..., description=_REPOS_ADDED_DESCRITPION
    )
    repositories_removed: list[Repository] = Field(
        ..., description=_REPOS_REMOVED_DESCRIPTION
    )
    repository: Repository | None = Field(None, description=_REPO_DESCRIPTION)
    repository_selection: RepositorySelectionEnum = Field(
        ..., description=_REPO_SELECTION
    )
    requester: User | None = None
    sender: User = Field(..., description=_SENDER_DESCRIPTION)
