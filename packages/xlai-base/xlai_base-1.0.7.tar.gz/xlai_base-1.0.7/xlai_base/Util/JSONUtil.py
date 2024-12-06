# coding=utf8
import json
from datetime import datetime
from importlib import import_module

from ..XLSYS.Base import AISerializeObject


class CommonEncoderALL(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, AISerializeObject):
            return obj.__dict__
        else:
            ""


class CommonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, object):
            return obj.__str__()
        else:
            return super(CommonEncoder, self).default(obj)


class SaveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            save_dict = {'__class_flag': "datetime",  '__time': obj.strftime("%Y-%m-%d %H:%M:%S")}
            return save_dict
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, object):
            save_dict = {'__class_data': obj.__dict__, '__class_flag': "class", '__class_module': obj.__module__,
                         '__class_name': obj.__class__.__name__}
            return save_dict
        else:
            return super(SaveEncoder, self).default(obj)


class LoadDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        super().__init__(
            object_hook=self.object_hook,
            # parse_float=self.parse_float,
            # parse_int=self.parse_int,
            # parse_constant=self.parse_constant,
            # object_pairs_hook=self.object_pairs_hook,
            *args, **kwargs)

    def object_hook(self, o):
        """
        对字典解码，如果同时设置'object_pairs_hook'，'object_hook'将不生效
        :param o: 原始数据字典
        :return: 实际需要的数据
        """
        if o.get('__class_flag') is not None and o.get('__class_flag') == 'class':
            obj = getattr(import_module(name=o['__class_module']), o['__class_name'])()
            obj.__dict__ = o['__class_data']
            return obj
        if o.get('__class_flag') is not None and o.get('__class_flag') == 'datetime':
            return datetime.strptime(o['__time'], "%Y-%m-%d %H:%M:%S")
        return o

    # def parse_float(self, o):
    #     """
    #     对浮点型解码
    #     :param o: 原始浮点型
    #     :return: 实际需要的数据
    #     """
    #     return o
    #
    # def parse_int(self, o):
    #     """
    #     对整型解码
    #     :param o: 原始整型
    #     :return: 实际需要的数据
    #     """
    #     return o
    #
    # def parse_constant(self, o):
    #     """
    #     对于'-Infinity', 'Infinity', 'NaN'之类的特殊值进行解码
    #     :param o:
    #     :return:
    #     """
    #     return o
    #
    # def object_pairs_hook(self, o):
    #     """
    #     对有序列表解码，如果同时设置'object_hook'，'object_hook'将不生效
    #     :param o: 原始数据数据
    #     :return: 实际需要的数据
    #     """
    #     return o
