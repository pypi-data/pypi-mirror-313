# coding=utf8
from typing import List

from ..Base import AISerializeObject


class RunTraceE(AISerializeObject):
    def __init__(self, name_key):
        self.name_key = name_key
        self.input_data_torch = None
        self.out_data = None
        self.next_trace_list: List[RunTraceE] = []
        pass

    pass

