import sys
import re
from collections import namedtuple

input_fs = sys.argv[1]
assert len(input_fs) > 0, 'no input file specified'
print input_file
input_file = open(input_fs, 'r+')

cat_line = input_file.readline()
print cat_line
cats = re.split('[\\t+]', cat_line)
# print cats
print cats[0]

for line in input_file:
   cats = re.split('[\\t+]', line)
   # print cats
   print cats[0]


# cat_line = f.readline()
# print cat_line
# cats = re.split('[\\t+]', cat_line)
# print cats