#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 17:23
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .threads_main import MortalThreadsMain


class MortalThreads(MortalThreadsMain):
    def __init__(self, func, max_workers=None, maximum=False, logfile=False, logger=False, reserve=True):
        super().__init__(func, max_workers, maximum, logfile, logger, reserve)

    def send(self, thread_name: str = None, **kwargs):
        return self._send(thread_name, **kwargs)

    def join(self, break_result="mortal_break"):
        return self._join(break_result)

    def stop(self, thread_name):
        return self._stop(thread_name)

    def stop_all(self):
        return self._stop_all()

    def clear_queue(self):
        return self._clear_queue()

    def clear_record(self):
        return self._clear_record()

    def close(self):
        return self._close()

    def done(self):
        return self._done()

    def get_qsize(self):
        return self._get_qsize()

    def get_status(self, thread_name):
        return self._get_status(thread_name)

    def get_result(self, thread_name):
        return self._get_result(thread_name)

    def get_all_result(self):
        return self._get_all_result()

    def get_failed(self):
        return self._get_failed()

    def rerun_failed(self):
        return self._rerun_failed()

    def set_max_workers(self, workers_number=None):
        return self._set_max_workers(workers_number)

    def is_close(self):
        return self._is_close()

    def is_run(self):
        return self._is_run()
