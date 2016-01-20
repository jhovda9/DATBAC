"""This program is part of "Presentasjon av resultat av automatisk testing av software" by Hovda and Jonassen. """

import xml.etree.ElementTree as ET
"""
class test(object):
    #parentTest
    children = []
    def __init__(self, testobject):
        self.testObject = testobject
        if testobject.find("TestResult").text == "Passed" :
            self.Result = True
        else:
            self.Result = False
        self.name = testobject.find("TestName").text
        self.findChildren()
    def findChildren(self):
        for child in self.testObject.findall("InnerTest"):
            self.children.append(test(child))

"""

class TFSTest(object):
    innerTests = []
    def __init__(self, name, result, errorMessage, detailedFile):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage
        self.detailedFile = detailedFile

def createTestObject(testElement):
    detailedResultsFile = "No file exists"
    if testElement.find("DetailedResultsFile") != None:
        detailedResultsFile = testElement.find("DetailedResultsFile").text
    testObject = TFSTest(testElement.find("TestName").text, testElement.find("TestResult").text, testElement.find("ErrorMessage").text,
                      detailedResultsFile)
    return testObject


def createTestHierarchy(root):
    baseTest = createTestObject(root)
    if root.find("InnerTests") != None:
        for test in root.find("InnerTests"):
            baseTest.innerTests.append(createTestObject(test))
    return baseTest

file = open("IciIpsTest.trx", "r")
root = ET.fromstring(file.read())
rootObject = createTestHierarchy(root)
for test in rootObject.innerTests:
    print test.name

def createHTML(file, outDir):
    trxFile = open(file, "r")
    htmlFile = open(outDir + "/" + file + ".html", "w+")
    root = createTestHierarchy(ET.fromstring(open(file, "r").read()))   