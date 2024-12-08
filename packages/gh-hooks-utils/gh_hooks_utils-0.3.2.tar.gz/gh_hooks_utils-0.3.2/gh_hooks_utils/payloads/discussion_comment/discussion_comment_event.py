from pydantic import BaseModel

from ..discussions import Discussion
from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..user import User
from .comment import Comment
from .discussion_comment_action_enum import DiscussionCommentActionEnum


class DiscussionCommentEvent(BaseModel):
    """Occurs when there is activity relating to a comment on a discussion.

    For activity relating to a discussion as opposed to comments on a
    discussion, use the discussion event.

    To subscribe to this event, a GitHub App must have at least read-level
    access for the "Discussions" repository permission.

    Availability for discussion_comment:
        * Repositories
        * Organizations
        * GitHub Apps
    """

    action: DiscussionCommentActionEnum
    comment: Comment
    discussion: Discussion
    enterprise: Enterprise | None = None
    installation: Installation | None = None
    organization: Organization | None = None
    repository: Repository
    sender: User
