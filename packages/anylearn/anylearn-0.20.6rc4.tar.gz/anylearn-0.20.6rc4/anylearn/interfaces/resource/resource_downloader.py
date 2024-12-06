import os
from abc import ABC, abstractmethod
import cgi
import time
from typing import Optional, Union

import requests

from anylearn.config import AnylearnConfig
from anylearn.utils.errors import AnyLearnException
from anylearn.utils.api import get_with_token, post_with_token, url_base


class ResourceDownloader(ABC):
    """
    资源下载接口
    """
    @abstractmethod
    def run(self,
            resource_id: str,
            polling: Union[float, int],
            save_path: Optional[Union[str, bytes, os.PathLike]]=None,
           ):
        """
        执行资源下载,自定义资源上传需实现此方法

        Parameters
        ----------
        resource_id
            资源ID
        save_path
            保存路径
        """
        raise NotImplementedError


class SyncResourceDownloader(ResourceDownloader):
    """
    资源同步下载工具类
    """

    def run(self,
            resource_id: str,
            save_path: Optional[Union[str, bytes, os.PathLike]],
            polling: Union[float, int]=5,
           ):

        compress_res = _compress_file(resource_id=resource_id)
        print(f"Resource compress {compress_res}")

        compress_state_res = _compress_complete(resource_id=resource_id, compression_id=compress_res['data'])
        print(f"Resource compress state {compress_state_res}")

        while not compress_state_res[0]['state'] == 2:
            time.sleep(polling)
            compress_state_res = _compress_complete(resource_id=resource_id, compression_id=compress_res['data'])
            print(f"Resource compress state {compress_state_res}")

        headers = {'Authorization': f"Bearer {AnylearnConfig.token}"}

        res = requests.get(url=f"{url_base()}/resource/download",
                           headers=headers,
                           params={
                               'file_id': resource_id,
                               'compression_id': compress_res['data'],
                               'token': AnylearnConfig.token,
                           })
        res.raise_for_status()

        content_header = res.headers.get('Content-Disposition')
        if content_header:
            _, params = cgi.parse_header(content_header)
            fileName = params['filename']
            with open(f"{save_path}/{fileName}", 'wb') as f:
                f.write(res.content)
            return fileName
        else:
            return "文件下载失败"


def _compress_file(resource_id: str):
    res = post_with_token(f"{url_base()}/resource/compression",
                          data={'file_id': resource_id})
    if not res or 'data' not in res:
        raise AnyLearnException("请求未能得到有效响应")
    return res
    
def _compress_complete(resource_id: str, compression_id: str):
    res = get_with_token(f"{url_base()}/resource/compression",
                         params={
                             'file_id': resource_id,
                             'compression_id': compression_id,
                             })
    if not res or not isinstance(res, list):
        raise AnyLearnException("请求未能得到有效响应")
    return res
