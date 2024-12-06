from __future__ import annotations

from anylearn.sdk.artifacts.artifact import Artifact
from anylearn.sdk.client import get_with_token
from anylearn.sdk.context import get_base_url
from anylearn.sdk.errors import AnylearnInvalidResponseError


class FileArtifact(Artifact):
    @classmethod
    def from_id(cls, id_: str) -> FileArtifact:
        res = get_with_token(
            f"{get_base_url()}/file/query",
            params={'id': id_},
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError("Request failed")
        return FileArtifact(**res[0])
