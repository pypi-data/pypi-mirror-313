from pydantic import BaseModel

from ..repository import Repository
from ..user import User


class CommitRef(BaseModel):
    label: str
    ref: str
    repo: Repository
    sha: str
    user: User
