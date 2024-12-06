import os
from pathlib import Path
from typing import Optional, Dict, List


__DEFAULT_HOST__ = "https://anylearn.nelbds.cn"


ARTIFACT_IDS = 'ANYLEARN_ARTIFACT_IDS'
TASK_ID = 'ANYLEARN_TASK_ID'
HOST = 'ANYLEARN_HOST'
TOKEN = 'ANYLEARN_AUTH_TOKEN'
REFRESH_TOKEN = 'ANYLEARN_AUTH_REFRESH_TOKEN'
ANYLEARN_ANYBOARD_IOTDB_HOST = 'ANYLEARN_ANYBOARD_IOTDB_HOST'


def get_artifact_ids() -> List[str]:
    ids_str = os.environ.get(ARTIFACT_IDS, None)
    if not ids_str:
        return []
    return ids_str.replace(" ", "").split(",")


def get_artifact_paths() -> List[Path]:
    ids = get_artifact_ids()
    paths = {}
    for id_ in ids:
        p = os.environ.get(id_, None)
        if not p:
            continue
        p = Path(p)
        if not p.exists():
            continue
        paths[id_] = p
    return paths


def get_task_id(default: Optional[str]=None):
    return os.environ.get(TASK_ID, default)


def inside_train_task():
    return ANYLEARN_ANYBOARD_IOTDB_HOST in os.environ


def get_auth() -> Dict[str, Optional[str]]:
    return {
        'host': os.environ.get(HOST, __DEFAULT_HOST__),
        'token': os.environ.get(TOKEN, None),
        'refresh_token': os.environ.get(REFRESH_TOKEN, None),
    }


def set_token(token: str) -> None:
    os.environ[TOKEN] = token
