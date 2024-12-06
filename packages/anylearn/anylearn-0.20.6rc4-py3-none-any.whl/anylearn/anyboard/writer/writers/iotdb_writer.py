import base64
import json
import os

from ..summary import ValueType
from .base import WriterBase, WriterType
from ...utils import anyboard_logger as logger


def get_iotdb_info():
    # 从环境变量获取 self.user,self.pw,self.ip, self.port,self.user_id,self.proj_id,self.task_id
    user_name = os.environ.get("ANYLEARN_ANYBOARD_IOTDB_USER")
    user_pass = os.environ.get("ANYLEARN_ANYBOARD_IOTDB_PASSWORD")
    iotdb_ip = os.environ.get("ANYLEARN_ANYBOARD_IOTDB_HOST")
    iotdb_port = os.environ.get("ANYLEARN_ANYBOARD_IOTDB_PORT")
    user_id = os.environ.get("ANYLEARN_USER_ID")
    proj_id = os.environ.get("ANYLEARN_PROJECT_ID")
    task_id = os.environ.get("ANYLEARN_TASK_ID")
    logger.info(f"get_iotdb_info: User: {user_name}, User ID: {user_id}, User Pass: {user_pass} "
                f"Project ID: {proj_id}, Task ID: {task_id}, IP: {iotdb_ip}, Port: {iotdb_port},")
    # logger.debug(f"get_iotdb_info: {user_name}, {user_pass}, {iotdb_ip}, {iotdb_port}, {user_id}, {proj_id}, {task_id}")
    return user_name, user_pass, iotdb_ip, iotdb_port, user_id, proj_id, task_id


class IotdbWriter(WriterBase):

    def __init__(self):
        super().__init__(WriterType.IOTDB)
        self.user_name, self.password, self.ip, self.port, self.user_id, self.proj_id, self.task_id = get_iotdb_info()
        self.device_prefix = f'root.{self.user_id}.{self.proj_id}.{self.task_id}'
        self.pool_config = None
        self.session_pool = None
        # self.try_register_user() # 发送请求需要Auth

    def set_template(self):
        # error: 803: Only the admin user can perform this operation
        sql = f"set device template scalar_template to {self.device_prefix}.scalar"
        self.retry_execute_non_query_statement(sql)
        sql = f"set device template image_template to {self.device_prefix}.image"
        self.retry_execute_non_query_statement(sql)
        sql = f"set device template histogram_template to {self.device_prefix}.histogram"
        self.retry_execute_non_query_statement(sql)

    def start(self):
        logger.debug("IotdbWriter start")
        if None in [self.user_name, self.password, self.ip, self.port, self.user_id, self.proj_id, self.task_id]:
            msg = "IotdbWriter start failed: get_iotdb_info failed"
            logger.error(msg)
            self.give_up = True
            return
        self.device_prefix = f'root.{self.user_id}.{self.proj_id}.{self.task_id}'
        try:
            from iotdb.SessionPool import PoolConfig
            from iotdb.SessionPool import SessionPool
        except Exception as e:
            msg = f"import iotdb failed, please install 'apache-iotdb': {e}"
            logger.error(msg)
            self.give_up = True
            return
        self.pool_config = PoolConfig(host=self.ip, port=str(self.port), user_name=self.user_name,
                                      password=self.password, fetch_size=1024,
                                      time_zone="UTC+8", max_retry=3)
        self.session_pool = SessionPool(self.pool_config, 25, 30000)
        # self.set_template()
        logger.debug("IotdbWriter start successully")

    def end(self):
        if self.session_pool is not None:
            self.session_pool.close()
        logger.debug("IotdbWriter end")

    def retry_get_session(self):
        count = 0
        while True:
            try:
                session = self.session_pool.get_session()
                return session
            except Exception as e:
                msg = f"get iotdb session failed: {e}"
                logger.error(msg)
                count += 1
                if count > 6 or self.give_up:
                    self.give_up = True
                    msg = "give up get iotdb session after 30s"
                    logger.error(msg)
                    return None
                os.system("sleep 5s")

    def retry_execute_non_query_statement(self, sql):
        # 有极少数时候（写image/初次连接） iotdb会显示连接中断(k8s问题？？？)
        count = 0
        session = self.retry_get_session()
        while True:
            try:
                session.execute_non_query_statement(sql)
                self.session_pool.put_back(session)
                return
            except Exception as e:
                msg = f"execute sql failed: sql: {sql}, error: {e}"
                logger.error(msg)
                count += 1
                if count > 3 or self.give_up:
                    self.give_up = True
                    msg = "give up execute sql after 30s"
                    logger.error(msg)
                    return
                os.system("sleep 10s")

    def create(self, name, type: ValueType):
        pass
        # FIXME: 只有管理员才能创建设备
        # if type not in ValueType:
        #     msg = f"Type {type} is not supported in IotdbWriter"
        #     logger.error(msg)
        #     return
        # create_sql = f"create timeseries using device template on {self.device_prefix}.{type.value}.`{name}`"
        # self.retry_execute_non_query_statement(create_sql)

    def add(self, summary):
        device_path = f'{self.device_prefix}.{summary.value.type.value}.`{summary.name}`'
        if summary.value.type == ValueType.SCALAR:
            insert_sql = f"insert into {device_path}" \
                         f"(walltime,step,single_value)values" \
                         f"({summary.walltime},{summary.step},{summary.value.value}) "
        elif summary.value.type == ValueType.IMAGE:
            # 转换成str可以吗!!??base64编码之后用utf-8编码
            insert_img_str = base64.b64encode(summary.value.image_bytes).decode('utf-8')
            s = summary
            v = summary.value  # channel???????????????????????????????????不要 ，还有gif和video？？？？？4透明度？？？
            insert_sql = f"insert into {device_path}" \
                         f"(walltime,step,height,width,channel,size,img_str,file_format)values" \
                         f"({s.walltime},{s.step},{v.height},{v.width},{v.channel},{v.size}," \
                         f"'{insert_img_str}','{v.file_format}')"
        elif summary.value.type == ValueType.HISTOGRAM:
            # 把bucket_limits和bucket_counts使用json.dumps从list编码为字符串
            json_str_bucket_limits = json.dumps(summary.value.bucket_limits)
            json_str_bucket_counts = json.dumps(summary.value.bucket_counts)
            s = summary
            v = summary.value
            insert_sql = f"insert into {device_path}" \
                         f"(walltime,step,min,max,num,sum,sum_squares,bucket_limits,bucket_counts)values" \
                         f"({s.walltime},{s.step},{v.min},{v.max},{v.num},{v.sum},{v.sum_squares}," \
                         f"'{json_str_bucket_limits}','{json_str_bucket_counts}')"
        else:
            msg = f"Type {summary.value.type} is not supported in IotdbWriter"
            logger.error(msg)
            return
        self.retry_execute_non_query_statement(insert_sql)
