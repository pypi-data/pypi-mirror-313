# coding=utf8
import json
from datetime import datetime
from enum import Enum
from io import StringIO
from typing import Optional

import numpy
import pandas
from pydantic import BaseModel

from ..Base import AISerializeObject
from ...Util import XLRedisUtil


class CREATE_SOURCE_DE(Enum):
    INPUT = 'input'
    SELF = 'self'
    STEP = 'step'
    pass


class XLLinkDE(BaseModel):
    key: str
    data_type: str
    data: object
    encode_type: Optional[str] = ''
    encode_data_off: Optional[int] = 0
    trace_id_list: list


class XLDE(AISerializeObject):
    def __init__(self, key, data_type, data, create_source: CREATE_SOURCE_DE, trace_id_list, encode_type='',
                 encode_data_off=0):
        # 类型
        self.data_type = data_type
        # key
        self.key = key
        # 数据
        self.data = data
        self.crate_source = create_source
        self.trace_id_list: list = trace_id_list
        # 是否运行编码
        self.encode_type = encode_type
        self.encode_data_off = encode_data_off
        self.encode_list = []

        self.redis_client = XLRedisUtil().get_data_client()
        self.covertData()
        pass

    def __str__(self):
        data_info = self.data
        if isinstance(self.data, object):
            data_info = self.data.__str__()
        return '<{}>{}<{}>'.format(self.key, data_info, self.crate_source)
        pass

    def covertData(self):
        if self.data_type == 'datetime' and isinstance(self.data, str):
            self.data = datetime.strptime(self.data, "%Y-%m-%d %H:%M:%S")
        if self.data_type == 'ndarray' and isinstance(self.data, str):
            self.data = numpy.asarray(json.loads(self.data))
        if self.data_type == 'DataFrame' and isinstance(self.data, str):
            data_str = self.redis_client.get(self.data)
            if data_str is not None:
                self.data = pandas.read_json(StringIO(data_str))
            else:
                self.data_type = 'expire'
            pass
        pass

    def toLinkDE(self):
        if self.data_type == 'datetime' and isinstance(self.data, datetime):
            str_data = self.data.strftime("%Y-%m-%d %H:%M:%S")
        elif self.data_type == 'ndarray' and isinstance(self.data, numpy.ndarray):
            # 将numpy数组转换为列表
            data_list = self.data.tolist()
            # 将数据转换为JSON格式的字符串
            str_data = json.dumps(data_list)
        elif self.data_type == 'DataFrame':
            str_data = datetime.now().strftime("ext-data-DataFrame-%Y%m%d_%H%M%S_%f")
            # 默认10分钟
            self.redis_client.set(str_data, self.data.to_json(), ex=600)
        else:
            str_data = self.data

        return {
            'key': self.key,
            'data_type': self.data_type,
            'encode_type': self.encode_type,
            'encode_data_off': self.encode_data_off,
            'data': str_data,
            'trace_id_list': self.trace_id_list
        }
        pass


class XLDataUtil(object):

    @staticmethod
    def INPUT_Build(data_info: XLLinkDE) -> XLDE:
        entity: XLDE = XLDE(key=data_info.key, data_type=data_info.data_type, data=data_info.data,
                            encode_type=data_info.encode_type,
                            encode_data_off=data_info.encode_data_off, create_source=CREATE_SOURCE_DE.INPUT,
                            trace_id_list=data_info.trace_id_list)
        return entity
        pass

    @staticmethod
    def SELF_Build(key, data, create_id, data_type=None) -> XLDE:
        if data_type is None:
            data_type = type(data).__name__
        entity: XLDE = XLDE(key=key, data_type=data_type, data=data, create_source=CREATE_SOURCE_DE.SELF,
                            trace_id_list=[create_id])
        return entity
        pass

    @staticmethod
    def STEP_Build(data_info: dict) -> XLDE:
        data_type = data_info.get('data_type')
        data = data_info.get('data')
        encode_type = '' if data_info.get('encode_type') is None else data_info.get('encode_type')
        encode_data_off = 0 if data_info.get('encode_data_off') is None else data_info.get('encode_data_off')

        entity: XLDE = XLDE(key=data_info.get('key'), data_type=data_type, data=data, encode_type=encode_type,
                            encode_data_off=encode_data_off,
                            create_source=CREATE_SOURCE_DE.STEP, trace_id_list=data_info.get('trace_id_list'))
        return entity
        pass

    @staticmethod
    def INPUT_DICT_Build(data_info: dict) -> XLDE:
        encode_type = '' if data_info.get('encode_type') is None else data_info.get('encode_type')
        encode_data_off = 0 if data_info.get('encode_data_off') is None else data_info.get('encode_data_off')
        entity: XLDE = XLDE(key=data_info['key'], data_type=data_info['data_type'], data=data_info['data'],
                            create_source=CREATE_SOURCE_DE.INPUT, trace_id_list=data_info['trace_id_list'],
                            encode_type=encode_type, encode_data_off=encode_data_off)
        return entity
        pass


pass
