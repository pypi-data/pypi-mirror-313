from pydantic import BaseModel

from ..author_association_enum import AuthorAssociationEnum
from ..user import User
from .reaction import Reaction


class Answer(BaseModel):
    author_association: AuthorAssociationEnum
    body: str
    child_comment_count: int
    created_at: str
    discussion_id: int
    html_url: str
    id: int
    node_id: str
    parent_id: int | None = None
    reactions: Reaction | None = None
    repository_url: str
    updated_at: str
    user: User | None = None
