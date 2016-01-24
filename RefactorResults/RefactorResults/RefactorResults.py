"""This program is part of "Presentasjon av resultat av automatisk testing av software" by Hovda and Jonassen. """

import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import green
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

def createHTML(file, outDir):
    htmlFile = open(outDir + "/" + file + ".html", "wb")
    root = createTestHierarchy(ET.fromstring(open(file, "r").read()))
    htmlFile.write("<table style='border: solid black 2px'>\n")
    htmlFile.write("<tr><td>Testname</td> <td>result</td> <td>Innertest</td> <td>Innertest result</td>\n")
    htmlFile.write("<tr style='border: solid black 2px'>")
    htmlFile.write("<td>Root test</td>")
    htmlFile.write("<td>" + root.result + "</td>")
    htmlFile.write("<td></td><td></td>\n")
    htmlFile.write("</tr>")
    for innerTest in root.innerTests:
        htmlFile.write("<tr style='border: solid black 2px'>")
        htmlFile.write("<td></td><td></td>")
        htmlFile.write("<td>" + innerTest.name + "</td>")
        htmlFile.write("<td>" + innerTest.result + "</td>")
        htmlFile.write("</tr>")
    htmlFile.write("</table>")

def createPDF(file, outDir):
    headers = ["Test name", "Result", "Innertest", "Innertest Result"]
    root = createTestHierarchy(ET.fromstring(open(file, "r").read()))
    table = []
    tableStyle = TableStyle([('Grid'),(0,0),(-1,-1)], 1, green)
    table.append(headers)
    table.append([root.name, str(root.result), "place", "place"])
    for innerTest in root.innerTests:
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])

        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])

        table.append(["place", "place", innerTest.name, str(innerTest.result)])
        table.append(["place", "place", innerTest.name, str(innerTest.result)])
    c = canvas.Canvas((file + ".pdf"))
    doc = SimpleDocTemplate(file + ".pdf")
    #c.drawString(100,2000, "Test av ReportLab")
    #print table
    tab = Table(table)
    tab.setStyle(tableStyle)
    what = []
    what.append(tab)
    doc.build(what)
    #c.draw
    #c.save()