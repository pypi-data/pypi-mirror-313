import fnmatch
import hashlib
import os
import random
import re
import shutil
import string
from pathlib import Path
from typing import List, Optional, Union
from zipfile import ZipFile

from ..config import AnylearnConfig
from ..interfaces import Mirror
from ..utils import logger
from ..utils.errors import (
    AnyLearnMissingParamException,
    AnyLearnNotSupportedException,
)


def get_mirror_by_name(name: str) -> Mirror:
    mirrors = Mirror.get_list()
    try:
        return next(m for m in mirrors if m.name == name)
    except:
        raise AnyLearnNotSupportedException((
            f"Container for `{name}` is not supported by "
            "the connected backend."
        ))


def make_name_by_path(path: Union[str, Path]) -> str:
    if not path:
        raise AnyLearnMissingParamException("`path` required.")
    path = Path(path)
    basename = path.name
    suffix = hashlib.sha1(str(path).encode('utf-8')).hexdigest()[:8]
    return f"{basename}-{suffix}"


def generate_random_name() -> str:
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 8))


def _check_resource_input(id: Optional[str]=None,
                          dir_path: Optional[Union[str, bytes, os.PathLike]]=None,
                          archive_path: Optional[Union[str, bytes, os.PathLike]]=None):
    if not any([id, dir_path, archive_path]):
        raise AnyLearnMissingParamException((
            "At least one of the parameters "
            "['id', 'dir_path', 'archive_path'] "
            "should be specified."
        ))


def _get_or_create_resource_archive(name,
                                    dir_path: Optional[Union[str, bytes, os.PathLike]]=None,
                                    archive_path: Optional[Union[str, bytes, os.PathLike]]=None):
    logger.info("Packaging resources...")
    if not archive_path or not Path(archive_path).exists():
        archive_path = shutil.make_archive(
            AnylearnConfig.workspace_path / name,
            "zip",
            dir_path
        )
    return archive_path


def _get_archive_checksum(archive_path: Optional[Union[str, bytes, os.PathLike]], buffer_size: int=65536):
    checksum = hashlib.blake2b()
    with open(archive_path, "rb") as f:
        while True:
            chunk = f.read(buffer_size)
            if not chunk:
                break
            checksum.update(chunk)
    return checksum.hexdigest()


def make_algorithm_zip(zip_filename: Optional[Union[os.PathLike, bytes, str]], algorithm_dir_path: Optional[Union[os.PathLike, bytes, str]]) -> Path:
    logger.info("Zipping algorithm files...")
    algorithm_files = get_algorithm_files(algorithm_dir_path)
    zip_path = Path(AnylearnConfig.workspace_path / zip_filename)
    with ZipFile(zip_path, "w") as zip_file:
        for file_path in algorithm_files:
            zip_file.write(file_path)
    return zip_path


def get_algorithm_files(algorithm_dir_path: Optional[Union[os.PathLike, bytes, str]]) -> List[str]:
    algorithm_dir_path = Path(algorithm_dir_path)
    if not algorithm_dir_path.exists():
        raise FileNotFoundError(
            f"Algorithm directory `{algorithm_dir_path}` does not exist."
        )

    gitignore_path = algorithm_dir_path / ".gitignore"
    if gitignore_path.exists():
        pattern = build_re_pattern_from_gitignore(gitignore_path)
    else:
        pattern = None

    algorithm_files = []
    for root, dirs, files in os.walk(algorithm_dir_path):
        if pattern:
            dirs[:] = [d for d in dirs if not re.match(pattern, d)]
            files[:] = [f for f in files if not re.match(pattern, f)]
        algorithm_files.extend([os.path.join(root, f) for f in files])
    return algorithm_files


def build_re_pattern_from_gitignore(gitignore_path: Optional[Union[os.PathLike, bytes, str]]) -> str:
    gitignore_path = Path(gitignore_path)
    if not gitignore_path.exists():
        raise FileNotFoundError(
            f"Gitignore file `{gitignore_path}` does not exist."
        )

    patterns = [".git"] # We ignore .git directory by default
    with gitignore_path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.endswith("/"):
                line = line[:-1]
            patterns.append(line)

    return r"|".join([fnmatch.translate(i) for i in patterns])
