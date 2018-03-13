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
        print self.name, 'took ==> ',(self.end - self.start)

class CountThread(Thread):

    def __init__(self, N, name):
        Thread.__init__(self)
        self.N = N
        self.name = name

    def run(self):
        print 'curr thread', threading.currentThread()
        while self.N>0:
            self.N -= 1


def one_thread_only(N):
    print '1 thread working'
    name = 'one_thread_only' 
    with my_timer(name):
        th1 = CountThread(N, name)
        th1.start()
        th1.join()

def one_func_only(N):
    print 'main thread function only'
    name = 'one_func_only' 
    with my_timer(name):
        th1 = CountThread(N, 'one_func_only')
        th1.run()
    

def use_two_thread(N):
    print '2 threads each counting half'
    name = 'use_two_thread'
    N = N/2

    with my_timer(name):
    
        th1 = CountThread(N, 'use_two_thread_1')
        th2 = CountThread(N, 'use_two_thread_2')
        th1.start()
        th2.start()
        th1.join()
        th2.join()

def use_two_func(N):
    print 'main thread call two functions each counting half'
    name = 'use_two_func'

    N = N/2
    with my_timer(name):
    
        th1 = CountThread(N, 'thread1')
        th2 = CountThread(N, 'thread2')
        th1.run()
        th2.run()

def use_four_thread(N):
    print '4 thread workers counting 1/4th'
    name = 'use_four_thread'

    N = N/4
    with my_timer(name):
        th1 = CountThread(N, 'thread1')
        th2 = CountThread(N, 'thread2')
        th3 = CountThread(N, 'thread3')
        th4 = CountThread(N, 'thread4')
        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th1.join()
        th2.join()
        th3.join()
        th4.join()




def main():

    N = 100*100*1000*10

    one_thread_only(N) 
    print '\n\n'
    one_func_only(N)
    print '\n\n'
    use_two_thread(N) 
    print '\n\n'
    use_two_func(N)
    print '\n\n'
    use_four_thread(N)
    



if __name__ == "__main__":
    main()




