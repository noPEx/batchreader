from multiprocessing import Process
import os

class MyProcess(Process):

    def __init__(self, name):
        super(MyProcess, self).__init__()
        self.name = name

    def return_name(self):
        return "Process %s" % self.name

    def run(self):
        print 'MyProcess pid: %s'%(os.getpid())
        return self.return_name()


print 'main pid %s'%(os.getpid())
proc = MyProcess('child')
proc.start()
