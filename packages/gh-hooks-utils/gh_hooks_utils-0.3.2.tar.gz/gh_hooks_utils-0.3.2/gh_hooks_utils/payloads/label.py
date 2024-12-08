from pydantic import BaseModel


class Label(BaseModel):
    id: int
    node_id: str
    url: str
    name: str
    description: str | None
    color: str
    default: bool
