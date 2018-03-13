import random
import threading
from threading import Thread


LINE_COUNT = 1000
EACH_LINE_BYTE = 7
BATCHES = 10
BATCH_SIZE = 100


class BatchReaderThread(Thread):
    def __init__(self, condition, name, fp, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.fp = fp
        self.condition = condition
        self.batch_data = None

    def get_data(self):
        return self.batch_data
        

    def run(self):
        self.batch_data = self.fp.read(start, end-start)
        
        

lock = threading.RLock()
class DataItem:

    def __init__(self):
        self.data_available = False

class Producer:

    def __init__(self, condition, filename, epochs):
        self.condition = condition
        self.fp = open(filename,'r')
        self.epochs = epochs
        self.line_count = LINE_COUNT
        self.current_order = [i for i in range(LINE_COUNT)]
        self.newline_offset = [i for i in range(LINE_COUNT)]
        self.previous_batch_data = f.read(EACH_LINE_BYTE)
        self.next_batch_data = None
        self.data_available = True
        self.rth = None

    def get_reader_thread(self):
        return self.rth

    def get_data(self, start, end):
        self.condition.acquire()

        self.data_available = False
        self.rth  = BatchReaderThread(condition, "off_%s_%s"%(start,end), self.fp, start*BATCH_SIZE, end*BATCH_SIZE)
        self.rth.start()
        return self.previous_batch_data

        #read into next
        
       

class Consumer:

    def __init__(self, condition):
        self.condition
        self.producer = Producer( 'data.txt', 1)
        self.N = 100*100*1000

    def countdown(self, N):
        print 'here'
        while N>0:
            N -= 1

    def run(self):
        for i in range(BATCHES):
            self.condition.acquire()

            if not self.producer.data_available:
                prin 'consumer is waiting for data'
                self.condition.wait()

            
            batch_data = self.producer.get_data(i*BATCH_SIZE, i*BATCH_SIZE + BATCH_SIZE)

            self.producer.data_available = False


def main():
    condition = threading.Condition()
    consumer = Consumer(condition, 'data.txt', 1)
    #producer = Producer(condition, 'data.txt', 1)
if __name__ == "__main__":
    main()
