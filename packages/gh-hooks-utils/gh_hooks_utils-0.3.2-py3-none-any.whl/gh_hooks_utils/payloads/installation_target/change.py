from pydantic import BaseModel

from .login import Login
from .slug import Slug


class Change(BaseModel):
    login: Login | None = None
    slug: Slug | None = None
