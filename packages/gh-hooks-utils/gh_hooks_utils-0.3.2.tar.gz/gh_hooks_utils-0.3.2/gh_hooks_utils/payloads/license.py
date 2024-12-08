from pydantic import BaseModel


class License(BaseModel):
    key: str
    name: str
    url: str | None
    spdx_id: str | None
    node_id: str
    html_url: str | None = None
