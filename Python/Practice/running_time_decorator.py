#running time measurement decorator
import time

def running_time(myfunc):
    'Decorator for measuring the time it takes for the function to operate'
    def wrap(*args):
        t1=time.time()
        myfunc(*args)
        t2=time.time()
        return "Running time : " + '{:10.8f}'.format(t2-t1)+"sec\n"
    return wrap
