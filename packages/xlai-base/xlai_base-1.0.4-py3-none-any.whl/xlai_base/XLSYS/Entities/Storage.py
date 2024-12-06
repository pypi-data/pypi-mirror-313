# coding=utf8
from datetime import datetime

class XLContext(object):
    def __init__(self,department, part, event):
        self.context_id = datetime.now().strftime("{}-{}}-%Y%m%d_%H%M%S_%f".format(department, part))
        self.event = event
        self.run_data_pool = {}
        self.run_trace_list = []
        pass

    pass

pass
