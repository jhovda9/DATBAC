#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET
import datetime
from re import split
import datetime
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


path = "D:Dropbox/SharedBachelor2016/TestData/xm3/Mcob02Ccpu.txt"
inStamp = "2016-02-22 09:36:21,765"
arr = locateLinesInLog(path, inStamp, 3, 3)
for lin in arr:
    print lin
print len(arr)
