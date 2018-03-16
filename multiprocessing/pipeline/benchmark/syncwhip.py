import time
from multiprocessing import Pipe, Process, Condition
import threading
import random

FILENAME='/home/soumya/training_samples/whiplash_x_10.mp4'
SIZE = 3 


KB = 1024
MB = KB*KB
GB = KB*MB

BATCHES = 10
CHUNK_SIZE_TO_READ = int(GB/2)


class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print self.name, 'took ==> ',(self.end - self.start)



class Producer():

    def __init__(self, fname):
        self.fp = open(fname,'r')
        self.batch_queue = []

    def _preprocess(self, data):
        N = 1000*1000*10*3
        while N>0:
            N -= 1
        return data

    def _preprocess_and_put_in_queue(self, data):

        self.batch_queue.append( self._preprocess(data) )
        #print 'self.batch_queue', len(self.batch_queue), self.batch_queue


        

    def _read_data(self,dummy=False):
        if dummy:
            return 'soumya' 
        else:
            offset = random.randint(5,16)*GB
            #print 'offset is : ' , offset/GB
            self.fp.seek(offset)
            data = self.fp.read(CHUNK_SIZE_TO_READ)
            #print 'length ', len(data)/KB
            return data

    def run(self):
        data = self._read_data()
        self._preprocess_and_put_in_queue(data)
        return self.batch_queue.pop(0)
        


class Consumer:
    
    def __init__(self):
        self.producer = Producer(FILENAME)

    def train_model(self):
        N = 1000*1000*10*3
        while N>0:
            N -= 1

    def run(self):
        for i in range(BATCHES):
            #print 'consumer waiting'
            batch_data = self.producer.run()
            self.train_model()
            #print 'consumer read at %s   with size===  %s'%(i, len(batch_data))
        #print 'done in consumer'


def main():
    consumer = Consumer()
    consumer.run()

if __name__ == "__main__":
    with my_timer('synced_queue'):
        main()    

