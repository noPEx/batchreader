
import time
def countdown():
    #print 'ok '
    N = 1000*1000*10*10
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


with my_timer('plain'):
    countdown()
