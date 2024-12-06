# coding=utf8
import inspect
import json
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import requests
from fastapi.dependencies.utils import analyze_param
from redis import Redis

from ...Department import BaseDPart
from ...Util import XLRedisUtil, XLLogger

_register_link = []

def mqLink(path, **kwargs):
    def decorator(func):
        sig = inspect.signature(func)
        param_field_list = []
        for param_name, param in sig.parameters.items():
            _param_info = analyze_param(
                param_name=param_name,
                annotation=param.annotation,
                value=param.default,
                is_path_param=False,
            )
            param_field_list.append(_param_info.field)
        _register_link.append([path, kwargs, func, param_field_list])

    return decorator


def _getSetSubIndex(redis_client: Redis, name, group, new_id=None):
    key = group + ":" + name + "readid"
    if new_id is not None:
        redis_client.set(key, new_id)
        return new_id
    return redis_client.get(key) or '0-0'


def _mqHandler(link_config: list, env_flag):
    logger = XLLogger()
    try:
        redis_util = XLRedisUtil()
        [mq_key, kwargs, func, param_list] = link_config
        if env_flag == 'dev':
            mq_key = 'dev_' + mq_key
        group = 'main'
        redis_client = redis_util.get_mq_client()
        try:
            redis_client.xinfo_consumers(name=mq_key, groupname=group)
        except Exception as e:
            redis_client.xadd(mq_key, {'sys': 'create'})
            consumer_id = _getSetSubIndex(redis_client, group=group, name=mq_key)
            redis_client.xgroup_create(name=mq_key, groupname=group, id=consumer_id)
        logger.info('mq 启动成功 mq_key:{}'.format(mq_key))
        while True:
            content = ""
            try:
                # block 0 时阻塞等待, 其他数值表示读取超时时间
                [[name, [(nid, content)]]] = redis_client.xreadgroup(groupname=group, consumername="consumer",
                                                                     streams={mq_key: '>'}, count=1, block=0)
                _ = _getSetSubIndex(redis_client, group=group, name=mq_key, new_id=nid)
                if not isinstance(content, dict) or len(content) ==0 or content.get('sys') is not None:
                    continue

                run_args = {}
                for param in param_list:
                    content_dict = json.loads(content[param.name].encode('utf-8'))
                    body_values, errors_ = param.validate(content_dict, {}, loc=("body",))
                    if isinstance(errors_, list) or errors_:
                        logger.error('解析数据错误； key:{} , data:{}'.format(param.name, content[param.name]))
                        continue
                    run_args[param.name] = body_values
                    pass

                logger.info("ev mq 收到消息; mq_key:{}| {} ".format(mq_key, run_args))
                if env_flag != 'dev' and redis_util.get('mq_dev_flag') is not None:
                    logger.info("ev mq 数据转发 mq_key：{} ttl:{}".format(mq_key, redis_util.ttl('mq_dev_flag')))
                    _ = redis_client.xadd('dev_' + mq_key, content)
                    continue
                    pass
                func(**run_args)
                pass
            except Exception as ex:
                logger.error("mq消息处理异常 content:{} e:{}".format(content, ex))
                traceback.print_exc()
                pass
    except Exception as e:
        logger.error("mq _mqRun 启动异常 link_config:{} e:{}".format(link_config, e))
        traceback.print_exc()
    pass


def _mqdev_handler(department: BaseDPart, env_flag):
    logger = XLLogger()
    if env_flag != 'dev':
        logger.info('_mqdev_handler 环境不是dev 可以不用执行')
        return
    while True:
        try:
            response = requests.post('http://host.home.tokgo.cn:{}/mq/dev/link/register'.format(department.port))
            # 间隔50秒
            time.sleep(50)
            pass
        except Exception as e:
            logger.error('_mqdev_handler 处理任务错')
            traceback.print_exc()
            time.sleep(30)
            pass
    pass


def sendMqData(mq_key, req):
    try:
        return XLRedisUtil().get_mq_client().xadd(mq_key, {'req': json.dumps(req)})
    except Exception as e:
        logger = XLLogger()
        logger.error("mq 发送消息失败; e:{}".format(e))
    pass


def mqSystemInit(department: BaseDPart, env_flag='dev'):
    if len(_register_link) == 0:
        return
    threadPool = ThreadPoolExecutor(max_workers=len(_register_link) + 1)
    for link_config in _register_link:
        threadPool.submit(_mqHandler, link_config, env_flag)

    # dev 环境相关的处理线程
    threadPool.submit(_mqdev_handler, department, env_flag)
    pass
