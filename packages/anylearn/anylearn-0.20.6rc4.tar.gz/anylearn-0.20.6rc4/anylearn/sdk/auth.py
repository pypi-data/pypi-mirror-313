from base64 import b64encode, b64decode
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import typer
from requests.exceptions import HTTPError
from rich import print

try:
    from ruamel.yaml import YAML
except ImportError:
    from ruamel_yaml import YAML

from anylearn.sdk.console import (
    console_error,
    console_success,
)
from anylearn.sdk.context import get_context
from anylearn.sdk.utils import (
    DEFAULT_ANYLEARN_HOST,
    get_config_path,
    raise_for_status,
    RequestRetrySession,
)


@dataclass
class Auth:
    host: str
    username: str
    access_token: str
    refresh_token: Optional[str] = None
    user_id: Optional[str] = None


__auth__: Auth = None


def configure_auth(force: bool = False) -> Optional[Auth]:
    global __auth__
    ctx = get_context()
    if not __auth__ or force:
        __auth__ = authenticate(host=ctx.host)
    return __auth__


def authenticate(host: str = DEFAULT_ANYLEARN_HOST) -> Optional[Auth]:
    """
    Try to ensure that user is authenticated to a given Anylearn host:
    1. Try to load auths from local config file.
    2. If no auths found or forced to relogin, prompt user to login.
    3. If auths found, try to login by tokens.
    4. If login bu token failed, prompt user to login.
    5. If login succeeded, dump auths to local config file.
    """
    if not host:
        host = DEFAULT_ANYLEARN_HOST
    host = host.rstrip("/")
    auths = _load()
    if not isinstance(auths, dict) or host not in auths:
        auth = None
    else:
        auth = auths[host]
        auth = _login_by_tokens(
            host=host,
            username=auth.username,
            access_token=auth.access_token,
            refresh_token=auth.refresh_token,
        )
    if not auth:
        auth = _prompt_login(host)
    _dump(auth)
    return auth


def authenticate_by_password(
    username: str,
    password: str,
    host: str = DEFAULT_ANYLEARN_HOST,
) -> Optional[Auth]:
    if not host:
        host = DEFAULT_ANYLEARN_HOST
    host = host.rstrip("/")
    auth = _login_by_password(
        host=host,
        username=username,
        password=password,
    )
    _dump(auth)
    return auth


def authenticate_by_access_token(
    username: str,
    access_token: str,
    host: str = DEFAULT_ANYLEARN_HOST,
) -> Optional[Auth]:
    if not host:
        host = DEFAULT_ANYLEARN_HOST
    host = host.rstrip("/")
    auth = _login_by_access_token(
        host=host,
        username=username,
        access_token=access_token,
    )
    _dump(auth)
    return auth


def authenticate_by_refresh_token(
    username: str,
    refresh_token: str,
    host: str = DEFAULT_ANYLEARN_HOST,
) -> Optional[Auth]:
    if not host:
        host = DEFAULT_ANYLEARN_HOST
    host = host.rstrip("/")
    auth = _relogin_by_refresh_token(
        host=host,
        username=username,
        refresh_token=refresh_token,
    )
    _dump(auth)
    return auth


def disauthenticate(host: str = DEFAULT_ANYLEARN_HOST) -> None:
    """
    Remove auths of a given Anylearn host from local config file.
    """
    if not host:
        host = DEFAULT_ANYLEARN_HOST
    host = host.rstrip("/")
    _del(host)


def _load() -> Optional[Dict[str, Auth]]:
    config_path = get_config_path()
    if not config_path.exists():
        return None
    yaml = YAML()
    config = yaml.load(config_path)
    if not config or 'auths' not in config:
        return None
    auths = {}
    for host, auth in config['auths'].items():
        if not host or not isinstance(auth, dict):
            continue
        if not all([
            auth.get('username'),
            auth.get('access_token'),
            auth.get('refresh_token'),
            auth.get('user_id'),
        ]):
            continue
        auths[host] = Auth(
            host=host,
            username=auth.get('username'),
            access_token=b64decode(auth.get('access_token').encode()).decode(),
            refresh_token=b64decode(auth.get('refresh_token').encode()).decode(),
            user_id=auth.get('user_id'),
        )
    return auths


