#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET

def locateLinesInLog(filePath, timeStamp, preLines, postLines):
    lines = []
    file = open(filePath, "r+")
    for i in range(preLines):
        lines.append("")
    with open(filePath) as openfileobject:
        for line in openfileobject:
            if line.startswith(timeStamp):
                lines.append(line)
                break
            else:
                for i in range(preLines):
                    if i != 2:
                        lines[i] = lines[i+1]
                    else:
                        lines[2] = line
    for i in range(postLines):
        lines.append(file.readline())
    file.close()
    return lines
path = "D:Dropbox/SharedBachelor2016/TestData/xm3/Mcob02Ccpu.txt"
inStamp = "2016-02-22 09:36:08,378"
arr = locateLinesInLog(path, inStamp, 3, 3)
print arr
print len(arr)
