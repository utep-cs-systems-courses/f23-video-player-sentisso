from typing import List, Generic, TypeVar
import threading

T = TypeVar('T')


class Queue(Generic[T]):
    def __init__(self, max_size=10):
        self.queue: List[T] = []
        self.lock = threading.Lock()
        self.max_size = max_size
        # number of empty spaces in the queue
        self.to_full = threading.Semaphore(self.max_size)
        # number of items in the queue
        self.to_empty = threading.Semaphore(0)

    def insert(self, item: T):
        self.to_full.acquire()  # block until to_full is greater than 0, then -= 1
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.to_empty.release()

    def remove(self):
        self.to_empty.acquire()  # block until to_empty is greater than 0, then -= 1
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        self.to_full.release()
        return item
