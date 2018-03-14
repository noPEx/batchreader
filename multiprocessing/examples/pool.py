from multiprocessing import Pool
import os

def f(x):
    print "pid : %s x : %s"%(os.getpid(), x)
    return x*x


if __name__ == "__main__":
    po = Pool(5)
    print po.map(f, [1,2,3] )
