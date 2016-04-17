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