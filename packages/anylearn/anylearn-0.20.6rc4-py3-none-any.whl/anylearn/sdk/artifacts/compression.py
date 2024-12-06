from __future__ import annotations

import cgi
import os
from pathlib import Path
from typing import Optional, Union

import requests

from anylearn.sdk.auth import configure_auth
from anylearn.sdk.client import get_with_token, post_with_token
from anylearn.sdk.context import get_base_url
from anylearn.sdk.errors import AnylearnInvalidResponseError
from anylearn.sdk.utils import ensure_dir, get_tmp_path


class Compression:
    def __init__(self, *_, **kwargs):
        self.id = kwargs.pop('id', None)
        self.parent_id = kwargs.pop('parent_id', None)
        self.sub_path = kwargs.pop('subpath', None)
        self.filename = kwargs.pop('filename', None)
        self.state = kwargs.pop('state', None)
        self.creator_id = kwargs.pop('creator_id', None)
        self.created_at = kwargs.pop('created_at', None)

    @classmethod
    def from_id_and_artifact_id(
        cls,
        id_: str,
        artifact_id: str
    ) -> Compression:
        res = get_with_token(
            f"{get_base_url()}/resource/compression",
            params={
                'file_id': artifact_id,
                'compression_id': id_,
            },
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError("Request failed")
        return Compression(**res[0])

    @classmethod
    def create(cls, artifact_id: str, sub_path: Optional[Union[str, bytes, os.PathLike]]) -> Compression:
        res = post_with_token(
            f"{get_base_url()}/resource/compression",
            data={
                'file_id': artifact_id,
                'subpath': sub_path,
            },
        )
        if not res or 'data' not in res:
            raise AnylearnInvalidResponseError("Request failed")
        compression_id = res['data']
        return Compression.from_id_and_artifact_id(
            id_=compression_id,
            artifact_id=artifact_id,
        )

    def ready_to_download(self) -> bool:
        return self.state == CompressionState.FINISHED

    def on_error(self) -> bool:
        return self.state in [
            CompressionState.FAILED,
            CompressionState.INVALID,
        ]

    def reload(self) -> None:
        res = get_with_token(
            f"{get_base_url()}/resource/compression",
            params={
                'file_id': self.parent_id,
                'compression_id': self.id,
            },
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError("Request failed")
        self.__init__(**res[0])

    def download(
        self,
        dest_dir: Optional[Union[str, bytes, os.PathLike]]=None,
    ) -> Path:
        assert self.ready_to_download()

        root_dir = Path(dest_dir or get_tmp_path())
        ensure_dir(root_dir)

        auth = configure_auth()
        headers = {'Authorization': f"Bearer {auth.access_token}"}
        res = requests.get(
            url=f"{get_base_url()}/resource/download",
            headers=headers,
            params={
                'file_id': self.parent_id,
                'compression_id': self.id,
                'token': auth.access_token,
            },
        )
        res.raise_for_status()

        content_header = res.headers.get('Content-Disposition')
        if content_header:
            _, params = cgi.parse_header(content_header)
            filename = params['filename']
            with open(root_dir / filename, "wb") as f:
                f.write(res.content)
            return root_dir / filename
        else:
            raise AnylearnInvalidResponseError(f"Failed to download {self.id}")


class CompressionState:
    CREATED = 0
    IN_PROGRESS = 1
    FINISHED = 2
    FAILED = -1
    INVALID = -2
