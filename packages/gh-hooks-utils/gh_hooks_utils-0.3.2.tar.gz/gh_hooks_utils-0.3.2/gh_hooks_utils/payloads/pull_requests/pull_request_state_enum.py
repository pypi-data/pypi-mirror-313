from enum import Enum, unique


@unique
class PullRequestStateEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
