from pydantic import BaseModel


class Organization(BaseModel):
    id: int
    login: str
    node_id: str | None = None
    url: str | None = None
    description: str | None = None
