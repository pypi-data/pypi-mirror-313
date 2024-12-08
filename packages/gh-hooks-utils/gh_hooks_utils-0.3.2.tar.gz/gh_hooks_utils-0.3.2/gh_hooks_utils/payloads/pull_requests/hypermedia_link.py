from pydantic import BaseModel


class HypermediaLink(BaseModel):
    href: str
