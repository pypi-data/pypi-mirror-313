from enum import Enum, unique


@unique
class MilestoneStateEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
