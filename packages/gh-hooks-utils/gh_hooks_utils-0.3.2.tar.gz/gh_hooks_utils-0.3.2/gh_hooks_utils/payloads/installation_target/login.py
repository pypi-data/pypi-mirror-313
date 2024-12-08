from pydantic import BaseModel, Field


class Login(BaseModel):
    from_login: str = Field(..., alias="from")
