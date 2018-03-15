import time
from multiprocessing import Pipe, Process, Condition
import threading
import random

FILENAME='/home/soumya/training_samples/whiplash_x_10.mp4'

KB = 1024
MB = KB*KB
GB = KB*MB

BATCHES = 10

class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print self.name, 'took ==> ',(self.end - self.start)


class PipeOutThread(threading.Thread):

    def __init__(self, prod_end, condition, SHARED_QUEUE_SIZE_LIMIT, queue):
        super(PipeOutThread, self).__init__()
        self.queue = queue
        self.SHARED_QUEUE_SIZE_LIMIT = SHARED_QUEUE_SIZE_LIMIT
        self.condition = condition
        self.prod_end = prod_end

    def get_queue_size(self):
        return len(self.queue)

    def run(self):
        for i in range(BATCHES):
            self.condition.acquire()

            if self.get_queue_size() < 1:
                print 'pipe:Thread is waiting'
                self.condition.wait()
                print 'just woke up buddy'
                
            print 'popping on len: %s'%(len(self.queue))
            self.prod_end.send( self.queue.pop(0) )
            
            #self.prod_end.send( self.queue[0] )

            self.condition.notify()
            self.condition.release()

        


class Producer(Process):

    def __init__(self, prod_end, fname, SHARED_QUEUE_SIZE_LIMIT):
        super(Producer, self).__init__()
        self.prod_end = prod_end
        self.fp = open(fname,'r')
        self.SHARED_QUEUE_SIZE_LIMIT = SHARED_QUEUE_SIZE_LIMIT
        self.batch_queue = []
        self.condition = Condition()
        self.pipe_out_thread = PipeOutThread( prod_end, self.condition, self.SHARED_QUEUE_SIZE_LIMIT, self.batch_queue)
        

    def _preprocess(self, data):
        N = 1000*1000*10*3
        while N>0:
            N -= 1
        return data

    def _is_shared_queue_full(self):

        if self.pipe_out_thread.get_queue_size() >= self.SHARED_QUEUE_SIZE_LIMIT:
            return True
        else:
            return False
        
        

    def _preprocess_and_put_in_queue(self, data):

        self.condition.acquire()

        print 'prod acquired'
        if self._is_shared_queue_full():
            print 'prod: queue is full so waiting'
            self.condition.wait()

        self.batch_queue.append( data )
        print 'self.batch_queue', len(self.batch_queue)
        self.condition.notify()
        self.condition.release()


        

    def _read_data(self, i, dummy=False):
        if dummy:
            return 'soumya' 
        else:
            data = None
            with my_timer('freader: %s'%(i)):
                offset = random.randint(5,16)*GB
                print 'offset is : ' , offset/GB
                self.fp.seek(offset)
                data = self.fp.read(GB)
                print 'len_data ', len(data)
            return data 

    def run(self):
        self.pipe_out_thread.start()
        for i in range(BATCHES):
            data = self._read_data(i)
            self._preprocess_and_put_in_queue(data)
            print 'prod put %s'%(i)
        self.pipe_out_thread.join()
        print 'done with processor'


class Consumer:
    
    def __init__(self, cons_end):
        self.cons_end = cons_end

    def train_model(self):
        N = 1000*1000*10
        while N>0:
            N -= 1

    def run(self):
        for i in range(BATCHES):
            print 'consumer waiting'
            batch_data = self.cons_end.recv()
            print 'consumer read at %s   with size===  %s'%(i, len(batch_data))
        print 'done in consumer'


def main():
    condition = threading.Condition()
    SIZE = 3 
    cons_end, prod_end = Pipe()
    consumer = Consumer(cons_end)
    producer = Producer(prod_end, FILENAME, SIZE)
    producer.start()
    consumer.run()
    producer.join()

if __name__ == "__main__":
    with my_timer('synced_queue'):
        main()    

