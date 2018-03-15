import time
from multiprocessing import Pipe, Process, Condition
import threading

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
        self.queue = queue
        self.SHARED_QUEUE_SIZE_LIMIT = SHARED_QUEUE_SIZE_LIMIT
        self.condition = condition
        self.prod_end = prod_end

    def get_queue_size(self):
        return len(self.queue)

    def run(self):
        for i in range(BATCH_SIZE):
            self.condition.acquire()

            if self.get_queue_size(self) < 1:
                self.condition.wait()
                
            self.prod_end.send( self.queue.pop(0) )

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
        return data

    def _is_shared_queue_full(self):

        if self.pipe_out_thread.get_queue_size() >= self.SHARED_QUEUE_SIZE_LIMIT:
            return True
        else:
            return False
        
        

    def _preprocess_and_put_in_queue(self, data):

        self.condition.acquire()

        if self._is_shared_queue_full():
            self.condition.wait()

        self.batch_queue.append( data )
        self.condition.notify()
        self.condition.release()


        

    def _read_data(self, i):
        """
        self.fp.seek(0)
        data = self.fp.seek(i * BATCH_SIZE  *EACH_LINE_BYTE)
        """
        return "soumya"

    def run(self):
        for i in range(BATCHES):
            data = self._read_data(i)
            self._preprocess_and_put_in_queue(data)


class Consumer:
    
    def __init__(self, cons_end):
        self.cons_end = cons_end

    def train_model(self):
        N = 1000*1000*10
        while N>0:
            N -= 1

    def run(self):
        for i in range(BATCHES):
            batch_data = self.cons_end.recv()
            print 'consumer read at %s   ===  %s'%(i, batch_data)


def main():
    fname = '/home/soumya/training_samples/whiplash.mp4'
    condition = threading.Condition()
    SIZE = 1
    cons_end, prod_end = Pipe()
    consumer = Consumer(cons_end)
    producer = Producer(prod_end, fname, SIZE)
    consumer.run()
    producer.start()
    producer.join()

if __name__ == "__main__":
    with my_timer('synced_queue'):
        main()    

