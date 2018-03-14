import threading

LINE_COUNT = 1000
EACH_LINE_BYTE = 7
BATCHES = 1000
BATCH_SIZE = 100000

DATA_FILE = 'data_%s_%s.txt'%( BATCHES, BATCH_SIZE)



def countdown():
    N = 1000*1000*10
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

    def __init__(self, condition, queue, condition_item_consumed):
        threading.Thread.__init__(self)
        self.condition = condition
        self.queue = queue
        self.condition_item_consumed = condition_item_consumed
        self.fp = open(DATA_FILE,'r')

    def run(self):
        for i in range(BATCHES):
            self.condition.acquire()

            #print 'i ',i
            self.fp.seek(i * BATCH_SIZE  *EACH_LINE_BYTE)
            lines = self.fp.read( BATCH_SIZE*EACH_LINE_BYTE)

            """
            if self.queue:
                #print 'waiting for item to get consumed'
                self.condition_item_consumed.wait()
                #print 'item consumed. now go and write'
            """
            if self.queue:
                #print 'waiting to write for ', i
                self.condition.wait()

            self.queue.append(lines)
            #print 'Produced ', i
            self.condition.notify()
            self.condition.release()
        self.fp.close()
            

import time
class ConsumerThread(threading.Thread):

    def __init__(self, condition, queue, condition_item_consumed):
        threading.Thread.__init__(self)
        self.condition = condition
        self.queue = queue
        self.condition_item_consumed = condition_item_consumed

    def run(self):
        for i in range(BATCHES):
            self.condition.acquire()
            if not self.queue:
                #print 'waiting for the queue to fill', i
                self.condition.wait()
                #print 'queue:consumer filled up',i

            batch_data = self.queue.pop(0)
            #print 'consumed ', i
            countdown()
            self.condition.notify()
            self.condition.release()
            
            #time.sleep(1)
            #self.condition_item_consumed.release()



def main():
    queue = []
    condition = threading.Condition()
    condition_item_consumed = threading.Condition()
    consumer = ConsumerThread(condition, queue, condition_item_consumed)
    producer = ProducerThread(condition, queue, condition_item_consumed)
    consumer.start()
    producer.start()
    consumer.join()
    producer.join()

if __name__ == "__main__":
    with my_timer("main"):
        main()
