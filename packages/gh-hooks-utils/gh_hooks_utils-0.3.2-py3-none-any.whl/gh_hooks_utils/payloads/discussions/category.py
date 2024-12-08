from pydantic import BaseModel


class Category(BaseModel):
    id: int
    created_at: str
    description: str
    emoji: str
    is_answerable: bool
    name: str
    node_id: str | None = None
    repository_id: int
    slug: str
    updated_at: str
