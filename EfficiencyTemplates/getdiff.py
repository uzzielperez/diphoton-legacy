import ROOT
import time
import subprocess
import os
import argparse
import re
from string import Template
import sys

parser = argparse.ArgumentParser(description="cmsDriver")
parser.add_argument("-a", "--filea", type=str, default="None")
parser.add_argument("-b", "--fileb", type=str, default="None")
args = parser.parse_args()

fo = open(args.filea, "rw+")
print "Name of filea: ", fo.name
linesa = fo.readlines()

fi = open(args.fileb, "rw+")
print "Name of fileb: ", fi.name
linesb = fi.readlines()

print "Nevents A: ", len(linesa)
print "Nevents B: ", len(linesb)
print "diff: ", len(list(set(linesa)-set(linesb)))

for event in list(set(linesa)-set(linesb)):
    print event[:-1]
# Close opend file
fo.close()
fi.close()
