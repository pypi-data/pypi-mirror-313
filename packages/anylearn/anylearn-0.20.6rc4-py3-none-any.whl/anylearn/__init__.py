from typing import Optional

import anylearn.env as env
from anylearn.applications import (
    report_intermediate_metric,
    report_final_metric,
    run,
    sync_algorithm,
    quick_train,
    upload,
    upload_and_run,
)
from anylearn.config import (
    AnyLearnAuthException,
    AnylearnConfig,
    init_sdk,
)
from anylearn.sdk import (
    Auth,
    Context,
    DatasetArtifact,
    FileArtifact,
    ModelArtifact,
    Task,
    get_task_output,
    init,
)
from anylearn.anyboard import WriterManager as SummaryWriter


def create_dataset(
    name: str,
    description: Optional[str] = None,
    public: bool = False,
) -> DatasetArtifact:
    return DatasetArtifact.create(
        name=name,
        description=description,
        public=public,
    )


def get_dataset(full_name: str) -> DatasetArtifact:
    return DatasetArtifact.from_full_name(full_name)


def get_model(full_name: str) -> ModelArtifact:
    return ModelArtifact.from_full_name(full_name)


# Detect auth info in env and init config
if env.inside_train_task():
    pass
else:
    auth = env.get_auth()
    if auth['host'] and auth['token']:
        AnylearnConfig.init_cluster_by_token(**auth)
        AnylearnConfig.init_workspace()
        AnylearnConfig.check_git()
        # Token may have expired then been refreshed
        env.set_token(AnylearnConfig.token)
