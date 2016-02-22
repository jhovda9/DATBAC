#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET


class TRXTest(object):
    innerTests = []
    def __init__(self, name, result, errorMessage):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage

class InnerTest(object):
    innerTests = []
    startTime = ""
    endTime = ""
    duration = ""
    detailedFile = ""
    def __init__(self, name):
        self.name = name

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
        self.timeStamp = timeStamp
"""
def createTestObject():
    detailedResultsFile = "No file exists"
    if testElement.find("DetailedResultsFile") != None:
        detailedResultsFile = testElement.find("DetailedResultsFile").text
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text, testElement.find("ErrorMessage").text,
                      detailedResultsFile)
    return testObject
"""

def initializeTRXStructure(path):
    testElement = ET.parse(path)
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text, testElement.find("ErrorMessage").text)
    for innerTest in testElement.find("InnerTests").iter("InnerTest"):
        testObject.innerTests.append(InnerTest(innerTest.find("TestName").text))
    return testObject

#path = "D:Dropbox/SharedBachelor2016/TestData/xmllog/HVC02 Query iteration parameters in iteration 1.xml"
pathTRX = "D:Dropbox/SharedBachelor2016/TestData/xm3/NASTLauncherResult.trx"
durr = initializeTRXStructure(pathTRX)

def parseInnerTest(trxTest, outdir):
    
    for innertest in trxTest.innerTests:
        root = ET.parse(os.path.join(outdir,innertest.name + ".xml"))

        innertest.logfile = root.find("logfile").text
        innertest.startTime = root.find("starttime").text
        innertest.endTime = root.find("endtime").text
        innertest.duration = root.find("duration").text

        subInnerTests = []
        for subinnertest in root.iter("subinnertest"):
            result = subinnertest.find("result").text
            errorMessage = subinnertest.find("text").text
            timestamp = subinnertest.find("endtime").text
            temp = SubInnerTest(result,errorMessage,timestamp)
            subInnerTests.append(temp)

parseInnerTest(durr, "D:Dropbox/SharedBachelor2016/TestData/xm3")
#tingen = parseInnerTest(path)
#print tingen.duration
#print tingen.innerTests[0].errorMessage

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