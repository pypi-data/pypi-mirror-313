from __future__ import annotations

from anylearn.sdk.client import get_with_token
from anylearn.sdk.context import get_base_url
from anylearn.sdk.errors import AnylearnInvalidResponseError


class Task:
    """
    AnyLearn训练任务类，以方法映射训练任务CRUD相关接口

    Attributes
    ----------
    id
        训练任务的唯一标识符，自动生成，由TRAI+uuid1生成的编码中后28个有效位（小写字母和数字）组成
    name
        训练任务的名称(长度1~50）)
    description
        训练任务描述（长度最大255）
    state
        训练任务状态
    creator_id
        创建者ID
    project_id
        训练项目ID
    algorithm_id
        算法ID
    algorithm_git_ref
        算法Gitea代码仓库的版本号（可以是commit号、分支名、tag名），非必填。
    hyperparams
        任务超参数列表
    hyperparams_prefix
        任务超参数键前标识
    hyperparams_delimeter
         任务超参数键值间的分隔符
    input_artifact_ids
        任务输入资产ID列表（以逗号分隔）
    output_artifact_id
        任务输出文件资产ID
    secret_key
        密钥
    created_at
        创建时间
    started_at
        任务开始执行时间
    finished_at
        结束时间
    envs
        训练任务环境变量（默认''）
    hpo
        是否开启超参数自动调优
    hpo_search_space
        开启超参数自动调优时不能为空
    final_metric
        最终结果指标
    resource_request : :obj:`List[Dict[str, Dict[str, int]]]`, optional
        训练所需计算资源的请求。
        如未填，则使用Anylearn后端的:obj:`default`资源组中的默认资源套餐。
    entrypoint
        算法训练的启动命令，非标准算法必填
    output_path
        算法训练结果（模型）存储目录路径，非标准算法必填
    image_id
        训练使用的镜像ID，默认为空，即使用算法绑定的镜像ID
    """

    def __init__(self, *_, **kwargs):
        self.id = kwargs.pop('id', None)
        self.name = kwargs.pop('name', None)
        self.description = kwargs.pop('description', None)
        self.state = kwargs.pop('state', None)
        self.creator_id = kwargs.pop('creator_id', None)
        self.project_id = kwargs.pop('project_id', None)
        self.algorithm_id = kwargs.pop('algorithm_id', None)
        self.algorithm_git_ref = kwargs.pop('algorithm_git_ref', None)
        self.hyperparams = kwargs.pop('train_params', None)
        self.hyperparams_prefix = kwargs.pop('train_params_prefix', "--")
        self.hyperparams_delimeter = kwargs.pop('train_params_delimeter', " ")
        self.input_artifact_ids = kwargs.pop('files', None)
        self.output_artifact_id = kwargs.pop('results_id', None)
        self.secret_key = kwargs.pop('secret_key', None)
        self.created_at = kwargs.pop('create_time', None)
        self.started_at = kwargs.pop('start_time', None)
        self.finished_at = kwargs.pop('finish_time', None)
        self.envs = kwargs.pop('envs', None)
        self.hpo = kwargs.pop('hpo', False)
        self.hpo_search_space = kwargs.pop('hpo_search_space', None)
        self.final_metric = kwargs.pop('final_metric', None)
        self.resource_request = kwargs.pop('resource_request', None)
        self.distr_num_nodes = kwargs.pop('num_nodes', 1)
        self.distr_num_proc = kwargs.pop('nproc_per_node', 1)
        self.entrypoint = kwargs.pop('entrypoint', None)
        self.output_path = kwargs.pop('output', None)
        self.image_id = kwargs.pop('mirror_id', None)

    @classmethod
    def from_id(cls, id_: str) -> Task:
        res = get_with_token(
            f"{get_base_url()}/train_task/query",
            params={'id': id_},
        )
        if not res or not isinstance(res, list):
            raise AnylearnInvalidResponseError("Request failed")
        return Task(**res[0])
