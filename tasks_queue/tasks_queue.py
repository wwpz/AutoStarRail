import threading
from queue import Queue, PriorityQueue
from utils.singleton import SingletonMeta
from collections import deque
import time

class TasksQueue(metaclass=SingletonMeta):
    def __init__(self):
        # 初始化优先级队列
        self.priority_queue = PriorityQueue()
        # 初始化FIFO队列
        self.fifo_queue = Queue()
        self.queue_lock = threading.Lock()
        self.queue = deque()  # 使用 deque 来实现任务队列

    # 用于将任务添加到优先级队列中
    def add_task(self, priority, task_func, *args, **kwargs):
        # 使用锁来确保线程安全
        with self.queue_lock:
            # 将任务函数、参数和优先级打包成一个元组，并放入优先级队列
            self.priority_queue.put((priority, (task_func, args, kwargs)))

    def add_task_fifo(self, task_func):
        """添加任务到队列末尾"""
        self.queue.append(task_func)  # 添加任务到队列

    # 用于从优先级队列中取出并执行任务
    def process_priority_tasks(self):
        while not self.priority_queue.empty():
            with self.queue_lock:
                if self.priority_queue.empty():
                    break
                # 从优先级队列中取出优先级最高的任务
                priority, (task_func, args, kwargs) = self.priority_queue.get()
            task_func(*args, **kwargs)  # 执行任务

    def process_fifo_tasks(self):
        """处理队列中的任务"""
        while self.queue:
            task_func = self.queue.popleft()  # 从队列头部取出任务
            task_func()  # 执行任务

    def execute_tasks(self):
        """执行队列中的所有任务，包括优先级和FIFO任务."""
        # self.process_priority_tasks()
        self.process_fifo_tasks()

    def is_empty(self):
        return len(self.queue) == 0  # 或者 return not self.queue