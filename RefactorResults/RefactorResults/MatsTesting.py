#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET


class TRXTest(object):
    innerTests = []
    def __init__(self, name, result, errorMessage, detailedFile):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage
        self.detailedFile = detailedFile

class InnerTest(object):
    innerTests = []
    def __init__(self, timestamp, detailedFile):
        self.timeStamp = timestamp
        self.detailedFile = detailedFile
    def calculateResult(self):
        result = "Passed"
        for subInner in self.innerTests:
            if subInner.result != "Passed":
                result = subInner.result
                break
        self.result = result

class SubInnerTest(object):
    def __init__(self, result, errorMessage, timeStamp):
        self.result = result
        self.errorMessage = errorMessage
        self.timeStamp = timestamp

path = "D:Dropbox/SharedBachelor2016/TestData/xmllog/HVC02 Query iteration parameters in iteration 1.xml"
def parseInnerTest():
    root = ET.parse(path)
    logfile = root.find("logFile").text
    timestamp = root.find("endtime").text

    xmlRoot = InnerTest(timestamp, logfile)

    #subInner = root.find("subinnertest")
    subInnerTests = []
    for subinnertest in root.iter("subinnertest"):
        result = subinnertest.find("result").text
        errorMessage = subinnertest.find("text").text
        timestamp = subinnertest.find("endtime").text
        temp = SubInnerTest(result,errorMessage,timestamp)
        subInnerTests.append(temp)

    xmlRoot.innerTests = subInnerTests
    xmlRoot.calculateResult()

#print root.find("subinnertest").find("text").text
#print root.find("subinnertest").find("text").text


for file in os.listdir("D:Dropbox/SharedBachelor2016/TestData/xmllog"):
    if file.endswith(".xml"):
        






"""
path = ""
path = "D:/Dropbox/Bachelor2016/In/20dc7a85-9275-4f2d-b84d-7c3568f0e9a9/NO-W-LMXMTH3/LoadNewSwUnitTestrack.xml.SwUpgradeTest Acu.txt"
#file = open(path, 'r+')
inStamp = "2015-11-17 05:17:28,717"


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

arr = locateLinesInLog(path, inStamp, 3, 3)
print arr
""" 