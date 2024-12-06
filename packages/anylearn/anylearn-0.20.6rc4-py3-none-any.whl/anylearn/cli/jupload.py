import os
from pathlib import Path
from typing import Optional, Tuple, Union

import typer
from requests import HTTPError
from rich import print
from typing_extensions import Annotated, Literal

from anylearn.cli._utils import HostOption
from anylearn.sdk.artifacts.artifact import Artifact, ArtifactState
from anylearn.sdk.artifacts.dataset import DatasetArtifact
from anylearn.sdk.artifacts.model import ModelArtifact
from anylearn.sdk.auth import authenticate
from anylearn.sdk.console import (
    console_error,
    console_success,
    console_warning,
)
from anylearn.sdk.context import init
from anylearn.sdk.errors import (
    AnylearnArtifactDuplicationError,
    AnylearnArtifactTooLargeError,
    AnylearnInvalidResponseError,
)
from anylearn.sdk.jumps.channel import JumpsChannel
from anylearn.sdk.jumps.uploader import JumpsUploader


app = typer.Typer()


@app.command()
def dataset(
    name: Annotated[str, typer.Argument(
        help="The name of the dataset to create.",
    )],
    path: Annotated[Path, typer.Argument(
        help="The local path (file or directory) of the dataset to upload.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    )],
    compress: Annotated[bool, typer.Option(
        help="Compress data during transfer (ex. rsync -z).",
    )] = True,
    host: str = HostOption,
):
    _jupload_artifact(
        artifact_type="dataset",
        name=name,
        path=path,
        compress=compress,
        host=host,
    )


@app.command()
def model(
    name: Annotated[str, typer.Argument(
        help="The name of the model to create.",
    )],
    path: Annotated[Path, typer.Argument(
        help="The local path (file or directory) of the model to upload.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    )],
    compress: Annotated[bool, typer.Option(
        help="Compress data during transfer (ex. rsync -z).",
    )] = True,
    host: str = HostOption,
):
    _jupload_artifact(
        artifact_type="model",
        name=name,
        path=path,
        compress=compress,
        host=host,
    )


def _jupload_artifact(
    artifact_type: Literal["dataset", "model"],
    name: str,
    path: Optional[Union[os.PathLike, bytes, str]],
    compress: bool,
    host: str,
) -> None:
    init(host)
    if not authenticate(host):
        raise typer.Abort()
    artifact, resume = _get_or_create_artifact(
        artifact_type=artifact_type,
        name=name,
    )
    _upload_via_jumps_channel(
        artifact_id=artifact.id,
        path=path,
        compress=compress,
        resume=resume,
    )
    console_success("Upload OK")


def _get_or_create_artifact(
    artifact_type: Literal["dataset", "model"],
    name: str,
) -> Tuple[Artifact, bool]:
    if artifact_type == "dataset":
        return _get_or_create_dataset(name)
    elif artifact_type == "model":
        return _get_or_create_model(name)


def _get_or_create_dataset(name: str) -> Tuple[DatasetArtifact, bool]:
    try:
        dataset = DatasetArtifact.from_full_name(name)
        if dataset.state != ArtifactState.CREATED:
            console_error(
                f"Dataset {name} "
                "is being uploaded via Web UI or "
                "is already fully uploaded."
            )
            raise typer.Abort()
        console_warning(f"Dataset {name} already exists in your namespace.")
        resume = typer.confirm("Do you want to resume previous upload?")
        if not resume:
            typer.confirm("Do you want to restart the upload?", abort=True)
        return dataset, resume
    except HTTPError:
        return _create_dataset(name), False


def _create_dataset(name: str) -> DatasetArtifact:
    try:
        print(f"Creating dataset {name}...")
        return DatasetArtifact.create(name=name)
    except AnylearnArtifactDuplicationError:
        console_error(f"Dataset {name} already exists in your namespace.")
        raise typer.Abort()
    except AnylearnInvalidResponseError:
        console_error(f"Failed to create dataset {name}.")
        raise typer.Abort()
    except Exception as e:
        console_error(f"An error occurred during dataset creation: {e}")
        raise typer.Abort()


def _get_or_create_model(name: str) -> Tuple[ModelArtifact, bool]:
    try:
        model = ModelArtifact.from_full_name(name)
        if model.state != ArtifactState.CREATED:
            console_error(
                f"Model {name} "
                "is being uploaded via Web UI or "
                "is already fully uploaded."
            )
            raise typer.Abort()
        console_warning(f"Model {name} already exists in your namespace.")
        resume = typer.confirm("Do you want to resume previous upload?")
        if not resume:
            typer.confirm("Do you want to restart the upload?", abort=True)
        return model, resume
    except HTTPError:
        return _create_model(name), False


def _create_model(name: str) -> ModelArtifact:
    try:
        print(f"Creating model {name}...")
        return ModelArtifact.create(name=name)
    except AnylearnArtifactDuplicationError:
        console_error(f"Model {name} already exists in your namespace.")
        raise typer.Abort()
    except AnylearnInvalidResponseError:
        console_error(f"Failed to create model {name}.")
        raise typer.Abort()
    except Exception as e:
        console_error(f"An error occurred during model creation: {e}")
        raise typer.Abort()


def _upload_via_jumps_channel(
    artifact_id: str,
    path: Optional[Union[os.PathLike, bytes, str]],
    compress: bool,
    resume: bool,
) -> None:
    jc = _get_jumps_channel_by_artifact_id(artifact_id, missing_ok=True)
    client_identifier = JumpsChannel.get_client_identifier(path)
    if resume and jc is not None and jc.client_code != client_identifier:
        console_error(
            "Local device or local artifact path "
            "has changed since previous upload."
        )
        raise typer.Abort()
    elif not resume or jc is None:
        jc = _create_jumps_channel(
            artifact_id=artifact_id,
            artifact_local_path=path,
        )
    print(f"Uploading {path} to jump server...")
    uploader = JumpsUploader(
        channel=jc,
        local_path=path,
        compress=compress,
    )
    if uploader.upload() != 0:
        console_error("Upload Failed (jump)")
        raise typer.Abort()
    print("Transforming into Anylearn asset...")
    if not jc.transform():
        console_error("Upload Failed (transform)")
        raise typer.Abort()
    jc.finish()


def _get_jumps_channel_by_artifact_id(
    artifact_id: str,
    missing_ok: bool = True,
) -> Optional[JumpsChannel]:
    try:
        print("Try to restore existing jump server channel...")
        return JumpsChannel.from_artifact_id(artifact_id)
    except:
        if not missing_ok:
            console_error(
                f"Jumps channel for artifact {artifact_id} not found."
            )
            raise typer.Abort()
        return None


def _create_jumps_channel(
    artifact_id: str,
    artifact_local_path: Optional[Union[os.PathLike, bytes, str]],
) -> JumpsChannel:
    try:
        print("Creating jump server channel...")
        return JumpsChannel.create(
            artifact_id=artifact_id,
            artifact_local_path=artifact_local_path,
        )
    except FileNotFoundError:
        console_error(f"Local path {artifact_local_path} not found.")
        raise typer.Abort()
    except AnylearnArtifactTooLargeError:
        raise typer.Abort()
    except AnylearnInvalidResponseError:
        console_error("Failed to create jumps channel.")
        raise typer.Abort()
    except Exception as e:
        console_error(f"An error occurred during jumps upload: {e}")
        raise typer.Abort()
