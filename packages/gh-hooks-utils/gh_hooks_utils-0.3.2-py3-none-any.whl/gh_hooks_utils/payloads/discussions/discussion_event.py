from pydantic import BaseModel, Field

from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..user import User
from .answer import Answer
from .discussion import Discussion
from .discussion_action_enum import DiscussionActionEnum


class DiscussionEvent(BaseModel):
    action: DiscussionActionEnum
    answer: Answer
    discussion: Discussion = Field(
        ..., description="A Discussion in a repository."
    )
    enterprise: Enterprise | None = Field(
        None,
        description=(
            "An enterprise on GitHub. Webhook payloads contain the enterprise "
            "property when the webhook is configured on an enterprise account "
            "or an organization that's part of an enterprise account."
        ),
    )
    installation: Installation | None = Field(
        None,
        description=(
            "The GitHub App installation. Webhook payloads contain the "
            "installation property when the event is configured for and sent "
            "to a GitHub App"
        ),
    )
    organization: Organization | None = Field(
        None,
        description=(
            "A GitHub organization. Webhook payloads contain the organization "
            "property when the webhook is configured for an organization, or "
            "when the event occurs from activity in a repository owned by an "
            "organization."
        ),
    )
    repository: Repository | None = Field(
        None,
        description=(
            "The repository on GitHub where the event occurred. Webhook "
            "payloads contain the repository property when the event occurs "
            "from activity in a repository."
        ),
    )
    sender: User = Field(..., description="A GitHub user.")
