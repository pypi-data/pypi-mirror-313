import os
from pathlib import Path
from typing import Optional, Union

import requests
from urllib3.util.retry import Retry
from requests import HTTPError
from requests.adapters import HTTPAdapter

from anylearn.sdk.errors import AnylearnError


DEFAULT_ANYLEARN_HOST = "https://anylearn.nelbds.cn"


def get_config_path() -> Path:
    config_dir = Path.home() / ".anylearn"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def get_artifact_download_path() -> Path:
    download_dir = Path.home() / ".anylearn" / "artifacts"
    download_dir.mkdir(parents=True, exist_ok=True)
    return download_dir


def get_tmp_path() -> Path:
    tmp_dir = Path.home() / ".anylearn" / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def ensure_dir(dir_: Optional[Union[os.PathLike, bytes, str]]):
    root_dir = Path(dir_)
    if root_dir.exists() and root_dir.is_file():
        raise AnylearnError(
            f"Path `{str(dir_)}` is expected to be a directory, "
            "a file given"
        )
    root_dir.mkdir(parents=True, exist_ok=True)


def raise_for_status(res: requests.Response):
    http_error_msg = ''
    if isinstance(res.reason, bytes):
        try:
            reason = res.reason.decode('utf-8')
        except UnicodeDecodeError:
            reason = res.reason.decode('iso-8859-1')
    else:
        reason = res.reason
    
    if isinstance(res.content, bytes):
        try:
            content = res.content.decode('utf-8')
        except UnicodeDecodeError:
            content = res.content.decode('iso-8859-1')
    else:
        content = res.content

    if 400 <= res.status_code < 500:
        http_error_msg = u'%s: "%s" for url: %s' % (res.status_code, content, res.url)

    elif 500 <= res.status_code < 600:
        http_error_msg = u'%s: "%s" for url: %s' % (res.status_code, reason, res.url)

    if http_error_msg:
        raise HTTPError(http_error_msg, response=res)


class RequestRetrySession(object):
    def __init__(
        self,
        retries=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE"],
        session=None,
    ):
        self.session = session or requests.session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
