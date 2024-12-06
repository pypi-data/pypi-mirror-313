# coding=utf8
from pydantic import BaseModel

from ..Base import AISerializeObject


class XLLinkDM(BaseModel):
    key: str
    data_type: str


class XLDM(AISerializeObject):
    def __init__(self, key, data_type, des=None):
        # 类型
        self.data_type = data_type
        # key
        self.key = key
        # 描述
        self.des = key if des is None else des

    def __str__(self):
        return '<{}><{}>'.format(self.key, self.data_type)
        pass

    def toLinkDM(self):
        return {
            'key': self.key,
            'data_type': self.data_type
        }
        pass


class XLDataMarkUtil(object):

    @staticmethod
    def keyDataBuild(key, data_type) -> XLDM:
        entity: XLDM = XLDM(key=key, data_type=data_type)
        entity.association_chain = [0, []]
        entity.create_identity = 0
        return entity
        pass


    @staticmethod
    def list2DictByKey(data_list: list) -> dict:
        data_dict = {}
        for d in data_list:
            data_dict[d.key] = d
        return data_dict
        pass


pass
