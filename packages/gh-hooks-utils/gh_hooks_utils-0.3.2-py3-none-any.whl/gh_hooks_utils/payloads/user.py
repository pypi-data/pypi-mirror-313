from pydantic import BaseModel, Field


class User(BaseModel):

    name: str | None = None
    email: str | None = None
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str | None
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    user_type: str = Field(..., alias="type")
    site_admin: bool
    starred_at: str | None = None
    user_view_type: str
