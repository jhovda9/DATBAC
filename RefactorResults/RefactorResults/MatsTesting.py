#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET
import datetime
from re import split
import datetime
import timeit
#from time import strptime


def locateLinesInLog(filePath, timeStamp, preLines, postLines):
    lines = []
    file = open(filePath, "r+")
    time = datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S,%f")
    for i in range(preLines):
        lines.append("")
    while True:
        line = file.readline()
        if not line: 
            break
        try:
            if time <= datetime.datetime.strptime(line[0:23],"%Y-%m-%d %H:%M:%S,%f"):
                lines.append(line)
                break
        except ValueError:
            continue
        else:
            for i in range(preLines):
                if i != preLines-1:
                    lines[i] = lines[i+1]
                else:
                    lines[preLines - 1] = line
    for i in range(postLines):
        lines.append(file.readline())
    file.close()
    return lines

"""
Search algorithm based on Binary search
See https://hg.python.org/cpython/file/2.7/Lib/bisect.py
for original binary search code
"""
def locateLines2(filepath, timeStamp, preLines, postLines):
    fil = open(filepath, "r+")
    lines = fil.readlines()
    stamp = datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S,%f")
    lo = 0
    hi = len(lines)
    while lo < hi:
        mid = (hi + lo)/2
        try:
            currStamp = datetime.datetime.strptime(lines[mid][0:23],"%Y-%m-%d %H:%M:%S,%f")
        except ValueError:
            mid = mid - 1
            continue
        if currStamp < stamp:
            lo = mid+1
        else:
            hi = mid
    ret = []
    for i in range(preLines+1)[::-1]:
        if lo-i < 0:
            continue
        try:
            ret.append(lines[lo-i])
        except  :
            continue
    for i in range(postLines+1)[1:]:
        try:
            ret.append(lines[lo+i])
        except IndexError:
            continue
    return ret
"""
path = "D:TONSofTEST/acu.txt"
inStamp = "2016-02-22 09:34:08,211"
arr = locateLines2(path,inStamp,3,3)
for lin in arr:
    print lin
print len(arr)
"""

def locateBench():
    inStamp = "2016-02-22 09:36:21,765"
    path = "D:TONSofTEST"
    for file in os.listdir(path):
        if file.endswith(".txt"):
            locateLines2((path + "/" + file),inStamp, 3, 3)

print timeit.timeit(locateBench,number=100)
