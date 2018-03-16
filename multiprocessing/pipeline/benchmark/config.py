import os

FILENAME='/home/soumya/training_samples/whiplash_x_10.mp4'
SIZE = 3 


KB = 1024
MB = KB*KB
GB = KB*MB

NUM_BATCHES = 10
CHUNK_SIZE_TO_READ = int(GB/2)
SHARED_QUEUE_SIZE_LIMIT = 3

COUNTER_PRODUCER = 10**7 * 3
COUNTER_CONSUMER = 10**7 * 3

class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print self.name, 'took ==> ',(self.end - self.start)


def countdown_producer():
    N = COUNTER_PRODUCER
    while N>0 :
        N -= 1
    
def countdown_consumer():
    N = COUNTER_CONSUMER
    while N>0 :
        N -= 1


def get_offset_array(fname, batches):
    size_in_bytes = os.path.getsize(fname)
    offset_array = []
    
    each_size = size_in_bytes/batches

    for i in batches:
        offset_array.append(i*each_size)
    offset_array.append(size_in_bytes)

    return offset_array
