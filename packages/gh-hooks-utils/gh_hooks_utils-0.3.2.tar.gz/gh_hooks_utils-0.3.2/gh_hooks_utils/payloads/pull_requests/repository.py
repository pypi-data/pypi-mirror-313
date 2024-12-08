from pydantic import BaseModel

from ..license import License
from ..permission import Permissions
from ..user import User


class Repository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    license: License | None = None
    forks: int
    permissions: Permissions | None = None
    owner: User
    private: bool
    html_url: str
    description: str | None
    fork: bool
    url: str
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    git_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    ssh_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    clone_url: str
    mirror_url: str | None
    hooks_url: str
    svn_url: str
    homepage: str | None
    language: str | None
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: bool | None = None
    topics: list[str] | None = None
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    has_discussions: bool | None = None
    archived: bool
    disabled: bool
    visibility: str
    pushed_at: str | None
    created_at: str | None
    updated_at: str | None
    allow_rebase_merge: bool | None = None
    temp_clone_token: str | None = None
    allow_squash_merge: bool | None = None
    allow_auto_merge: bool | None = None
    delete_branch_on_merge: bool | None = None
    allow_update_branch: bool | None = None
    use_squash_pr_title_as_default: bool | None = None
    squash_merge_commit_title: str | None = None
    squash_merge_commit_message: str | None = None
    merge_commit_title: str | None = None
    merge_commit_message: str | None = None
    allow_merge_commit: bool | None = None
    allow_forking: bool | None = None
    open_issues: int
    watchers: int
    master_branch: str | None = None
    starred_at: str | None = None
    anonymous_access_enabled: bool | None = None
