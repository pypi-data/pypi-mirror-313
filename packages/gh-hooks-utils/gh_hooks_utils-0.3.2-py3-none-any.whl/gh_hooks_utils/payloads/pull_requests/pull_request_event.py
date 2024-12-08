from pydantic import BaseModel

from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..user import User
from .pull_request import PullRequest
from .pull_request_action_enum import PullRequestActionEnum


class PullRequestEvent(BaseModel):
    action: PullRequestActionEnum
    enterprise: Enterprise | None = None
    installation: Installation | None = None
    number: int
    organization: Organization | None = None
    pull_request: PullRequest
    repository: Repository
    sender: User

    def is_closed(self) -> bool:
        return (
            self.pull_request is not None
            and self.pull_request.closed_at is not None
        )

    def is_merged(self) -> bool:
        return (
            self.pull_request is not None and self.pull_request.merged is True
        )

    def merged_by(self) -> User | None:
        return self.pull_request.merged_by

    def opened_by(self) -> User:
        return self.pull_request.user
