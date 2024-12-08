from pydantic import BaseModel, Field


class Reaction(BaseModel):
    plus_one: int = Field(..., alias="+1")
    minus_one: int = Field(..., alias="-1")
    confused: int
    eyes: int
    heart: int
    hooray: int
    laugh: int
    rocket: int
    total_count: int
    url: str
