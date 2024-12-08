from pydantic import BaseModel

from ..author_association_enum import AuthorAssociationEnum
from ..discussions import Reaction
from ..user import User


class Comment(BaseModel):
    id: int
    author_association: AuthorAssociationEnum
    body: str
    child_comment_count: int
    created_at: str
    discussion_id: int
    html_url: str
    node_id: str
    parent_id: int | None = None
    reactions: list[Reaction] | None = None
    repository_url: str
    updated_at: str
    user: User | None = None
