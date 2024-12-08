from pydantic import BaseModel

from ..events import EventsEnum
from .account import Account
from .repository_selection_enum import RepositorySelectionEnum
from .user import User


class Installation(BaseModel):
    id: int
    node_id: str | None = None
    client_id: str | None = None
    account: Account | None = None
    repository_selection: RepositorySelectionEnum | None = None
    access_tokens_url: str | None = None
    repositories_url: str | None = None
    html_url: str | None = None
    app_id: int | None = None
    app_slug: str | None = None
    target_id: int | None = None
    target_type: str | None = None
    permissions: dict[str, str] | None = None
    events: list[EventsEnum] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    single_file_name: str | None = None
    has_multiple_single_files: bool | None = None
    suspended_by: User | None = None
    suspended_at: str | None = None
