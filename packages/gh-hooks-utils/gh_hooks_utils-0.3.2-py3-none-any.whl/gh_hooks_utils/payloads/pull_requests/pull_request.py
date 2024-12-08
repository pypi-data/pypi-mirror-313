from pydantic import BaseModel, Field

from ..author_association_enum import AuthorAssociationEnum
from ..label import Label
from ..user import User
from .auto_merge import AutoMerge
from .commit_ref import CommitRef
from .link import Link
from .milestone import Milestone
from .pull_request_state_enum import PullRequestStateEnum
from .team import Team


class PullRequest(BaseModel):
    id: int
    number: int
    url: str
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    state: PullRequestStateEnum
    locked: bool
    title: str
    user: User
    body: str | None = None
    labels: list[Label]
    milestone: Milestone | None = None
    active_lock_reason: str | None = None
    created_at: str
    updated_at: str | None = None
    closed_at: str | None = None
    merged_at: str | None = None
    merge_commit_sha: str | None = None
    assignee: User | None = None
    assignees: list[User] | None = None
    requested_reviewers: list[User] | None = None
    requested_teams: list[Team] | None = None
    head: CommitRef
    base: CommitRef
    links: Link = Field(..., alias="_links")
    author_association: AuthorAssociationEnum
    auto_merge: AutoMerge | None
    draft: bool | None = None
    merged: bool
    mergeable: bool | None = None
    rebaseable: bool | None = None
    mergeable_state: str
    merged_by: User | None = None
    comments: int
    review_comments: int
    maintainer_can_modify: bool
    commits: int
    additions: int
    deletions: int
    changed_files: int
    allow_auto_merge: bool = False
    allow_update_branch: bool | None = None
    delete_branch_on_merge: bool | None = False
    merge_commit_message: str | None = None
    merge_commit_title: str | None = None
    squash_merge_commit_message: str | None = None
    squash_merge_commit_title: str | None = None
    use_squash_pr_title_as_default: bool | None = None
