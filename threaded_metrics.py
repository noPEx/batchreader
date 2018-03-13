from threading import Thread
import threading
import time

class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print 'exit ::', (self.end - self.start)

class CountThread(Thread):

    def __init__(self, N, name):
        Thread.__init__(self)
        self.N = N
        self.name = name

    def run(self):
        print 'curr thread', threading.currentThread()
        with my_timer(self.name):
            while self.N>0:
                self.N -= 1

N = 100*100*1000
COUNT *= 10

th1 = CountThread(N, 'thread1')
#th1.start()
th1.run()
