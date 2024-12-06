# coding=utf8
import inspect
import json

from . import XLObjectUtil


class AISerializeObject(object):
    pass


class ObjectMangeBase(object):

    def __init__(self, name_key, cover_obj=False, **kwargs):
        self.name_key = name_key
        old_obj = XLObjectUtil.getObj(name_key, prn=False)
        if old_obj is not None and not cover_obj:
            old_obj_info = XLObjectUtil.getObjInfo(name_key)
            print(json.dumps(old_obj_info))
            raise Exception("{} 的 obj已经存在了".format(name_key))
        # 获取当前调用栈的帧
        stack = inspect.stack()
        obj_info = {
            'stack_info_list': ["{}--{}".format(stack[i].filename, stack[i].lineno) for i in range(1, len(stack)) if "XLAI" in stack[i].filename]
        }

        XLObjectUtil.updateObj(name_key, self, obj_info)
        pass

    pass
