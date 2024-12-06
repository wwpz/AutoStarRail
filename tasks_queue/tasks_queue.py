import threading
from queue import Queue
from queue import PriorityQueue


class TasksQueue:
    def __init__(self):
        # 初始化FIFO队列
        self.task_queue = Queue()  # 使用FIFO队列
        # 初始化优先级队列
        self.task_queue = PriorityQueue()
        self.queue_lock = threading.Lock()

    # 用于将任务添加到队列中
    def add_task(self, priority, task_func, *args, **kwargs):
        # 使用锁来确保线程安全
        with self.queue_lock:
            # 将任务函数、参数和优先级打包成一个元组，并放入队列
            self.task_queue.put((priority, (task_func, args, kwargs)))

    # 用于将任务添加到队列中（FIFO顺序）
    def add_task_fifo(self, task_func, *args, **kwargs):
        # 将任务函数、参数打包成一个元组，并放入队列（没有优先级）
        self.task_queue.put((task_func, args, kwargs))

    # 用于从队列中取出并执行任务
    def process_tasks(self):
        while True:
            # 使用锁来确保线程安全（如果多个线程可能调用这个方法）
            with self.queue_lock:
                # 如果队列为空，则退出循环（或者你可以选择阻塞等待新任务）
                if self.task_queue.empty():
                    break
                # 从队列中取出优先级最高的任务
                priority, (task_func, args, kwargs) = self.task_queue.get()
            # 执行任务（这里不在锁的保护下，因为执行任务可能需要时间，并且不应该阻塞队列的访问）
            task_func(*args, **kwargs)
