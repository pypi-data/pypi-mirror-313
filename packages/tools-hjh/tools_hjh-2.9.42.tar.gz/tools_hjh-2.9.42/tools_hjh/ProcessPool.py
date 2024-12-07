# coding:utf-8
from multiprocessing import Pool
from uuid import uuid1
import time


def main():
    pass


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size):
        self.pool = Pool(processes=size)
        self.task_dict = {}

    def run(self, func, args=(), kwds={}, name=None, callback=None, error_callback=None):
        id_ = uuid1()
        task = self.pool.apply_async(func=func, args=args, kwds=kwds, callback=callback, error_callback=error_callback)
        self.task_dict[id_] = (name, task)
        return id_
    
    def wait(self):
        while self.get_running_num() > 0:
            time.sleep(0.1)
        
    def kill(self):
        self.pool.terminate()
        self.pool.join()
        
    def get_running_num(self):
        running_tasks_num = 0
        for _, v in self.task_dict.items():
            if not v[1].ready():
                running_tasks_num = running_tasks_num + 1
        return running_tasks_num
    
    def get_running_name(self):
        running_task_names = []
        for _, v in self.task_dict.items():
            if not v[1].ready():
                running_task_names.append(v[0])
        return running_task_names
    

if __name__ == '__main__':
    main()
