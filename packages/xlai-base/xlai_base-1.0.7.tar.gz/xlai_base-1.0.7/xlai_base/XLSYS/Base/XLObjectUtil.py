# coding=utf8

__OBJECT_POOL = {}
__OBJECT_INFO_DICT = {}


def getObj(name_key, prn=True):
    _obj = __OBJECT_POOL.get(name_key)
    if prn and _obj is None:
        print('getObj 为空: ',name_key)
    return _obj
    pass


def getObjInfo(name_key) -> dict:
    return __OBJECT_INFO_DICT.get(name_key)
    pass


def updateObj(name_key, obj, info={}):
    __OBJECT_POOL[name_key] = obj
    __OBJECT_INFO_DICT[name_key] = info
    pass





