from enum import Enum, unique


@unique
class DiscussionActionEnum(str, Enum):
    ANSWERED = "answered"
    CATEGORY_CHANGED = "category_changed"
    CLOSED = "closed"
    CREATED = "created"
    DELETED = "deleted"
    EDITED = "edited"
    LABELED = "labeled"
    LOCKED = "locked"
    PINNED = "pinned"
    REOPENED = "reopened"
    TRANSFERRED = "transferred"
    UNANSWERED = "unanswered"
    UNLABELED = "unlabeled"
    UNLOCKED = "unlocked"
    UNPINED = "unpined"
