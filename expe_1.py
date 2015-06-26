# coding=utf-8
from edit_distance import sequence_alignemt, get_sequence
from util import memory_usage

from util import plot
import numpy as np
import resource
import random
import time
import gc

z = "ABCD"
g = 0.7
a = 1
gc.disable()


def task2():
    gc.collect()
    result = [[],[],[]]
    for i in range(11):
        size = 10*pow(2, i)
    
        # Getting currante memory usage
        start_mem = memory_usage()
        for j in range(10):
            # Releasing unused memory
            gc.collect()
            # Getting current time
            start_time = time.clock()
            # Chain generation
            x = "".join([random.choice(z) for _ in range(size)])
            y = "".join([random.choice(z) for _ in range(size)])

            # Sequence Alignment
            M, cost = sequence_alignemt(x, y, g, a)
            out_x, out_y = get_sequence(x, y, g, a, M)

            elapsed = (time.clock() - start_time)/60
            used_men = memory_usage() - start_mem
            
            # Saves chain size
            result[0].append(size)
            # Saves time
            result[1].append(elapsed)
            # Saves consumed memory
            result[2].append(used_men)
            
            print "i = %d, j = %d\nElapsed Time: %.3f mins\nUsed memory: %.3f MB" % (i, j, elapsed, used_men)

            # Releasing unused memory
            del x, y, M, out_x, out_y
            gc.collect()
            if elapsed > 15:
                return result
    return result


if __name__ == '__main__':
    result = task2()
    plot(result)

