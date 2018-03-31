from time import time
import atexit

total_time = {}

def timethis(f):
    def wrap(*args, **kwargs):
        start = time()
        ret = f(*args)
        end = time()
        if f.__name__ in total_time:
            total_time[f.__name__] += end - start
        else:
            total_time[f.__name__] = end - start
        return ret
    return wrap


def report():
    header = "-----------------------------------\n"\
    + "|             Report              |\n"\
    + "-----------------------------------"
    rule = "-----------------------------------"
    
    print(header)
    for func in total_time.items():
        print("|{:20}|\t{:10.6f}|".format(func[0], func[1]))
    print(rule)

atexit.register(report)
