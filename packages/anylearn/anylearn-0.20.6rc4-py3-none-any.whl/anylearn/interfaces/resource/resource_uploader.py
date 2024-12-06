from abc import ABC, abstractmethod

import requests
from tqdm import tqdm

from anylearn.config import AnylearnConfig
from anylearn.utils import logger
from anylearn.utils.api import url_base


class ResourceUploader(ABC):
    """
    资源上传工具接口
    """

    @abstractmethod
    def run(self, resource_id: str, chunks: list):
        """
        执行资源上传,自定义资源上传需实现此方法

        Parameters
        ----------
        resource_id
            资源ID
        chunks
            被切割后的文件内容列表
        """
        raise NotImplementedError


class SyncResourceUploader(ResourceUploader):
    def run(self, resource_id: str, chunks: list):
        for i, chunk in enumerate(tqdm(chunks)):
            url = f"{url_base()}/resource/upload"
            headers = {'Authorization': f"Bearer {AnylearnConfig.token}"}
            files = {'file': chunk}
            data = {'file_id': resource_id, 'chunk': str(i)}
            res = requests.post(url, headers=headers, files=files, data=data)
            res.raise_for_status()
