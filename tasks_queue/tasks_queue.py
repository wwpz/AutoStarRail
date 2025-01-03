import threading

from log import log
from queue import Queue, PriorityQueue
from utils.singleton import SingletonMeta
from collections import deque


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

    def add_task_fifo(self, task_func, task_id=None):
        """添加任务到队列末尾，并给任务一个可选的标识"""
        self.queue.append((task_id, task_func))

    def remove_task_fifo(self, task_id):
        """根据任务标识从队列中移除任务"""
        with self.queue_lock:
            self.queue = deque(task for task in self.queue if task[0] != task_id)

    def process_priority_tasks(self):
        while not self.priority_queue.empty():
            with self.queue_lock:
                if self.priority_queue.empty():
                    break
                # 从优先级队列中取出优先级最高的任务
                priority, (task_func, args, kwargs) = self.priority_queue.get()
            task_func(*args, **kwargs)

    def process_fifo_tasks(self):
        """处理队列中的任务"""
        while self.queue:
            task_id, task_func = self.queue.popleft()
            log.debug(f"正在执行任务 ID: {task_id}")
            print(self.queue_len())
            task_func()
            self.after_task_execution(task_id)


    def after_task_execution(self,task_id):
        log.debug(f"任务 {task_id} 执行完毕，执行后续操作...")
        # if task_id == "hzh_signin":
        #     cfg.set_value("hzh_signin",False)

    def execute_tasks(self):
        """执行队列中的所有任务，包括优先级和FIFO任务."""
        # self.process_priority_tasks()
        self.process_fifo_tasks()

    def queue_len(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0  # 或者 return not self.queue
