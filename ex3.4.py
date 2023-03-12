import threading
import random
import time

class CircularQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [None for i in range(size)]
        self.head = self.tail = -1
        self._lock = threading.Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def enqueue(self, data):
        while True:
            self.lock()
            if ((self.tail + 1) % self.size) != self.head:
                if self.head == -1:
                    self.head = 0
                self.tail = (self.tail + 1) % self.size
                self.queue[self.tail] = data
                self.unlock()
                return
            else:
                self.unlock()
                time.sleep(1)

    def dequeue(self):
        while True:
            self.lock()
            if self.head == -1:
                self.unlock()
                time.sleep(1)
            elif self.head == self.tail:
                data = self.queue[self.head]
                self.head = self.tail = -1
                self.unlock()
                return data
            else:
                data = self.queue[self.head]
                self.head = (self.head + 1) % self.size
                self.unlock()
                return data

def producer():
    while True:
        num = random.randint(1, 10)
        time.sleep(num)
        q.enqueue(num)

def consumer():
    while True:
        num = random.randint(1, 10)
        time.sleep(num)
        data = q.dequeue()
        print(f"Consumed: {data}")

if __name__ == '__main__':
    q = CircularQueue(5)
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
