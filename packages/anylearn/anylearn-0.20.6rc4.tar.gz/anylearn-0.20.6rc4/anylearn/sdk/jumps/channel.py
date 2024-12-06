from __future__ import annotations

import hashlib
import os
import time
import uuid
from pathlib import Path
from typing import Optional, Tuple, Union

from rich import print

from anylearn.sdk.errors import (
    AnylearnInvalidResponseError,
    AnylearnArtifactTooLargeError,
)
from anylearn.sdk.client import (
    get_with_token,
    patch_with_token,
    post_with_token,
)
from anylearn.sdk.console import console_error, console_warning
from anylearn.sdk.context import get_base_url
from anylearn.sdk.sshkey import SSHKey, generate_ssh_key_pair
from anylearn.sdk.utils import get_config_path


def get_jumps_dir_path() -> Path:
    jumps_dir = get_config_path().parent / "jumps"
    jumps_dir.mkdir(parents=True, exist_ok=True)
    return jumps_dir


JUMPS_SSH_KEY_NAME = "jumpsk"
JUMPS_ARTIFACT_SIZE_SOFT_LIMIT = 20 * 1024 * 1024 * 1024 # 20GB
JUMPS_ARTIFACT_SIZE_HARD_LIMIT = 50 * 1024 * 1024 * 1024 # 50GB


def get_jumps_ssh_key_paths() -> Tuple[Path, Path]:
    root = get_jumps_dir_path()
    private_key_path = root / JUMPS_SSH_KEY_NAME
    public_key_path = private_key_path.with_suffix(".pub")
    return private_key_path, public_key_path


def load_jumps_ssh_key() -> Optional[SSHKey]:
    private_key_path, public_key_path = get_jumps_ssh_key_paths()
    if not private_key_path.exists() or not public_key_path.exists():
        return None
    return SSHKey(
        public_key=public_key_path.read_bytes(),
        private_key=private_key_path.read_bytes(),
    )


def dump_jumps_ssh_key(ssh_key: SSHKey) -> None:
    private_key_path, public_key_path = get_jumps_ssh_key_paths()
    private_key_path.write_bytes(ssh_key.private_key)
    private_key_path.chmod(0o600)
    public_key_path.write_bytes(ssh_key.public_key)


class JumpsChannel:

    def __init__(self, *_, **kwargs) -> None:
        self.id = kwargs.get('id', None)
        self.client_code = kwargs.get('client_code', None)
        self.ip = kwargs.get('ip', None)
        self.port = kwargs.get('port', None)
        self.username = kwargs.get('username', None)
        self.path = kwargs.get('path', None)

    @classmethod
    def from_artifact_id(self, artifact_id: str) -> JumpsChannel:
        url = f"{get_base_url()}/jumps/channels/asset/{artifact_id}"
        res = get_with_token(url)
        if not res or not isinstance(res, dict):
            raise AnylearnInvalidResponseError(
                "Failed to get channel on jump server."
            )
        return JumpsChannel(**res)

    @classmethod
    def create(
        cls,
        artifact_id: str,
        artifact_local_path: Optional[Union[str, bytes, os.PathLike]],
    ) -> JumpsChannel:
        # Prepare SSH key
        ssh_key = load_jumps_ssh_key()
        if ssh_key is None:
            ssh_key = generate_ssh_key_pair()
            dump_jumps_ssh_key(ssh_key)
        # Total number of files and total size
        artifact_local_path = Path(artifact_local_path)
        if not artifact_local_path.exists():
            raise FileNotFoundError(
                f"Local artifact path {artifact_local_path} not found"
            )
        # TODO: avoid blocking the main thread since artifact may be huge
        size, nfiles = cls.get_local_artifact_stat(artifact_local_path)
        # Client conformity identifier
        client_identifier = cls.get_client_identifier(artifact_local_path)
        # Create channel
        res = post_with_token(
            f"{get_base_url()}/jumps/channels",
            data={
                'asset_id': artifact_id,
                'ssh_public_key': ssh_key.public_key.decode(),
                'total_size': size,
                'nb_files': nfiles,
                'client_code': client_identifier,
            }
        )
        if not res or not isinstance(res, dict):
            raise AnylearnInvalidResponseError(
                "Failed to create channel on jump server."
            )
        return JumpsChannel(**res)

    @classmethod
    def get_local_artifact_stat(
        cls,
        artifact_local_path: Optional[Union[str, bytes, os.PathLike]],
    ) -> Tuple[int, int]:
        artifact_local_path = Path(artifact_local_path)
        if not artifact_local_path.exists():
            raise FileNotFoundError(
                f"Local artifact path {artifact_local_path} not found"
            )
        if artifact_local_path.is_file():
            size, nfiles = artifact_local_path.stat().st_size, 1
            cls.check_artifact_size(size)
        elif not artifact_local_path.is_dir():
            raise FileNotFoundError(
                f"Local artifact path {artifact_local_path} is "
                "neither a file nor a directory"
            )
        size = 0
        nfiles = 0
        for f in artifact_local_path.glob("**/*"):
            if f.is_file():
                size += f.stat().st_size
                nfiles += 1
                cls.check_artifact_size(size)
        return size, nfiles

    @classmethod
    def check_artifact_size(cls, size: int) -> None:
        if size > JUMPS_ARTIFACT_SIZE_HARD_LIMIT:
            console_error(
                "artifact size exceeds Anylearn's size limit of "
                "[bold]50GB[/bold] "
                "for upload via jump server."
            )
            raise AnylearnArtifactTooLargeError(
                "Artifact size must be less than 50GB"
            )
        elif size > JUMPS_ARTIFACT_SIZE_SOFT_LIMIT:
            console_warning(
                "artifact size is larger than "
                "Anylearn's recommended maximum size of "
                "[bold]20GB[/bold] "
                "for upload via jump server."
            )

    @classmethod
    def get_client_identifier(cls, artifact_local_path: Optional[Union[str, bytes, os.PathLike]]) -> str:
        artifact_local_path = Path(artifact_local_path)
        mac_address = hex(uuid.getnode())
        code = f"{str(artifact_local_path)}@{mac_address}"
        h = hashlib.blake2s()
        h.update(code.encode())
        return h.hexdigest()

    def transform(self) -> bool:
        # Create transformation
        url = f"{get_base_url()}/jumps/channels/{self.id}/trans"
        res = post_with_token(url)
        if not res or not isinstance(res, dict):
            raise AnylearnInvalidResponseError(
                "Failed to create transformation on jump server."
            )
        # Poll transformation status
        status = self.get_transformation_status()
        while not status or status == 'running':
            status = self.get_transformation_status()
            time.sleep(1)
        return status == "succeeded"

    def get_transformation_status(self) -> Optional[str]:
        url = f"{get_base_url()}/jumps/channels/{self.id}/trans"
        res = get_with_token(url)
        if not res or not isinstance(res, dict):
            raise AnylearnInvalidResponseError(
                "Failed to get transformation status."
            )
        return res.get('status')

    def finish(self):
        patch_with_token(f"{get_base_url()}/jumps/channels/{self.id}/finishing")

    def __repr__(self) -> str:
        return (
            "JumpsChannel("
            f"id={self.id}, "
            f"ip={self.ip}, "
            f"port={self.port}, "
            f"username={self.username}, "
            f"path={self.path}"
            ")"
        )
