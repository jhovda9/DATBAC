#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET

"""path = ""
path = "D:/Dropbox/Bachelor2016/In/20dc7a85-9275-4f2d-b84d-7c3568f0e9a9/NO-W-LMXMTH3/LoadNewSwUnitTestrack.xml.SwUpgradeTest Acu.txt"
#file = open(path, 'r+')
inStamp = "2015-11-17 05:17:28,717"
"""

def locateLinesInLog(filePath, timeStamp, preLines, postLines):
    lines = []
    file = open(filePath, "r+")
    stamp_found = False
    for i in range(preLines):
        lines.append("")
    while not stamp_found:
        line = file.readline()
        if line.startswith(timeStamp):
            stamp_found = True
            lines.append(line)
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
"""
arr = locateLinesInLog(path, inStamp, 3, 3)
print arr
"""