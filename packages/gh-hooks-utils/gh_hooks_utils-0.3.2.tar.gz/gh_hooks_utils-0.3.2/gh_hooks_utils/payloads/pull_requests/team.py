from pydantic import BaseModel


class Team(BaseModel):
    id: int
    node_id: str
    url: str
    members_url: str
    name: str
    description: str | None
    permission: str
    privacy: str | None = None
    notification_setting: str | None = None
    html_url: str
    repositories_url: str
    slug: str
    ldap_dn: str | None = None
