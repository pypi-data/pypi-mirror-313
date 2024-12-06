# coding:utf-8
import time
from multiprocessing import Process


def main():
    pass


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, while_wait_time=0.1):
        self.size = size
        self.running_p = []
        self.p_pname = {}
        self.while_wait_time = while_wait_time

    def run_nowait(self, func, args, name=None): 
        p = Process(target=func, args=args)
        self.running_p.append(p)
        p.start()
        self.p_pname[p] = name
        return p.pid

    def run(self, func, args, name=None):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """     
        while self.get_running_num() >= self.size:
            time.sleep(self.while_wait_time)
        return self.run_nowait(func, args, name=name)
    
    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        for p in self.running_p:
            if p.is_alive():
                p.join()
        
    def get_running_num(self):
        running_num = 0
        for p in self.running_p.copy():
            if p.is_alive():
                running_num = running_num + 1
        return running_num
    
    def get_running_name(self):
        running_names = []
        for p in self.running_p:
            if p.is_alive():
                running_names.append(self.p_pname[p])
        return running_names
    

if __name__ == '__main__':
    main()
