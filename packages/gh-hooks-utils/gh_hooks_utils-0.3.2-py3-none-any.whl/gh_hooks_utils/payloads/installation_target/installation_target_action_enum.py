from enum import Enum, unique


@unique
class InstallationTargetActionEnum(str, Enum):
    RENAMED = "renamed"
