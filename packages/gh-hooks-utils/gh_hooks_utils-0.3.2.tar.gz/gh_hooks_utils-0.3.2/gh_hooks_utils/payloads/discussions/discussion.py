from pydantic import BaseModel

from ..author_association_enum import AuthorAssociationEnum
from ..label import Label
from ..user import User
from .category import Category
from .discussion_state_enum import DiscussionStateEnum
from .discussion_state_reason_enum import DiscussionStateReasonEnum
from .reaction import Reaction


class Discussion(BaseModel):
    id: int
    active_lock_reason: str | None = None
    answer_chosen_at: str | None = None
    answer_chosen_by: User | None = None
    answer_html_url: str | None = None
    author_association: AuthorAssociationEnum
    body: str
    category: Category
    comments: int
    created_at: str
    html_url: str
    locked: bool
    node_id: str
    number: int
    reactions: list[Reaction] | None = None
    repository_url: str
    state: DiscussionStateEnum
    state_reason: DiscussionStateReasonEnum | None = None
    timeline_url: str | None = None
    title: str
    updated_at: str | None = None
    user: User | None = None
    labels: list[Label] | None = None
