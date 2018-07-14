import sys
import os

print "OS Home: %s" % os.environ['HOME']

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)