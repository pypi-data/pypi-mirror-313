from __future__ import annotations

from typing import Optional

from requests import HTTPError

from anylearn.sdk.artifacts.artifact import Artifact
from anylearn.sdk.auth import configure_auth
from anylearn.sdk.client import get_with_token, post_with_token
from anylearn.sdk.context import get_base_url
from anylearn.sdk.errors import (
    AnylearnArtifactDuplicationError,
    AnylearnInvalidResponseError,
)


class DatasetArtifact(Artifact):

    @classmethod
    def from_full_name(cls, full_name: str) -> DatasetArtifact:
        res = get_with_token(
            f"{get_base_url()}/dataset/query",
            params={'fullname': full_name},
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError(
                f"Failed to get dataset {full_name} from server."
            )
        return DatasetArtifact(**res[0])

    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str] = None,
        public: bool = False,
    ) -> DatasetArtifact:
        auth = configure_auth()
        # Check if dataset already exists
        full_name = f"{auth.username}/{name}"
        try:
            get_with_token(
                f"{get_base_url()}/dataset/query",
                params={'fullname': full_name},
            )
            raise AnylearnArtifactDuplicationError(
                f"Dataset {full_name} already exists."
            )
        except HTTPError as e:
            if e.response.status_code != 404:
                raise
        # Create dataset
        res = post_with_token(
            f"{get_base_url()}/dataset/add",
            data={
                'name': name,
                'description': description,
                'public': 1 if public else 0,
            },
        )
        if not res or not isinstance(res, dict) or not res.get('data'):
            raise AnylearnInvalidResponseError(
                f"Failed to create dataset {full_name} on server."
            )
        return cls.from_full_name(full_name)
