from pydantic import BaseModel, Field

from ..account import Account
from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..user import User
from .change import Change
from .installation_target_action_enum import InstallationTargetActionEnum

_ENTERPRISE_DESCRIPTION = """An enterprise on GitHub. Webhook payloads contain
the enterprise property when the webhook is configured on an enterprise account
or an organization that's part of an enterprise account."""

_ORG_DESCRIPTION = """A GitHub organization. Webhook payloads contain the
organization property when the webhook is configured for an organization, or
when the event occurs from activity in a repository owned by an organization."""

_REPO_DESCRIPTION = """The repository on GitHub where the event occurred.
Webhook payloads contain the repository property when the event occurs from
activity in a repository."""

_SENDER_DESCRIPTION = "A GitHub user."


class InstallationTargetEvent(BaseModel):
    """Activity relating to the user or organization account that a GitHub App is installed on.

    Availability for installation:
        *GitHub Apps
    """

    account: Account
    action: InstallationTargetActionEnum
    changes: Change
    enterprise: Enterprise | None = Field(
        None,
        description=_ENTERPRISE_DESCRIPTION,
    )
    installation: Installation | None = None
    organization: Organization | None = Field(
        None, description=_ORG_DESCRIPTION
    )
    repository: Repository | None = Field(None, description=_REPO_DESCRIPTION)
    sender: User = Field(..., description=_SENDER_DESCRIPTION)
    target_type: str
