from .artifacts.algorithm import AlgorithmArtifact
from .artifacts.artifact import Artifact, ArtifactState
from .artifacts.dataset import DatasetArtifact
from .artifacts.file import FileArtifact
from .artifacts.model import ModelArtifact
from .auth import Auth
from .context import Context, init
from .project import Project
from .task import Task

def get_task_output(task_id: str) -> FileArtifact:
    task = Task.from_id(task_id)
    return FileArtifact.from_id(task.output_artifact_id)
