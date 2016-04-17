#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET
import RefactorResults
import datetime
from re import split
import datetime
import timeit
import Tkinter as TK
#from time import strptime

filepath = "D:Desktop/NASTLauncherResult.trx"


def initializeTRXStructure(path):
    testElement = ET.parse(path)
    testObject = RefactorResults.TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text,
                         testElement.find("ErrorMessage").text)
    for innerTest in testElement.find("InnerTests").iter("InnerTest"):
        testObject.innerTests.append(RefactorResults.InnerTest(innerTest.find("TestName").text, innerTest.find("TestResult").text,
                                               innerTest.find("ErrorMessage").text,
                                               innerTest.find("DetailedResultsFile").text))
    return testObject

def parseInnerTest(trxTest, outdir):
    
    for inner in trxTest.innerTests:
        root = ET.parse(os.path.join(outdir, inner.detailedFile))
        inner.logfile = root.find("logfile").text
        inner.startTime = root.find("starttime").text
        inner.endTime = root.find("endtime").text
        inner.duration = root.find("duration").text
        for subinnertest in root.findall("subinnertest"):
            inner.subInnerTests.append(SubInnerTest(subinnertest.find("result").text, subinnertest.find("text").text,
                                                    subinnertest.find("endtime").text))


#Alternativ:
def initstructsafe(path):
    testElement = ET.parse(path)
    name = ""
    result = ""
    errorMessage = ""
    innertestRoot = None
    for elem in testElement.findall("*"):
        tag = elem.tag.lower()
        if tag == "testname" or tag == "name":
            name = elem.text
        elif tag == "testresult" or tag == "result":
            result = elem.text
        elif tag == "errormessage":
            errorMessage = elem.text
        elif tag == "innertests" or tag == "subtests" or tag == "tests":
            innertestsRoot = elem
    trxTest = RefactorResults.TRXTest(name, result, errorMessage)

    for innertest in innertestsRoot.findall('*'):
        name = ""
        result = ""
        errorMessage = ""
        detailedResultsFile = ""
        for elem in innertest.findall("*"):
            tag = elem.tag.lower()
            if tag == "testname" or tag == "name":
                name = elem.text
            elif tag == "testresult" or tag == "result":
                result = elem.text
            elif tag == "errormessage":
                errorMessage = elem.text
            elif tag == "detailedresultsfile" or tag == "resultsfile" or tag == "file" or tag == "detailedfile":
                detailedResultsFile = elem.text
        inner = RefactorResults.InnerTest(name, result, errorMessage, detailedResultsFile)
        trxTest.innerTests.append(inner)
    return trxTest


#Alternative for sub-inner tests
def createSubInnerTests(trxTest, outDir):
    for innerTest in trxTest.innerTests:
        logFile = ""
        startTime = ""
        endTime = ""
        duration = ""
        subInnerTests = []
        root = ET.parse(os.path.join(outDir, innerTest.detailedFile))
        for elem in root.findall('*'):
            tag = elem.tag.lower()
            if tag == "logfile" or tag == "log" or tag == "file":
                logFile = elem.text
            elif tag == "starttime" or tag == "start":
                startTime == elem.text
            elif tag == "endtime" or tag == "end" or tag == "stop":
                endTime = elem.text
            elif tag == "duration":
                duration = elem.text
            elif tag == "subinnertest":
                subInnerTests.append(elem)
        innerTest.logFile = logFile
        innerTest.startTime = startTime
        innerTest.endTime = endTime
        innerTest.duration = duration
        for subInnerTest in subInnerTests:
            text = ""
            result = ""
            endTime = ""
            for elem in root.findall('*'):
                tag = elem.tag.lower()
                if tag == "text" or tag == "message":
                    text = elem.text
                elif tag == "result":
                    result = elem.text
                elif tag == "endTime" or tag == "time" or tag == "timestamp":
                    endTime = elem.text
            innerTest.subInnerTests.append(RefactorResults.SubInnerTest(result, text, endTime))



