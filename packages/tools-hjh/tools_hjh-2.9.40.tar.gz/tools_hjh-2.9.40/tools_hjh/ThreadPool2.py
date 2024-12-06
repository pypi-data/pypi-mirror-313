# coding:utf-8
from uuid import uuid1
from concurrent.futures import ThreadPoolExecutor
import time


def main():
    pass


class ThreadPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, while_wait_time=0.1):
        self.tid_task = {}
        self.tid_status = {}
        self.tid_trs = {}
        self.tid_tname = {}
        self.size = size
        self.while_wait_time = while_wait_time
        self.pool = ThreadPoolExecutor(max_workers=self.size)
        
    def run_nowait(self, func, args, kwargs={}, name=None):
        thread_id = uuid1()
        task = self.pool.submit(func, *args, **kwargs)
        self.tid_task[thread_id] = task
        self.tid_tname[thread_id] = name
        return thread_id

    def run(self, func, args, kwargs={}, name=None):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        while self.get_running_num() >= self.size:
            time.sleep(self.while_wait_time)
        return self.run_nowait(func=func, args=args, kwargs=kwargs, name=name)

    def get_results(self):
        self.wait()
        return self.tid_trs
    
    def get_result(self, thread_id):
        self.get_results()
        return self.tid_trs[thread_id]

    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        for tid, task in self.tid_task.items():
            if tid not in self.tid_trs:
                self.tid_trs[tid] = task.result()
    
    def get_running_num(self):
        running_thread_ids = self.get_running_id()
        return len(running_thread_ids)
    
    def get_running_id(self):
        running_thread_ids = []
        for tid, task in self.tid_task.copy().items():
            if not task.done():
                running_thread_ids.append(tid)
        return running_thread_ids
    
    def get_running_name(self):
        running_names = []
        running_thread_ids = self.get_running_id()
        for tid in running_thread_ids:
            running_names.append(self.tid_tname[tid])
        return running_names
    
    def clear(self):
        self.tid_task = {}
        self.tid_status = {}
        self.tid_trs = {}
        self.tid_tname = {}


if __name__ == '__main__':
    main()
