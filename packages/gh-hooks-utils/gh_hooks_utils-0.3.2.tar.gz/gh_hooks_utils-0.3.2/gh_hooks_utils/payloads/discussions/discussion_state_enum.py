from enum import Enum, unique


@unique
class DiscussionStateEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    LOCKED = "locked"
    CONVERTING = "converting"
    TRANSFERRING = "transferring"
