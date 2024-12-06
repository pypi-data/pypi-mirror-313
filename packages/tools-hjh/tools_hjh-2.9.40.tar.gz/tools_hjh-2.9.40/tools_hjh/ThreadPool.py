# coding:utf-8
from uuid import uuid1
from concurrent.futures import ThreadPoolExecutor, wait


def main():
    pass


class ThreadPool():
    """ 维护一个线程池 """
    
    def __init__(self, size):
        self.pool = ThreadPoolExecutor(max_workers=size)
        self.task_dict = {}
        
    def run(self, func, args=(), kwargs={}, name=None):
        id_ = uuid1()
        task = self.pool.submit(func, *args, **kwargs)
        self.task_dict[id_] = (name, task)
        return id_

    def get_results(self):
        self.wait()
        task_rs = {}
        for k, v in self.task_dict.items():
            task_rs[k] = v[1].result()
        return task_rs
    
    def get_result(self, id_):
        wait(self.task_dict[id_][1])
        return self.task_dict[id_][1].result()

    def wait(self):
        tasks = []
        for _, v in self.task_dict.items():
            tasks.append(v[1])
        wait(tasks)
    
    def get_running_num(self):
        running_tasks_num = 0
        for _, v in self.task_dict.items():
            if not v[1].done():
                running_tasks_num = running_tasks_num + 1
        return running_tasks_num
    
    def get_running_name(self):
        running_task_names = []
        for _, v in self.task_dict.items():
            if not v[1].done():
                running_task_names.append(v[0])
        return running_task_names


if __name__ == '__main__':
    main()
