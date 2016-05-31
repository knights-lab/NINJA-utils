#!/usr/bin/env python
from subprocess import Popen, PIPE
import sys

# This script prints the maximum memory usage in KB for a task

p = Popen(['time', '-f', '%M'] + sys.argv[1:], stderr=PIPE)
ru_maxrss = int(p.communicate()[1])
print("Maximum rss %d KB" % ru_maxrss)
