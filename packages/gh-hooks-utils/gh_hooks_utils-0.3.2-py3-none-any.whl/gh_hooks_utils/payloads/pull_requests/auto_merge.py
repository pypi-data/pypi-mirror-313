from pydantic import BaseModel

from ..user import User
from .merge_method_enum import MergeMethodEnum


class AutoMerge(BaseModel):
    enabled_by: User
    merge_method: MergeMethodEnum
    commit_title: str
    commit_message: str
