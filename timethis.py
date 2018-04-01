from time import time
from collections import defaultdict
from inspect import isfunction
import atexit, sys

#This is apparently bad practice; but should be ok in this particular case.
import __main__ 

total_time = defaultdict(lambda: 0)
timing = {}

def timethis(f):
    def wrap(*args, **kwargs):
        start = time()
        ret = f(*args)
        end = time()
        
        total_time[f.__name__ + "()"] += (end - start)

        return ret

    return wrap


def timefrom(id):
    if id in timing:
        raise SyntaxError("Missing timeto function for id: " + id)
    else:
        start = time()
        timing[id] = start
    
        
def timeto(id):
    if id not in timing:
        raise SyntaxError("Missing timefrom function for id: " + id)
    else:
        end = time()
        total_time[id] += (end - timing[id])
        del timing[id]

def autotime(namespace=__main__.builtins__.locals(), module_name='__main__'):
    for name, obj in namespace.items():
        if isfunction(obj) and obj.__module__ == module_name: 
            namespace[name] = timethis(namespace[name]) 
            
    

def report():
    if timing:
        ids = list(timing.keys()).__str__()
        raise SyntaxError("Missing timeto function for id: " + ids)

    header = "-----------------------------------\n"\
    + "|             Report              |\n"\
    + "-----------------------------------"
    rule = "-----------------------------------"
    
    print(header)
    for func in total_time.items():
        print("|{:20}|\t{:10.6f}|".format(func[0], func[1]))
    print(rule)

atexit.register(report)
