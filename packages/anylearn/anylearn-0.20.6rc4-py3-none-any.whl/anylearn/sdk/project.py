from __future__ import annotations

from anylearn.sdk.client import get_with_token
from anylearn.sdk.context import get_base_url
from anylearn.sdk.errors import AnylearnInvalidResponseError


class Project:
    """
    AnyLearn训练项目类

    Attributes
    ----------
    id
        项目的唯一标识符，自动生成，由PROJ+uuid1生成的编码中后28个有效位（小写字母和数字）组成
    name
        项目名称（非空 长度1~50）
    description
        项目描述（可为空 长度最大255）
    created_at
        创建时间
    updated_at
        更新时间
    creator_id
        创建者的ID
    creator_username
    """

    def __init__(self, *_, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.created_at = kwargs.get('create_time', None)
        self.updated_at = kwargs.get('update_time', None)
        self.creator_id = kwargs.get('creator_id', None)
        self.creator_username = kwargs.get('creator_username', None)

    @classmethod
    def from_full_name(cls, full_name: str) -> Project:
        res = get_with_token(
            f"{get_base_url()}/project/query",
            params={'fullname': full_name},
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError("Request failed")
        return Project(**res[0])
    