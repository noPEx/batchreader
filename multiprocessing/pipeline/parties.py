import time
from multiprocessing import Pipe, Process

EACH_LINE_BYTE = 7
BATCHES = 1000
BATCH_SIZE = 100000

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


#runs in parent process
class Producer(Process):

    def __init__(self, prod_end):
        super(Producer, self).__init__()
        self.fp = open(DATA_FILE, 'r')
        self.prod_end = prod_end

    def run(self):
        for i in range(BATCHES):
            #print 'write ',i
            self.fp.seek(0)
            self.fp.seek(i * BATCH_SIZE  *EACH_LINE_BYTE)
            lines = self.fp.read( BATCH_SIZE*EACH_LINE_BYTE)
            #print 'compl ', i
            self.prod_end.send(lines)
            #print 'sent ',i
            ack = self.prod_end.recv()
            #print ack
        self.fp.close()
        self.prod_end.close()

class Consumer:

    def __init__(self, cons_end):
        self.cons_end = cons_end

    def train_model(self):
        N = 1000*1000*10
        while N>0:
            N -= 1

    def run(self):
        for i in range(BATCHES):
            #print i
            batch_data = self.cons_end.recv()
            #print 'len recv : %s'%( len(batch_data))
            self.cons_end.send('ack : %s'%(i))
            self.train_model()


def main():
    prod_end, cons_end = Pipe()

    pr = Producer(prod_end)
    csr = Consumer(cons_end)
    pr.start()
    csr.run()
    pr.join()
    
    

if __name__ == "__main__":
    with my_timer('producer-consumer'):
        main()

            
