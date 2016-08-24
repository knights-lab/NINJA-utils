#!/usr/bin/env python
from subprocess import Popen, PIPE
import sys
import math
from timeit import default_timer as timer

def convertSize(size):
   if (size == 0):
       return '0B'
   size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '%s %s' % (s,size_name[i])

# This script prints the maximum memory usage in KB for a task
def timeit():
    p = Popen(['time', '-f', '%M'] + sys.argv[1:], stderr=PIPE)
    start_time = timer()
    ru_maxrss = int(p.communicate()[1])
    print("Time %d seconds" % timer() - star)
    print("Maximum rss %s" % convertSize(ru_maxrss))

if __name__ == '__main__':
    timeit()
