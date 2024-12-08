from pydantic import BaseModel


class Enterprise(BaseModel):
    id: int
    slug: str
    name: str
    node_id: str
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
