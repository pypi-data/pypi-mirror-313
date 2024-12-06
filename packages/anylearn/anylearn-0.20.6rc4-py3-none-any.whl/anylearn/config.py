from pathlib import Path
import requests
import shutil

from anylearn.sdk.auth import (
    authenticate_by_access_token,
    authenticate_by_password,
    authenticate_by_refresh_token,
)
from anylearn.sdk.context import init as init_context
from anylearn.utils import logger
from anylearn.utils.errors import InvalidArguments, AnyLearnAuthException


class AnylearnConfig(object):
    """
    Anylearn SDK配置类，
    包含Anylearn后端引擎的连接配置和SDK的本地存储配置。
    """

    cluster_address = None
    """Anylearn后端引擎集群网关地址"""

    username = None
    """Anylearn后端引擎账户用户名"""

    user_id = None
    """Anylearn后端引擎账户ID"""

    password = None
    """Anylearn后端引擎账户密码"""

    token = None
    """Anylearn后端引擎API令牌"""

    refresh_token = None
    """Anylearn后端引擎API令牌刷新令牌"""

    workspace_path = Path().home() / ".anylearn"
    """SDK本地存储工作区路径"""

    git_ready = False

    @classmethod
    def init(cls, cluster_address=None, username=None, password=None,
             token=None, workspace=None, disable_git=False):
        # Cluster Auth
        cls.init_cluster(cluster_address, username, password, token)
        # Local workspace
        cls.init_workspace(workspace)
        # Detect git
        cls.git_ready = not disable_git and cls.check_git()

    @classmethod
    def init_cluster_by_token(
        cls,
        host: str,
        token: str,
        refresh_token: str,
    ) -> None:
        init_context(host=host)
        if host.endswith("/"):
            host = host[:-1]
        cls.cluster_address = host
        cls.token = token
        cls.refresh_token = refresh_token
        cls.cluster_login_by_token()

    @classmethod
    def init_cluster(cls, cluster_address=None, username=None, password=None,
                     token=None):
        if not all([
            cluster_address,
            isinstance(cluster_address, str),
            any([username and password, token]),
        ]):
            raise InvalidArguments('无有效登录配置')
        init_context(host=cluster_address)
        if cluster_address.endswith('/'):
            cluster_address = cluster_address[:-1]
        cls.cluster_address = cluster_address
        cls.username = username
        cls.password = password
        cls.token = token
        if token is None:
            cls.cluster_login()
    
    @classmethod
    def cluster_login(cls):
        if not cls.username or not cls.password:
            raise InvalidArguments(
                "Cannot login without username and password"
            )
        auth = authenticate_by_password(
            username=cls.username,
            password=cls.password,
            host=cls.cluster_address,
        )
        if auth:
            cls.token = auth.access_token
            cls.refresh_token = auth.refresh_token
            cls.user_id = auth.user_id
        else:
            raise AnyLearnAuthException()

    @classmethod
    def cluster_login_by_token(cls) -> None:
        if not cls.token:
            raise InvalidArguments("Cannot login with empty token")
        auth = authenticate_by_access_token(
            username=cls.username,
            access_token=cls.token,
            host=cls.cluster_address,
        )
        if auth:
            cls.user_id = auth.user_id
        elif cls.refresh_token:
            cls.cluster_relogin_by_token()
        else:
            raise AnyLearnAuthException()

    @classmethod
    def cluster_relogin_by_token(cls) -> None:
        if not cls.refresh_token:
            raise InvalidArguments(f"Cannot relogin with empty refresh token")
        auth = authenticate_by_refresh_token(
            username=cls.username,
            refresh_token=cls.refresh_token,
            host=cls.cluster_address,
        )
        if auth:
            cls.token = auth.access_token
            cls.user_id = auth.user_id
        else:
            raise AnyLearnAuthException()

    @classmethod
    def init_workspace(cls, workspace=None):
        cls.workspace_path = Path(workspace) if workspace \
                                             else cls.workspace_path
        # Remove if workspace path points to a file
        if cls.workspace_path.is_file():
            cls.workspace_path.unlink()
        # Ensure workspace folder exists
        cls.workspace_path.mkdir(exist_ok=True)

    @classmethod
    def clear_workspace(cls):
        shutil.rmtree(cls.workspace_path)

    @classmethod
    def check_git(cls):
        try:
            from git import Repo
            return True
        except:
            logger.warning("Git executable not found.")
            cls.git_ready = False
            return False


def init_sdk(cluster_address, username, password, disable_git=False):
    """
    初始化SDK与后端连接的接口。
    调用本接口并传入后端地址、用户名和密码，
    SDK将自动以相应账户进行登录并获取后端API令牌。

    Parameters
    ----------
    cluster_address : :obj:`str`
        Anylearn后端引擎集群网关地址。
    username : :obj:`str`
        Anylearn后端引擎账户用户名。
    password : :obj:`str`
        Anylearn后端引擎账户密码。
    """
    AnylearnConfig.init(
        cluster_address=cluster_address,
        username=username,
        password=password,
        disable_git=disable_git,
    )


def init_sdk_incontainer(cluster_address):
    """
    初始化无鉴权信息的SDK与后端连接的接口。
    调用本接口仅需传入后端地址，
    无需账户信息。
    以此方式初始化的SDK将无法调用需要鉴权信息的接口，
    仅可调用无需API令牌的公共接口。

    此接口的使用场景多为任务执行容器内与后端建立通信，
    不建议用户使用。

    Parameters
    ----------
    cluster_address : :obj:`str`
        Anylearn后端引擎集群网关地址。
    """
    AnylearnConfig.init(
        cluster_address=cluster_address,
        token="INCONTAINER"
    )


def print_config():
    print(AnylearnConfig.cluster_address)
