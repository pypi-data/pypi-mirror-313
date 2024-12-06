import random
from typing import Optional

from anylearn.interfaces.base import BaseObject
from anylearn.utils.api import (
    url_base,
    patch_with_token,
)
from anylearn.utils.errors import AnyLearnException


TAG_COLOR = [
    { 'text_color': '#F53F3F', 'color': '#FCE7E7' },
    { 'text_color': '#FE8041', 'color': '#FFF3ED' },
    { 'text_color': '#FEB841', 'color': '#FCF7E1' },
    { 'text_color': '#1FC472', 'color': '#E9F9EF' },
    { 'text_color': '#35CBFC', 'color': '#E9F6F9' },
    { 'text_color': '#357FFC', 'color': '#EBF2FF' },
    { 'text_color': '#605AFF', 'color': '#EDEDFF' },
    { 'text_color': '#FFFFFF', 'color': '#F53F3F' },
    { 'text_color': '#FFFFFF', 'color': '#FE8041' },
    { 'text_color': '#FFFFFF', 'color': '#FEB841' },
    { 'text_color': '#FFFFFF', 'color': '#1FC472' },
    { 'text_color': '#FFFFFF', 'color': '#37BBE8' },
    { 'text_color': '#FFFFFF', 'color': '#357FFC' },
    { 'text_color': '#FFFFFF', 'color': '#605AFF' },
]


class TrainTag(BaseObject):
    """
    Anylearn训练任务标签类，仅支持quick_train打标签

    Attributes
    ----------
    id
        训练任务标签的唯一标识符，自动生成，由TTAG+uuid1生成的编码中后28个有效位（小写字母和数字）组成
    name
        标签的名称
    project_id
        所属项目的id
    """

    _fields = {
        # 资源创建/更新请求包体中必须包含且不能为空的字段
        'required': {
            'create': ['name', 'color', 'text_color', 'project_id'],
            'update': ['id', 'name', 'color', 'text_color', 'project_id'],
        },
        # 资源创建/更新请求包体中包含的所有字段
        'payload': {
            'create': ['name', 'color', 'text_color', 'project_id', 'description'],
            'update': ['id', 'name', 'color', 'text_color', 'project_id', 'description'],
        },
    }
    """
    创建/更新对象时：

    - 必须包含且不能为空的字段 :obj:`_fields['required']`
    - 所有字段 :obj:`_fields['payload']`
    """

    def __init__(self,
                 id: Optional[str]=None,
                 name: Optional[str]=None,
                 color: Optional[str]=None,
                 text_color: Optional[str]=None,
                 project_id: Optional[str]=None,
                 description: Optional[str]=None):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.color = color
        self.text_color = text_color
        self.description = description
    
    def _url_create(self):
        return f"{url_base()}/{self._namespace()}/tag"
    
    def _url_update(self):
        return f"{url_base()}/{self._namespace()}/tag"
    
    def _update(self):
        data = self._payload_update()
        res = patch_with_token(self._url_update(), data=data)
        if not res or 'data' not in res:
            raise AnyLearnException("请求未能得到有效响应")
        return self.id == res['data']
    
    def get_list(self):
        pass

    def get_detail(self):
        pass
        
    @staticmethod
    def generate_random_tag_color():
        color_item = TAG_COLOR[random.randint(0, len(TAG_COLOR)-1)]
        return color_item['color'], color_item['text_color']

    def _namespace(self):
        return "train_task"
