# coding=utf8
import copy
from datetime import datetime

from ...Department import BaseDPart


class XLCGlobalInfo(object):
    def __init__(self, context_id, up_globalInfo: dict):
        if up_globalInfo is None or up_globalInfo.get('all_trace_id') is None:
            self.all_trace_id = []
        else:
            self.all_trace_id = copy.deepcopy(up_globalInfo['all_trace_id'])

        self.all_trace_id.append(context_id)
        pass

    def to_dict(self):
        return {
            'all_trace_id': self.all_trace_id
        }


class XLContext(object):
    def __init__(self, department: BaseDPart, part, up_globalInfo: dict):
        department_name = department.name.lower()
        self.context_id = datetime.now().strftime("{}-{}-%Y%m%d_%H%M%S_%f".format(department_name, part))
        self.global_info = XLCGlobalInfo(context_id=self.context_id, up_globalInfo=up_globalInfo)
        self.run_data_pool = {}
        self.run_trace_list = []
        pass

    pass


pass
