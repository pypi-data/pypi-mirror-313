# coding=utf8
import json
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import requests
from redis import Redis

from ...Department import BaseDPart
from ...Util import XLRedisUtil, XLLogger

dev_mq_key = None
online_mq_key = None


def _getSetSubIndex(redis_client: Redis, name, group, new_id=None):
    key = group + ":" + name + "readid"
    if new_id is not None:
        redis_client.set(key, new_id)
        return new_id
    return redis_client.get(key) or '0-0'


def _mqHandler(rec_mq_key, department: BaseDPart, env_flag):
    logger = XLLogger()
    redis_util = XLRedisUtil()
    redis_client = redis_util.get_mq_client()
    try:
        group = 'main'
        try:
            redis_client.xinfo_consumers(name=rec_mq_key, groupname=group)
        except Exception as e:
            redis_client.xadd(rec_mq_key, {'sys': 'create'})
            consumer_id = _getSetSubIndex(redis_client, group=group, name=rec_mq_key)
            redis_client.xgroup_create(name=rec_mq_key, groupname=group, id=consumer_id)

        while True:
            content = ""
            try:
                # block 0 时阻塞等待, 其他数值表示读取超时时间
                [[name, [(nid, content)]]] = redis_client.xreadgroup(groupname=group, consumername="consumer",
                                                                     streams={rec_mq_key: '>'}, count=1, block=0)
                _ = _getSetSubIndex(redis_client, group=group, name=rec_mq_key, new_id=nid)
                if not isinstance(content, dict) or len(content) == 0 or content.get('sys') is not None:
                    continue
                if env_flag == 'dev':
                    # if rec_mq_key == 'dev_http_event':
                    b_url = 'http://127.0.0.1:{}{}'.format(department.port, content['path'])
                    # 测试环境执行的逻辑
                    if content['method'] == 'POST':
                        response = requests.post(b_url, json=json.loads(content['str_body']))
                        redis_client.xadd(online_mq_key,
                                          {'evnet_id': content['evnet_id'], 'content': response.content,
                                           'status_code': response.status_code, 'text': response.text})
                    elif content['method'] == 'GET':
                        response = requests.get(b_url, params=json.loads(content['path_params']))
                        redis_client.xadd(online_mq_key,
                                          {'evnet_id': content['evnet_id'],
                                           'status_code': response.status_code,
                                           'content': response.content,
                                           'text': response.text})
                else:
                    # 运行环境执行的逻辑; 使用默认的保存60s
                    redis_util.setDict('dev_http_back_' + content['evnet_id'], content)
                pass
            except Exception as ex:
                logger.error("mq消息处理异常 content:{} e:{}".format(content, ex))
                traceback.print_exc()
                pass
    except Exception as e:
        logger.error("mq _mqHandlerDev 启动异常 e:{}".format(e))
        traceback.print_exc()
    pass


def _mqdev_handler(department: BaseDPart, env_flag):
    logger = XLLogger()
    if env_flag != 'dev':
        logger.info('_mqdev_handler 环境不是dev 可以不用执行')
        return
    while True:
        try:
            response = requests.post('http://host.home.tokgo.cn:{}/dev/mq/http/link/register/'.format(department.port))
            # 间隔50秒
            time.sleep(50)
            pass
        except Exception as e:
            logger.error('_mqdev_handler 处理任务错')
            traceback.print_exc()
            time.sleep(30)
            pass
    pass


def sendDevMqData(evnet_id, method, path, path_params, str_body):
    try:
        return XLRedisUtil().get_mq_client().xadd(dev_mq_key, {'evnet_id': evnet_id, 'method': method, 'path': path,
                                                               'path_params': json.dumps(path_params),
                                                               'str_body': str_body})
    except Exception as e:
        logger = XLLogger()
        logger.error("mq http 发送消息失败; e:{}".format(e))
    pass


def HttpDevMQInit(department: BaseDPart, env_flag='dev'):
    global dev_mq_key
    global online_mq_key
    dev_mq_key = '{}_dev_http_event'.format(department.name)
    online_mq_key = '{}_online_http_event'.format(department.name)

    threadPool = ThreadPoolExecutor(max_workers=2)
    if env_flag == 'dev':
        threadPool.submit(_mqHandler, dev_mq_key, department, env_flag)
        # threadPool.submit(_mqHandler, 'online_http_event')
    else:
        threadPool.submit(_mqHandler, online_mq_key, department, env_flag)
    # dev 环境相关的处理线程
    threadPool.submit(_mqdev_handler, department, env_flag)
    pass
