from pydantic import BaseModel, Field


class Account(BaseModel):
    id: int
    archived_at: str | None = None
    avatar_url: str
    created_at: str | None = None
    description: str | None = None
    events_url: str | None = None
    followers: int | None = None
    followers_url: str | None = None
    following: int | None = None
    following_url: str | None = None
    gists_url: str | None = None
    gravatar_id: str | None = None
    has_organization_projects: bool | None = None
    has_repository_projects: bool | None = None
    hooks_url: str | None = None
    html_url: str
    is_verified: bool | None = None
    issues_url: str | None = None
    login: str | None = None
    members_url: str | None = None
    name: str | None = None
    node_id: str
    organizations_url: str | None = None
    public_gists: int | None = None
    public_members_url: str | None = None
    public_repos: int | None = None
    received_events_url: str | None = None
    repos_url: str | None = None
    site_admin: bool | None = None
    slug: str | None = None
    starred_url: str | None = None
    subscriptions_url: str | None = None
    account_type: str | None = Field(None, alias="type")
    updated_at: str | None = None
    url: str | None = None
    website_url: str | None = None
    user_view_type: str | None = None
