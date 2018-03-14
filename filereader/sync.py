import threading
import time

#LINE_COUNT = 1000
EACH_LINE_BYTE = 7
BATCHES = 1000
BATCH_SIZE = 100000

DATA_FILE = 'data_%s_%s.txt'%( BATCHES, BATCH_SIZE)



def train_model():
    N = 1000*1000*10*3
    while N>0:
        N -= 1

class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print self.name, 'took ==> ',(self.end - self.start)

class ProducerThread(threading.Thread):

    def __init__(self, condition, queue):
        threading.Thread.__init__(self)
        self.condition = condition
        self.queue = queue
        self.fp = open(DATA_FILE,'r')

    def run(self):
        for i in range(BATCHES):
            self.fp.seek(0)
            self.fp.seek(i * BATCH_SIZE  *EACH_LINE_BYTE)
            lines = self.fp.read( BATCH_SIZE*EACH_LINE_BYTE)

            self.condition.acquire()

            if self.queue:
                #print 'prod:waiting to write for ', i
                self.condition.wait()
                #print 'woke up %s %s'%( i, '\n')

            self.queue.append(lines)
            #print 'Produced ', i

            self.condition.notify()
            self.condition.release()
        self.fp.close()
            

class ConsumerThread(threading.Thread):

    def __init__(self, condition, queue):
        threading.Thread.__init__(self)
        self.condition = condition
        self.queue = queue

    def run(self):
        for i in range(BATCHES):
            self.condition.acquire()
            if not self.queue:
                #print 'waiting for the queue to fill', i
                self.condition.wait()
                #print 'queue:consumer filled up',i

            batch_data = self.queue.pop(0)
            #print 'notifying ', i
            self.condition.notify()
            self.condition.release()
            #time.sleep(1)
            #print 'consumed %s %s'%(i, '\n')
            train_model()
            
            #time.sleep(1)
            #self.condition_item_consumed.release()



def main():
    queue = []
    condition = threading.Condition()
    consumer = ConsumerThread(condition, queue)
    producer = ProducerThread(condition, queue)
    consumer.start()
    producer.start()
    consumer.join()
    producer.join()

if __name__ == "__main__":
    with my_timer("main"):
        main()
