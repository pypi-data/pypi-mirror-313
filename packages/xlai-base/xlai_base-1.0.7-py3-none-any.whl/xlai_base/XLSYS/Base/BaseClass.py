# coding=utf8
import threading

'''
支持多线程的单例
'''


class SingletonArgs(object):

    def __init__(self, cls):
        self._instance_lock = threading.Lock()
        self._cls = cls
        self.uniqueInstance = None

    def __call__(self, **kwargs):
        if self.uniqueInstance is None:
            with self._instance_lock:
                if self.uniqueInstance is None:
                    self.uniqueInstance = self._cls(**kwargs)
        return self.uniqueInstance
