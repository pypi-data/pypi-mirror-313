from pydantic import BaseModel


class Permissions(BaseModel):
    admin: bool
    pull: bool
    triage: bool | None = None
    push: bool
    maintain: bool | None = None
