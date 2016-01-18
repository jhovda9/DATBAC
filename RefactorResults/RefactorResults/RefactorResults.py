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

class test(object):
    innerTests = []
    def __init__(self, name, result, errorMessage, detailedFile):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage
        self.detailedFile = detailedFile

def createTestObject(testElement):
    result = False
    if testElement.find("TestResult").text == "Passed":
        result = True
    testObject = test(testElement.find("TestName").text, result, testElement.find("ErrorMessage").text, 
                      "Placeholder")
    return testObject

file = open("IciIpsTest.trx", "r")
root = ET.fromstring(file.read())
rootObject = createTestObject(root)
print rootObject.result