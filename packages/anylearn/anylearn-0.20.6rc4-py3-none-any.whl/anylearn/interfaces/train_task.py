import os
from datetime import datetime
import json
import time
from typing import Dict, List, Optional, Union

from anylearn.utils.api import (
    url_base,
    get_with_token,
    patch_with_token,
    post_with_token,
    post_with_secret_key,
)
from anylearn.utils.errors import (
    AnyLearnException,
    AnyLearnMissingParamException,
)
from anylearn.utils.func import logs_beautify
from anylearn.interfaces.base import BaseObject
from anylearn.interfaces.resource import (
    File,
    Model,
    Resource,
    ResourceDownloader,
    ResourceState,
    SyncResourceDownloader,
)
from anylearn.interfaces.train_tag import TrainTag
from anylearn.__about__ import __version__ as anylearn_version


class TrainTaskState:
    """
    训练任务状态标识：

    - 0(CREATED)表示已创建
    - 1(RUNNING)表示运行中
    - 2(SUCCESS)表示已完成
    - -1(DELETED)表示已删除
    - -2(FAIL)表示失败
    - -3(ABORT)表示中断
    """
    CREATED = 0
    RUNNING = 1
    SUCCESS = 2
    DELETED = -1
    FAIL = -2
    ABORT = -3