def findElement(element,string):
    try:
        element.find(string)
    except ET.ParseError:
        return




def parseInnerTest(trxTest, outdir):
    
    for inner in trxTest.innerTests:
        root = ET.parse(os.path.join(outdir, inner.detailedFile))
        inner.logfile = root.find("logfile").text
        inner.startTime = root.find("starttime").text
        inner.endTime = root.find("endtime").text
        inner.duration = root.find("duration").text
        for subinnertest in root.findall("subinnertest"):
            inner.subInnerTests.append(RefactorResults.SubInnerTest(subinnertest.find("result").text, subinnertest.find("text").text,
                                                    subinnertest.find("endtime").text))

testobject = initstructsafe(filepath)
print testobject.name
print testobject.innerTests[0].name
print testobject.innerTests[1].subInnerTests[0].errorMessage
"""
gui = TK.Tk()
topFrame = TK.Frame(gui)
topFrame.pack(side = "top", fill = "x", expand = 1)
imageLabel = TK.Label(topFrame, text = "Placeholder image")
imageLabel.pack(side = "left")
resultsLabel = TK.Label(topFrame, text = "X/X tests passed. Final Result: Passed")
resultsLabel.pack(side = "bottom")
detailedFrame = TK.Frame(gui)
detailedFrame.pack(side = "bottom")
frameb1 = TK.Frame(detailedFrame)
frameb1.pack()
b1 = TK.Button(frameb1, text = "result 1")
b1.pack()
l1 = TK.Label(frameb1, text = "Error X/X")
l1.pack()
frameb2 = TK.Frame(detailedFrame)
frameb2.pack()
b2 = TK.Button(frameb2, text = "result 2")
b2.pack()
l2 = TK.Label(frameb2, text = "Error X/X")
l2.pack()
frameb3 = TK.Frame(detailedFrame)
frameb3.pack()
b3 = TK.Button(frameb3, text = "result 3")
b3.pack()
l3 = TK.Label(frameb3, text = "Error X/X")
l3.pack()
frameb4 = TK.Frame(detailedFrame)
frameb4.pack()
b4 = TK.Button(frameb4, text = "result 4")
b4.pack()
l4 = TK.Label(frameb4, text = "Error X/X")
l4.pack()
frameb5 = TK.Frame(detailedFrame)
frameb5.pack()
b5 = TK.Button(frameb5, text = "result 5")
b5.pack(side = "left")
l5 = TK.Label(frameb5, text = "Error X/X")
l5.pack(side = "right")
gui.mainloop()"""

filepath = "D:Desktop/AnalogIoCcpu.txt"
timestamp = "2016-02-22 09:34:08,211"

def locateLinesInLog(filePath, timeStamp):
    fil = open(filePath, "r+")
    lines = fil.readlines()
    fil.close()
    stamp = datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S,%f")
    lo = 0
    hi = len(lines)
    removedInRow = 0
    addedCusRemoved = 0
    while lo < hi:
        if len(lines) < 2:
            return -1
        mid = (hi + lo)/2
        try:
            currStamp = datetime.datetime.strptime(lines[mid][0:23],"%Y-%m-%d %H:%M:%S,%f")
        except ValueError:
            lines.pop(mid)
            removedInRow += 1
            hi -= 1
            continue
        if currStamp < stamp:
            lo = mid+1
            addedCusRemoved += removedInRow
            removedInRow = 0
        else:
            hi = mid
            if currStamp == stamp:
                addedCusRemoved += removedInRow
                removedInRow = 0
            else:
                removedInRow = 0
    addedCusRemoved += removedInRow
    return lo + addedCusRemoved

lo = locateLinesInLog(filepath, timestamp)
file = open("D:Desktop/AnalogIoCcpu.txt", "r+")
lines = file.readlines()
file.close()
print lo, lines[lo]