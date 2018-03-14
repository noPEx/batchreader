from multiprocessing import Process, Queue, Condition
import os
import time

EACH_LINE_BYTE = 7
BATCHES = 100
BATCH_SIZE = 10000

DATA_FILE = 'data_%s_%s.txt'%( BATCHES, BATCH_SIZE)


class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print self.name, 'took ==> ',(self.end - self.start)

class Producer(Process):

    def __init__(self, name, queue, condition):
        super(Producer, self).__init__()
        self.name = name
        self.queue = queue
        self.condition = condition
        self.fp = open(DATA_FILE, 'r')

    def run(self):
        print 'producer running with pid : %s'%(os.getpid())
        for i in range(BATCHES):
            self.fp.seek(0)
            self.fp.seek(i * BATCH_SIZE  *EACH_LINE_BYTE)
            lines = self.fp.read( BATCH_SIZE*EACH_LINE_BYTE)

            self.condition.acquire()

            if not self.queue.empty() or self.queue.qsize() == 1 :
                #print 'prod:waiting to write for ', i
                self.condition.wait()
                #print 'woke up %s %s'%( i, '\n')

            self.queue.put(lines)
            #print 'Produced ', i

            self.condition.notify()
            self.condition.release()
            #print 'released ', i
        self.fp.close()


class Consumer(Process):

    def __init__(self, name, queue, condition):
        super(Consumer , self).__init__()
        self.name = name
        self.queue = queue
        self.condition = condition

    def train_model(self):
        N = 1000*1000*10*3
        while N>0:
            N -= 1



    def run(self):
        print 'consumer running with pid : %s'%(os.getpid())
        for i in range(BATCHES):
            self.condition.acquire()
            if self.queue.empty():
                #print 'waiting for the queue to fill', i
                self.condition.wait()
                #print 'queue:consumer filled up',i

            batch_data = self.queue.get()
            #print 'notifying ', i
            self.condition.notify()
            self.condition.release()
            #time.sleep(1)
            #print 'consumed %s %s'%(i, '\n')
            self.train_model()
            
            #time.sleep(1)
            #self.condition_item_consumed.release()



def main():

    queue = Queue()
    condition = Condition()
    prod = Producer('prod', queue, condition)
    cons = Consumer('cons', queue, condition)

    prod.start()
    cons.start()
    prod.join()
    cons.join()


if __name__ == "__main__":
    with my_timer('timer'):
        main()