def _dump(auths: Union[Dict[str, Auth], Auth]) -> None:
    if auths is None:
        return
    if isinstance(auths, Auth):
        auths = {auths.host: auths}
    config_path = get_config_path()
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch()
    yaml = YAML()
    config = yaml.load(config_path)
    if not config:
        config = {}
    if 'auths' not in config:
        config['auths'] = {}
    for _, auth in auths.items():
        if not all([
            auth.host,
            auth.username,
            auth.access_token,
            auth.refresh_token,
            auth.user_id,
        ]):
            continue
        config['auths'][auth.host] = {
            'username': auth.username,
            'access_token': b64encode(auth.access_token.encode()).decode(),
            'refresh_token': b64encode(auth.refresh_token.encode()).decode(),
            'user_id': auth.user_id,
        }
    yaml.dump(config, config_path)


def _del(hosts: Union[List[str], str]) -> None:
    config_path = get_config_path()
    if not config_path.exists():
        return None
    yaml = YAML()
    config = yaml.load(config_path)
    if not config or 'auths' not in config:
        return None
    if isinstance(hosts, str):
        hosts = [hosts]
    for host in hosts:
        if host in config['auths']:
            del config['auths'][host]
    yaml.dump(config, config_path)


def _login_by_tokens(
    host: str,
    username: str,
    access_token: str,
    refresh_token: str,
) -> Optional[Auth]:
    try:
        auth = _login_by_access_token(
            host=host,
            username=username,
            access_token=access_token,
        )
        auth.refresh_token = refresh_token
        return auth
    except HTTPError as e:
        if e.response.status_code != 401:
            return None
        return _relogin_by_refresh_token(
            host=host,
            username=username,
            refresh_token=refresh_token,
        )


def _login_by_access_token(
    host: str,
    username: str,
    access_token: str,
) -> Optional[Auth]:
    with RequestRetrySession() as sess:
        res = sess.get(
            f"{host}/api/user/me",
            headers={'Authorization': f"Bearer {access_token}"},
        )
        raise_for_status(res)
        res.encoding = "utf-8"
        data = res.json()
        if (
            'id' not in data or
            'username' not in data or
            data['username'] != username
        ):
            raise ValueError
        return Auth(
            host=host,
            username=username,
            access_token=access_token,
            user_id=data['id'],
        )


def _relogin_by_refresh_token(
    host: str,
    username: str,
    refresh_token: str,
) -> Optional[Auth]:
    with RequestRetrySession() as sess:
        try:
            res = sess.get(
                f"{host}/api/user/refresh_token",
                headers={'Authorization': f"Bearer {refresh_token}"},
            )
            raise_for_status(res)
            res.encoding = "utf-8"
            data = res.json()
            if 'token' not in data:
                raise ValueError
            auth = _login_by_access_token(
                host=host,
                username=username,
                access_token=data['token'],
            )
            auth.refresh_token = refresh_token
            return auth
        except:
            return None


def _prompt_login(host: str) -> Optional[Auth]:
    print(f"Login to {host} :")
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    auth = _login_by_password(
        host=host,
        username=username,
        password=password,
    )
    if auth:
        console_success(f"Login to {host} as {auth.username} succeeded.")
    else:
        console_error("Login failed. Please check your username and password.")
    return auth


def _login_by_password(
    host: str,
    username: str,
    password: str,
) -> Optional[Auth]:
    with RequestRetrySession() as sess:
        try:
            res = sess.post(
                f"{host}/api/user/login",
                data={
                    'username': username,
                    'password': password,
                },
            )
            raise_for_status(res)
            res.encoding = "utf-8"
            data = res.json()
            if not all([
                data.get('id'),
                data.get('token'),
                data.get('refresh_token'),
                data.get('username'),
            ]):
                raise ValueError
            return Auth(
                host=host,
                username=data['username'],
                access_token=data['token'],
                refresh_token=data['refresh_token'],
                user_id=data['id'],
            )
        except:
            return None
