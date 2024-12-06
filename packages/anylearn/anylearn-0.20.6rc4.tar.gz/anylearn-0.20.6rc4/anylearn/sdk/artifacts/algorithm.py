from __future__ import annotations

from anylearn.sdk.artifacts.artifact import Artifact
from anylearn.sdk.client import get_with_token
from anylearn.sdk.context import get_base_url
from anylearn.sdk.errors import AnylearnInvalidResponseError


class AlgorithmArtifact(Artifact):
    @classmethod
    def from_full_name(cls, full_name: str) -> AlgorithmArtifact:
        res = get_with_token(
            f"{get_base_url()}/algorithm/query",
            params={'fullname': full_name},
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError("Request failed")
        return AlgorithmArtifact(**res[0])
