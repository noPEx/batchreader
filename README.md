experiments on python multhreading/gil/throughput when using threads etc

Here is a talk on GIL by the creator of PLY(Python Lex/Yacc)
   - www.dabeaz.com/python/UnderstandingGIL.pdf
   - video for talk : https://www.youtube.com/watch?v=ph374fJqFPE

### code examples

threaded_metrics.py -> does the same computation in main thread, new thread, two threads, 4 threads and compares time taken.

###filereader/

    simple.py -> does a i/o intensive computation for a producer/consumer setup in main thread
    sync.py   -> does i/o intensive computation using multithreaded producer/consumer paradim using condition variables for synchronization 
    datacreator.py -> creates input data for the above two codes
    countdown.py -> timed program for a countdown function for given large number N
