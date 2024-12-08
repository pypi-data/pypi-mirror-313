from pydantic import BaseModel, Field


class Slug(BaseModel):
    from_slug: str = Field(..., alias="from")
