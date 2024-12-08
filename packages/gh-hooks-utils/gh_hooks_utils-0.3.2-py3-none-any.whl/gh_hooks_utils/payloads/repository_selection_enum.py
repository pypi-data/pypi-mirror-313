from enum import Enum, unique


@unique
class RepositorySelectionEnum(str, Enum):
    """Describe whether all repositories have been selected or there's a selection involved"""

    ALL = "all"
    SELECTED = "selected"
