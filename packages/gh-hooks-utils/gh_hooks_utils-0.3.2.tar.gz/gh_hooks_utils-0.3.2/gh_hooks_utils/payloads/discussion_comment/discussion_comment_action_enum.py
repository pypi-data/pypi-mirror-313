from enum import Enum, unique


@unique
class DiscussionCommentActionEnum(str, Enum):
    CREATED = "created"
    DELETED = "deleted"
    EDITED = "edited"
