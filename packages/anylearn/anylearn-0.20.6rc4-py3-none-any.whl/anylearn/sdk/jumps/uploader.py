import os
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional, Union

import paramiko
from rich import print

from anylearn.sdk.errors import AnylearnError
from anylearn.sdk.jumps.channel import (
    JumpsChannel,
    get_jumps_ssh_key_paths,
)


class JumpsUploader:

    def __init__(
        self,
        channel: JumpsChannel,
        local_path: Optional[Union[os.PathLike, bytes, str]],
        compress: bool = True,
    ) -> None:
        self.channel = channel
        self.local_path = Path(local_path)
        if not self.local_path.exists():
            raise AnylearnError(
                f"Local path {self.local_path} does not exist"
            )
        if not self.local_path.is_file() and not self.local_path.is_dir():
            raise AnylearnError(
                f"Local path {self.local_path} is "
                "neither a file nor a directory"
            )
        self.compress = compress
        self._check_channel()
        self.ssh_private_key_path = get_jumps_ssh_key_paths()[0]

    def _check_channel(self):
        if self.channel is None:
            raise AnylearnError(
                "Channel must not be None"
            )
        if any([
            self.channel.id is None,
            self.channel.ip is None,
            self.channel.port is None,
            self.channel.username is None,
            self.channel.path is None,
        ]):
            raise AnylearnError(
                f"Channel is not properly configured: {self.channel}"
            )

    def rsync_available(self):
        try:
            subprocess.check_output(["rsync", "--version"])
            return True
        except:
            return False

    def compression_effective(self):
        # TODO: automatically detect whether compression is effective
        return True

    def upload(self):
        if self.rsync_available():
            return self._upload_by_rsync()
        else:
            with self._open_ssh() as ssh:
                with ssh.open_sftp() as sftp:
                    return self._upload_by_sftp(sftp)

    def _upload_by_rsync(self) -> int:
        if not self.rsync_available():
            raise AnylearnError(
                "Cannot upload by rsync since rsync is not available"
            )
        rsync_options = "-avP"
        if self.compress and self.compression_effective():
            rsync_options += "z"
        ssh_command = (
            "ssh"
            f" -p {self.channel.port}"
            f" -i {self.ssh_private_key_path}"
        )
        rsync_source = (
            f"{str(self.local_path)}/"
            if self.local_path.is_dir()
            else f"{str(self.local_path)}"
        )
        rsync_dest = (
            f"{self.channel.username}@{self.channel.ip}"
            ":"
            f"{self.channel.path}"
        )
        rsync_command = (
            "rsync"
            f" {rsync_options}"
            f" -e \"{ssh_command}\""
            f" {rsync_source}"
            f" {rsync_dest}"
        )
        proc = subprocess.run(rsync_command, shell=True, check=True)
        return proc.returncode

    def _open_ssh(self) -> paramiko.SSHClient:
        self._check_channel()
        compress = self.compress and self.compression_effective()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=self.channel.ip,
            port=self.channel.port,
            username=self.channel.username,
            key_filename=str(self.ssh_private_key_path),
            compress=compress,
        )
        return ssh

    def _upload_by_sftp(self, sftp: paramiko.SFTPClient) -> int:
        if self.local_path.is_file():
            return self._upload_file_by_sftp(sftp)
        elif self.local_path.is_dir():
            return self._upload_dir_by_sftp(sftp)
        else:
            raise AnylearnError(
                f"Local path {self.local_path} is "
                "neither a file nor a directory"
            )

    def _upload_file_by_sftp(self, sftp: paramiko.SFTPClient) -> int:
        remote_f = Path(self.channel.path) / self.local_path.name
        sftp.put(str(self.local_path), str(remote_f))
        # Preserve file metadata (access time and modification time)
        stat = self.local_path.stat()
        sftp.utime(str(remote_f), (stat.st_atime, stat.st_mtime))
        return 0

    def _upload_dir_by_sftp(self, sftp: paramiko.SFTPClient) -> int:
        # Progress counter
        transfered_size = 0
        transfered_nb_files = 0
        # Traverse local path
        for root, dirs, files in os.walk(
            str(self.local_path),
            topdown=True,
            followlinks=False,
        ):
            local_current_path = Path(root)
            local_relative_path = local_current_path.relative_to(self.local_path)
            remote_current_path = Path(self.channel.path) / local_relative_path
            # Create sub-directories
            for d in dirs:
                sftp.mkdir(str(remote_current_path / d))
            # Transfer files
            for f in files:
                local_f = local_current_path / f
                remote_f = remote_current_path / f
                sftp.put(str(local_f), str(remote_f))
                # Preserve file metadata (access time and modification time)
                stat = local_f.stat()
                sftp.utime(str(remote_f), (stat.st_atime, stat.st_mtime))
                # Counter
                transfered_size += stat.st_size
                transfered_nb_files += 1
                # TODO: display progress with total counts
                print(f"Uploaded {local_f}")
                print(f"  Transfered {transfered_nb_files} files, {transfered_size} bytes")
        return 0
