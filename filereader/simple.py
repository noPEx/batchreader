
import time
EACH_LINE_BYTE = 7
BATCHES = 1000
BATCH_SIZE = 100000

DATA_FILE = 'data_%s_%s.txt'%(BATCHES, BATCH_SIZE)
fp = open(DATA_FILE, 'r')


def countdown():
    #print 'ok '
    N = 1000*1000*10
    while N>0:
        N -= 1
    #print 'done '

class my_timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self): 
        self.start = time.time()
        self.end = None

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        print self.name, 'took ==> ',(self.end - self.start)

def reader():
    for i in range(BATCHES):
        #print i 
        fp.seek(i * BATCH_SIZE*EACH_LINE_BYTE)
        data = fp.read(BATCH_SIZE*EACH_LINE_BYTE)
        countdown()


with my_timer('plain'):
    reader()

