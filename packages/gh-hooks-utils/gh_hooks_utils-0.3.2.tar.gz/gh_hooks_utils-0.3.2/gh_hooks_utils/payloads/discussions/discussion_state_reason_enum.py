from enum import Enum, unique


@unique
class DiscussionStateReasonEnum(str, Enum):
    RESOLVED = "resolved"
    OUTDATED = "outdated"
    DUPLICATE = "duplicate"
    REOPENED = "reopened"
    NULL = "null"
