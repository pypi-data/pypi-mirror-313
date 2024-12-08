from pydantic import BaseModel

from ..enterprise import Enterprise
from ..installation import Installation
from ..organization import Organization
from ..repository import Repository
from ..user import User
from .installation_action_enum import InstallationActionEnum


class InstallationEvent(BaseModel):
    """Occurs when there is activity relating to a GitHub App installation.

    All GitHub Apps receive this event by default. You cannot manually
    subscribe to this event.

    Availability for installation:
        *GitHub Apps
    """

    action: InstallationActionEnum
    enterprise: Enterprise | None = None
    installation: Installation | None = None
    organization: Organization | None = None
    repository: Repository | None = None
    repositories: list[Repository] | None = None
    requester: User | None = None
    sender: User
