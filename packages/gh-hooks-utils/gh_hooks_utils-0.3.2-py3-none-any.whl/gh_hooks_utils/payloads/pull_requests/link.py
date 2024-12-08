from pydantic import BaseModel, Field

from .hypermedia_link import HypermediaLink


class Link(BaseModel):
    comments: HypermediaLink
    commits: HypermediaLink
    statuses: HypermediaLink
    html: HypermediaLink
    issue: HypermediaLink
    review_comments: HypermediaLink
    review_comment: HypermediaLink
    link_self: HypermediaLink = Field(..., alias="self")
