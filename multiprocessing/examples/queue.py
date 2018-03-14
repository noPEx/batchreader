from multiprocessing import Process, Queue
import os

def f(q):
    q.put(42)
    q.put([1,2])
    print 'process pid %s'%(os.getpid())
    


if __name__ == "__main__":
    print 'parent pid %s'%(os.getpid())
    q = Queue()
    p = Process(target = f, args=(q,))
    p.start()
    print q.get()
    p.join()