class TrainTask(BaseObject):
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
    train_params
        训练任务参数列表
    train_params_prefix
        训练超参数键前标识
    train_params_delimeter
         训练超参数键值间的分隔符
    files
        训练相关的文件（默认'' 多个的话用逗号','隔开）
    results_id
        训练结果文件ID
    secret_key
        密钥
    create_time
        创建时间
    finish_time
        结束时间
    envs
        训练任务环境变量（默认''）
    hpo
        是否开启超参数自动调优
    hpo_search_space
        开启超参数自动调优时不能为空
    final_metric
        最终结果指标
    load_detail
        初始化时是否加载详情
    resource_request : :obj:`List[Dict[str, Dict[str, int]]]`, optional
        训练所需计算资源的请求。
        如未填，则使用Anylearn后端的:obj:`default`资源组中的默认资源套餐。
    entrypoint
        算法训练的启动命令，非标准算法必填
    output
        算法训练结果（模型）存储目录路径，非标准算法必填
    mirror_id
        训练使用的镜像ID，默认为空，即使用算法绑定的镜像ID
    """

    _fields = {
        # 资源创建/更新请求包体中必须包含且不能为空的字段
        'required': {
            'create': ['name', 'project_id', 'algorithm_id', 'train_params'],
            'update': [],
        },
        # 资源创建/更新请求包体中包含的所有字段
        'payload': {
            'create': ['name', 'description', 'project_id', 'algorithm_id',
                       'algorithm_git_ref', 'train_params', 'envs',
                       'train_params_prefix', 'train_params_delimeter',
                       'files', 'resource_request', 'num_nodes', 'nproc_per_node',
                       'entrypoint', 'output', 'mirror_id'],
            'update': [],
        },
    }
    """
    创建/更新对象时：

    - 必须包含且不能为空的字段 :obj:`_fields['required']`
    - 所有字段 :obj:`_fields['payload']`
    """

    def __init__(self,
                 id: Optional[str]=None,
                 name: Optional[str]=None,
                 description: Optional[str]=None,
                 state: Optional[int]=None,
                 creator_id: Optional[str]=None,
                 project_id: Optional[str]=None,
                 algorithm_id: Optional[str]=None,
                 algorithm_git_ref: Optional[str]=None,
                 train_params: Optional[str]=None,
                 train_params_prefix: str="--",
                 train_params_delimeter: str=" ",
                 files: Optional[list]=None,
                 results_id: Optional[str]=None,
                 secret_key: Optional[str]=None,
                 create_time: Optional[datetime]=None,
                 finish_time: Optional[datetime]=None,
                 envs: Optional[str]=None,
                 hpo=False,
                 hpo_search_space: Optional[str]=None,
                 final_metric: Optional[float]=None,
                 resource_request: Optional[List[Dict[str, Dict[str, int]]]]=None,
                 load_detail=False,
                 entrypoint: Optional[str]=None,
                 output: Optional[Union[os.PathLike, bytes, str]]=None,
                 mirror_id: Optional[str]=None,
                 num_nodes=1,
                 nproc_per_node=1):
        """
        Parameters
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
        train_params
            训练任务参数列表
        train_params_prefix
            训练超参数键前标识
        train_params_delimeter
            训练超参数键值间的分隔符
        files
            训练相关的文件（默认'' 多个的话用逗号','隔开）
        results_id
            训练结果文件ID
        secret_key
            密钥
        create_time
            创建时间
        finish_time
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
        load_detail
            初始化时是否加载详情
        num_nodes
            训练任务请求的节点数
        entrypoint
            算法训练的启动命令，非标准算法必填
        output
            算法训练结果（模型）存储目录路径，非标准算法必填
        mirror_id
            训练使用的镜像ID，默认为空，即使用算法绑定的镜像ID
        """
        self.name = name
        self.description = description
        self.state = state
        self.creator_id = creator_id
        self.project_id = project_id
        self.algorithm_id = algorithm_id
        self.algorithm_git_ref = algorithm_git_ref
        self.train_params = train_params
        self.train_params_prefix = train_params_prefix
        self.train_params_delimeter = train_params_delimeter
        self.files = files
        self.results_id = results_id
        self.secret_key = secret_key
        self.create_time = create_time
        self.finish_time = finish_time
        self.envs = envs
        self.hpo = hpo
        self.hpo_search_space = hpo_search_space
        self.final_metric = final_metric
        self.resource_request = resource_request
        self.num_nodes = num_nodes
        self.nproc_per_node = nproc_per_node
        self.entrypoint = entrypoint
        self.output = output
        self.mirror_id = mirror_id
        super().__init__(id=id, load_detail=load_detail)

    def finished(self):
        """
        检查训练任务是否完成

        Returns
        -------
        bool
            True or False
        """
        return self.state in [
            TrainTaskState.SUCCESS,
            TrainTaskState.FAIL,
            TrainTaskState.ABORT,
            TrainTaskState.DELETED,
        ]

    @classmethod
    def get_list(cls):
        """
        Listing is not supported for TrainTask
        """
        raise AnyLearnException("Listing is not supported for TrainTask")

    def get_detail(self):
        """
        获取训练任务详细信息

        - 对象属性 :obj:`id` 应为非空

        Returns
        -------
        TrainTask
            训练任务对象。
        """
        self._check_fields(required=['id'])
        res = get_with_token(f"{url_base()}/train_task/query",
                             params={'id': self.id})
        if not res or not isinstance(res, list):
            raise AnyLearnException("请求未能得到有效响应")
        res = res[0]
        self.__init__(id=res['id'], name=res['name'],
                      description=res['description'], state=res['state'],
                      creator_id=res['creator_id'],
                      project_id=res['project_id'],
                      algorithm_id=res['algorithm_id'],
                      algorithm_git_ref=res['algorithm_git_ref'],
                      train_params=res['args'], files=res['files'],
                      results_id=res['results_id'],
                      secret_key=res['secret_key'],
                      create_time=res['create_time'],
                      finish_time=res['finish_time'],
                      entrypoint=res['entrypoint'],
                      output=res['output'],
                      mirror_id=res['mirror_id'],
                      envs=res['envs'],
                      resource_request=json.loads(res['resource_request']))

    def _create(self):
        data = self._payload_create()
        if data['files'] and isinstance(data['files'], list):
            data['files'] = ','.join(data['files'])
        if self.hpo:
            if not self.hpo_search_space:
                msg = f"{self.__class__.__name__}缺少必要字段：hpo_search_space" + \
                    "——当开启超参数自动调优时（hpo==True），hpo_search_space为必填字段"
                raise AnyLearnMissingParamException(msg)
            data['hpo'] = 1
            data['hpo_search_space'] = json.dumps(self.hpo_search_space)
        if data['resource_request']:
            data['resources'] = json.dumps(data['resource_request'])
        del(data['resource_request'])
        data['sdk_version'] = anylearn_version
        res = post_with_token(self._url_create(), data=data)
        if not res or 'data' not in res:
            raise AnyLearnException("请求未能得到有效响应")
        self.id = res['data']
        return True

    def _update(self):
        # No update for train task
        pass

    def get_log(self, limit=100, direction="init", offset=0, offset_index=-1):
        """
        训练任务日志查询接口

        - 对象属性 :obj:`id` 应为非空

        :param limit: :obj:`int`
            日志条数上限（默认值100）。
        :param direction: :obj:`str`
            日志查询方向。
        :param offset: :obj:`int`
            日志查询偏移量。
        :param offset_index :obj:`int`
            日志查询偏移量索引，搭配偏移量使用作为分页基准。

        :return: 

            .. code-block:: json

                [
                  {
                    "offset": 164324567,
                    "offset_index": 1234,
                    "text": "Task TRAId123 started."
                  },
                  {
                    "offset": 164324590,
                    "offset_index": 1238,
                    "text": "Task TRAId123 finished."
                  }
                ]

        """
        self._check_fields(required=['id'])
        params = {
            'id': self.id,
            'limit': limit,
            'direction': direction,
            'index': offset,
            'offset_index': offset_index,
        }
        res = get_with_token(f"{url_base()}/train_task/logs", params=params)
        if not res or type(res) != list:
            raise AnyLearnException("请求未能得到有效响应")
        return [r for r in res if r['text'].strip()]

    def get_last_log(self, limit: int=100, debug: bool=False):
        """
        训练任务日志最近n行查询接口，返回日志文本列表。

        - 对象属性 :obj:`id` 应为非空

        :param limit :obj:`int`
            需要查询的行数（默认100）。
        :param debug :obj:`bool`
            是否显示更全面的debug信息（默认False）。

        :return: 

            .. code-block:: json

                [
                  "log text1",
                  "log text2"
                ]

        """
        logs = logs_beautify(logs=self.get_log(limit=limit), debug=debug)
        return list(reversed(logs))

    def get_full_log(self, debug: bool=False):
        """
        训练任务日志全量查询接口，返回日志文本列表。

        - 对象属性 :obj:`id` 应为非空

        :param debug :obj:`bool`
            是否显示更全面的debug信息（默认False）。

        :return: 

            .. code-block:: json

                [
                  "log text1",
                  "log text2"
                ]

        """
        logs = []
        offset = 0
        offset_index = -1
        while True:
            try:
                log_parts = self.get_log(
                    offset=offset,
                    offset_index=offset_index,
                    direction="back"
                )
                last = log_parts[-1]
                offset = last['offset']
                offset_index = last['offset_index']
                logs.extend(log_parts)
            except:
                break
        return logs_beautify(logs=logs, debug=debug)

    def stream_log(self,
                   init_limit: int=100,
                   polling: int=2,
                   debug: bool=False):
        """
        实时训练任务日志流式生成接口，每次迭代返回日志文本的一行。

        - 对象属性 :obj:`id` 应为非空

        :param init_limit :obj:`bool`
            起始日志需要查询的行数（默认100）。
        :param polling :obj:`int`
            轮询间隔时间（单位：秒，默认2）。
        :param debug :obj:`bool`
            是否显示更全面的debug信息（默认False）。

        :return: :obj:`Iterator`

        """
        # Some initial logs (latest)
        logs = []
        while not logs:
            logs = self.get_log(limit=init_limit)
        for l in reversed(logs_beautify(logs, debug=debug)):
            yield l
        # Keep fetching new logs
        offset = logs[0]['offset']
        offset_index = logs[0]['offset_index']
        while not self.finished():
            try:
                self.get_detail()
                logs = self.get_log(
                    offset=offset,
                    offset_index=offset_index,
                    direction="back",
                )
                if not logs:
                    continue
                for l in logs_beautify(logs, debug=debug):
                    yield l
                offset = logs[-1]['offset']
                offset_index = logs[-1]['offset_index']
            except:
                time.sleep(polling)

    def get_status(self):
        """
        训练任务状态查询接口

        - 对象属性 :obj:`id` 、 :obj:`secret_key` 应为非空

        :return: 
            .. code-block:: json

                {
                  "current_epoch": "2",
                  "current_train_loss": "2.169192314147949",
                  "current_train_step": "1288",
                  "ip": "10.244.2.124",
                  "process": "1.0",
                  "secret_key": "TKEY123",
                  "state": "success"
                }

        """
        self._check_fields(required=['id', 'secret_key'])
        params = {
            'id': self.id,
            'secret_key': self.secret_key,
        }
        res = get_with_token(f"{url_base()}/train_task/status", params=params)
        if not res or type(res) != dict:
            raise AnyLearnException("请求未能得到有效响应")
        return res

    def download_results(self,
                         save_path: Optional[Union[str, bytes, os.PathLike]],
                         async_download: bool=True,
                         downloader: Optional[ResourceDownloader]=None,
                         polling: Union[float, int]=5,
                        ):
        """
        下载训练任务结果

        Parameters
        ----------
        save_path : :obj:`str`
            文件保存路径。
        downloader : :obj:`ResourceDownloader`
            可以使用SDK中的SyncResourceDownloader，也可以自定义实现ResourceDownloader。
        polling : :obj:`float, int`
            下载前要先压缩文件，轮询查看文件有没有压缩完的时间间隔，单位：秒。默认值5

        Returns
        -------
        str
            文件名。
        """
        self._check_fields(required=['results_id'])
        if self.state == TrainTaskState.FAIL:
            raise AnyLearnException("训练失败！")
        elif self.state == TrainTaskState.DELETED:
            raise AnyLearnException("训练已删除！")
        elif self.state == TrainTaskState.ABORT:
            raise AnyLearnException("训练中断！")
        elif self.state == TrainTaskState.CREATED:
            raise AnyLearnException("训练未开始!")
        elif self.state == TrainTaskState.RUNNING:
            raise AnyLearnException("正在训练中，请耐心等待...")
        if not downloader:
            if async_download:
                downloader = SyncResourceDownloader()
            else:
                downloader = SyncResourceDownloader()
        return Resource.download_file(resource_id=self.results_id, # type: ignore
                                      save_path=save_path,
                                      downloader=downloader,
                                      polling=polling,
                                     )

    def report_final_metric(self, metric: float):
        """
        训练任务汇报最终结果指标

        - 对象属性 :obj:`id` 、 :obj:`secret_key` 应为非空

        :param metric: :obj:`float`
            最终结果指标。

        :return:
            .. code-block:: json

                {
                  "msg": "任务TRAId123结果指标保存成功"
                }

        """
        self._check_fields(required=['id', 'secret_key'])
        data = {
            'id': self.id,
            'metric': metric,
        }
        res = post_with_secret_key(f"{url_base()}/train_task/final_metric",
                                   data=data,
                                   secret_key=self.secret_key)
        if not res or type(res) != dict:
            raise AnyLearnException("请求未能得到有效响应")
        self.final_metric = metric
        return res

    def get_final_metric(self):
        """
        获取训练任务最终结果指标

        - 对象属性 :obj:`id` 应为非空

        :return: 
            .. code-block:: json

                {
                  "final_metric": 662.8,
                  "id": "TRAI1d3",
                  "name": "test"
                }

        """
        self._check_fields(required=['id'])
        res = get_with_token(f"{url_base()}/train_task/final_metric",
                             params={'id': self.id})
        if not res or 'final_metric' not in res:
            raise AnyLearnException("请求未能得到有效响应")
        self.final_metric = res['final_metric']
        return res

    def report_intermediate_metric(self, metric: float):
        """
        训练任务汇报中间结果指标

        - 对象属性 :obj:`id` 、 :obj:`secret_key` 应为非空

        :param metric: :obj:`float`
            中间结果指标。

        :return: 
            .. code-block:: json

                {
                  "msg": "任务TRAId123结果指标保存成功"
                }

        """
        self._check_fields(required=['id', 'secret_key'])
        data = {
            'id': self.id,
            'metric': metric,
        }
        res = post_with_secret_key(f"{url_base()}/train_task/intermediate_metric",
                                   data=data,
                                   secret_key=self.secret_key)
        if not res or type(res) != dict:
            raise AnyLearnException("请求未能得到有效响应")
        return res

    def get_intermediate_metric(self, last_timestamp: str="1970-01-01 00:00:00"):
        """
        获取训练任务中间结果指标

        - 对象属性 :obj:`id` 应为非空

        :param last_timestamp: :obj:`str`
            仅获取某一时刻以后的中间结果,格式"1970-01-01 00:00:00"

        :return: 
            .. code-block:: json

                [
                  {
                    "id": "METR123",
                    "metric": 90.0,
                    "train_task_id": "TRAI123",
                    "reported_at": "2021-04-29 21:00:00"
                  },
                  {
                    "id": "METR456",
                    "metric": 99.0,
                    "train_task_id": "TRAI123",
                    "reported_at": "2021-04-29 21:10:00"
                  }
                ]

        """
        self._check_fields(required=['id'])
        res = get_with_token(f"{url_base()}/train_task/intermediate_metric",
                             params={
                                 'id': self.id,
                                 'last_timestamp': last_timestamp,
                             })
        if not res or type(res) != list:
            raise AnyLearnException("请求未能得到有效响应")
        return res

    def transform_model(self,
                        file_path: Optional[Union[str, bytes, os.PathLike]],
                        name: str,
                        description: Optional[str]=None,
                        is_zipfile: bool=False,
                        public: bool=False,
                        polling: Union[float, int]=5):
        """
        模型文件转存接口

        - 对象属性 :obj:`results_id` 、 :obj:`algorithm_id` 应为非空

        Parameters
        ----------
        file_path : :obj:`str`
            模型文件路径。
        name : :obj:`str`
            模型的名称。
        description : :obj:`str`
            模型描述。
        is_zipfile : :obj:`bool`
            模型是否为zip文件。默认为False。
        public : :obj:`bool`
            模型是否公开。默认为False。
            模型转存后可到前端模型详情中设置模型的协作者。
        polling : :obj:`float|int`
            模型转换中轮询模型状态的时间间隔（单位：秒）。 默认为5秒。

        Returns
        -------
        Model
            模型对象。
        """
        self._check_fields(required=['results_id', 'algorithm_id'])
        data = {
            'file_id': self.results_id,
            'file_path': file_path,
            'name': name,
            'description': description,
            'algorithm_id': self.algorithm_id,
            'is_zipfile': "1" if is_zipfile else "0",
            'public': int(public),
        }
        res = post_with_token(f"{url_base()}/model/transform",
                              data=data)
        if not res or 'data' not in res:
            raise AnyLearnException("请求未能得到有效响应")
        model = Model(id=res['data'])
        finished = [ResourceState.ERROR, ResourceState.READY]
        while model.state not in finished:
            time.sleep(polling)
            model.get_detail()
        if model.state == ResourceState.ERROR:
            raise AnyLearnException("Error occured when transforming model")
        return model
    
    def tag_tags(self, tags: List[TrainTag]):
        """
        给训练项目打标签
        
        - 对象属性 :obj:`id` 应为非空

        Parameters
        ----------
        tags : :obj:`list`
            将要打在训练任务上的标签列表。
        """
        self._check_fields(required=['id'])
        data = {
            'tags': json.dumps({
                self.id: [tag.id for tag in tags]
            })
        }
        res = patch_with_token(f"{url_base()}/train_task/tags", data=data)
        if not res or 'data' not in res:
            raise AnyLearnException("请求未能得到有效响应")

    def get_results_file(self) -> File:
        self._check_fields(required=['results_id'])
        return File(id=self.results_id, load_detail=True)

    def _namespace(self):
        return "train_task"
