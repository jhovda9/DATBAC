"""This program is part of "Presentasjon av resultat av automatisk testing av software" by Hovda and Jonassen. """

import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import green
from BeautifulSoup import BeautifulSoup as BS
import os
import sys
import datetime
import matplotlib.pyplot as plt
import cStringIO

colors = {'passed': '#26C154',
          'error': '#DF4138',
          'failed': '#DF4138',
          'warning': '#DF9538',
          'other': '#4138df'
          }
icons = {'testpass': 'iVBORw0KGgoAAAANSUhEUgAAAIsAAABpCAYAAAAKldB2AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAAPrSURBVHhe7d2/axRBGMbx/DUKYqMIFora2IilIhYqCEqEgAQbG0GsLAQrGxEL/5OEeEEtVfzxz5z3rky4vX3ubndm3pl3Zp7ic7l97rjNsl8IaZKd+XxOjTp3dG9++uD2/NWfj4tD/J5lcKT6SSinDm51xgYDR6rbcihTgoEj1QuF4mwLBo5Up02hOJuCGQxUpzGhOOuC6R1QnaaE4qBgeh9K9fEJxVkNZvDhVI+QUJzlYOBJqHwxQnFcMPBEVLaYoThXj3fxyahcGqFcnj1efDR/DFVFMxQxOCGVSTsU0TshlSlFKKJ3QOVJFYoYDFSOC58fwJsdYl0oAo5kX+pQBBzJthyhCDiSXblCEXAkm3KGIuBI9uQORcCRbLEQioAj2XFx9hDe7BA+oQg4kg2WQhFwpPyshSLgSHlZDEXAkfKxGoqAI+VhORQBR0rPeigCjpRWCaEIOFI6l2aP4M0OoRGKgCOlUVIoAo6kr7RQBBxJV4mhCDiSnlJDEXAkHSWHIuBI8ZUeioAjxVVDKAKOFI/cVHSzQ+QIRcCR4qgpFAFHCldbKAKOFKbGUAQcyV+toQg4kp+aQxFwpOlqD0XAkaZpIRQBRxqvlVAEHGmclkIRcKTtWgtFwBHZ+/5m8QW/1poWQxFwXPX0x9vuryyfObyzOMTvaUWroQg4Lnv+810XiruwloNpORQBR+fl7w+9UJwWg2k9FAFHsS4Up6VgGMp/cJT/ALEpFKeFYK4dP4HXHqLEUMRgeP33UxcBukik5mAYSt9gmBKKU2MwDGWod+ATilNTMAwFO3kSEopTQzAMZb3u4ezhXXiRPkoOhqFstvVXZB8lBsNQtuseXvx633Qw17/swWsIUVso4uRJq8EwlPF6B60Fw1CmGQytBMNQpoNj7cEwFD9wFLUGw1D8wdGpLRiGEgaOy2oJhqGEg+Oq0oO58W0ffg8hWgtFwBEpNRiGEg8c1yktGIYSFxw3KSUYhhIfHLexHgxD0QHHMawGw1D0wHEsa8EwFF1wnMJKMAxFHxynyh3Mza/P4GeEYChDcPSRKxiGkg4cfaUOhqGkBccQqYJhKOnBMZR2MAwlDzjGoBXM+aP78LUQDGUcOMaiEUxsDGU8OMZkORiGMg0cY7MYDEOZDo4aLAXDUPzAUYuFYBiKPzhqyhkMQwkDR205gmEo4eCYQspgGEoccEwlRTAMJR44pqQZDEOJC46paQTDUOKDYw4xg2EoOuCYS4xgGIoeOOYUEgxD0QXH3HyCYSj64GjBlGAYShpwtGJMMAwlHThasikYhpIWHK1BwTCU9OBo0XIwDCUPOFolwVw53l08xa+TpvnOP9N0RctZvjZJAAAAAElFTkSuQmCC',
         'testfail': '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',
         'error': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABaSURBVDhPY/j//z/DAzeL//cdycRuGUAj/jMwPPbBIkkq9pn3n+ERNgmScQ/dDOoB+x+ECakbOQYhNBLC6PpoZRA6HkaBjY6pZhCxmJoGUa0YAfmf8oLtPwMAwsMZ2E1CMc0AAAAASUVORK5CYII=',
         'failed': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABaSURBVDhPY/j//z/DAzeL//cdycRuGUAj/jMwPPbBIkkq9pn3n+ERNgmScQ/dDOoB+x+ECakbOQYhNBLC6PpoZRA6HkaBjY6pZhCxmJoGUa0YAfmf8oLtPwMAwsMZ2E1CMc0AAAAASUVORK5CYII=',
         'warning': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABYSURBVDhPY/j//z/Dg6kW/++TjTOARvxnYHg8A5skiXjGvP8Mj7BJkIx76GZQD9j/IExI3cgxCKGREEbXRyuD0PEwCmx0TDWDiMXUNIhqxQjI/5QXbP8ZAKH+dtRVhEDRAAAAAElFTkSuQmCC',
         'passed': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABYSURBVDhPY/j//z9D5MGQ/2pk4yKgEf8ZGCYfwiZJIj405z9DAzYJkvF0uhk0Hex/ECakbuQYhNBICKPro5VB6HgYBTY6pppBxGJqGkS1YgTkf8oLtv8MAHM2ANZQJ/u9AAAAAElFTkSuQmCC',
         'other': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABaSURBVDhPY/j//z9DkvP9/44WZGLnB0Aj/jMw9PtjkSQV+z/5z9CJTYJk/JhuBj0G+x+ECakbOQYhNBLC6PpoZRA6HkaBjY6pZhCxmJoGUa0YAfmf8oLtPwMA2RQYzLYTEH4AAAAASUVORK5CYII='
        }
testCounters = {}


class TRXTest(object):
    def __init__(self, name, result, errorMessage, innerTests = []):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage
        self.innerTests = list(innerTests)


class InnerTest(object):
    def __init__(self, name, result, errorMessage, detailedFile, subInnerTests = [], startTime = "", endTime = "",
                 duration = ""):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage
        self.detailedFile = detailedFile
        self.subInnerTests = list(subInnerTests)
        self.startTime = startTime
        self.endTime = endTime
        self.duration = duration



class SubInnerTest(object):
    def __init__(self, result, errorMessage, timeStamp):
        self.result = result
        self.errorMessage = errorMessage
        self.timeStamp = timeStamp


def initializeTRXStructure(path):
    parser = ET.XMLParser(encoding="utf-8")
    testElement = ET.parse(path, parser = parser)
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text,
                         testElement.find("ErrorMessage").text)
    for innerTest in testElement.find("InnerTests").iter("InnerTest"):
        testObject.innerTests.append(InnerTest(innerTest.find("TestName").text, innerTest.find("TestResult").text,
                                               innerTest.find("ErrorMessage").text,
                                               innerTest.find("DetailedResultsFile").text))
        testCounter(innerTest.find("TestResult").text)
    return testObject

def testCounter(result):
    global testCounters
    if result not in testCounters:
        testCounters[result] = 1
    else:
        testCounters[result] += 1


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


def generateTestReport(outDir):
    trxFile = findTRX(outDir)
    if trxFile == None:
        print "No .trx file found in " + outDir
        return
    trxRoot = initializeTRXStructure(os.path.join(outDir, trxFile))
    parseInnerTest(trxRoot, outDir)
    createHTML(trxFile, outDir, trxRoot)



def findTRX(outDir):
    for file in os.listdir(outDir):
        if file.endswith(".trx"):
            return file


def createTestObject(testElement):
    detailedResultsFile = "No file exists"
    if testElement.find("DetailedResultsFile") != None:
        detailedResultsFile = testElement.find("DetailedResultsFile").text
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text,
                         testElement.find("ErrorMessage").text, detailedResultsFile)
    return testObject


def createTestHierarchy(root):
    baseTest = createTestObject(root)
    if root.find("InnerTests") != None:
        for test in root.find("InnerTests"):
            baseTest.innerTests.append(createTestObject(test))
    return baseTest

def returnEmptyIfNone(s):
    if s is None:
        return ''
    return str(s)

def createHTML(file, outDir, trxRoot):
    global icons
    divCounter = 0
    currentTest = ""
    prevTest = ""
    logFiles = []
    htmlFile = open(os.path.join(outDir, file + ".html"), "wb")

    # HEADER
    if trxRoot is not None:
        htmlFile.write("<!DOCTYPE html><html><head><title>" + returnEmptyIfNone(trxRoot.name) + "</title>")
        htmlFile.write("<body><div id='header'>")
        htmlFile.write("<div id='iconarea'>")
        if trxRoot.result == "Passed":
            htmlFile.write("<img src='data:image/png;base64," + icons['testpass'] + "'/>")
        else:
            htmlFile.write("<img src='data:image/png;base64," + icons['testfail'] + "'/>")
        htmlFile.write("</div><div id='textresultarea'>")
        htmlFile.write("<h1> Title: " + returnEmptyIfNone(trxRoot.name) + "</h1>")
        htmlFile.write("<h1> Result: " + returnEmptyIfNone(trxRoot.result) + "</h1>")
        htmlFile.write("<h3> ErrorMessage: " + returnEmptyIfNone(trxRoot.errorMessage) + "</h3> </div>")
        base64 = drawPieChart()
        if base64 is not None:
            htmlFile.write("<div id='summaryarea'><div id='chartarea'><div id='chart'>")
            htmlFile.write("<img src='data:image/png;base64,%s'" %base64.getvalue().encode("base64").strip())
        htmlFile.write("</div><div id='chartlist'><ul>")
        htmlFile.write("</ul></div></div></div></div>")

    # MAIN
    if trxRoot.innerTests is not None:
        htmlFile.write("<div id='innertestcontainer'>")
        for innerTest in trxRoot.innerTests:
            currentColor, currentTest = getColorFromResult(innerTest.result)
            if currentTest != prevTest:
                for div in range(0, divCounter):
                    htmlFile.write("</div>")
                htmlFile.write("<div class='innertests' onclick='oneClick(event,this)'>")
                htmlFile.write("<img class='" + currentTest + "' src='data:image/png;base64," + currentColor + "'/>")
                htmlFile.write("<span class='spancounter'></span>" + returnEmptyIfNone(innerTest.result))
                if str.lower(innerTest.result) != 'passed':
                    htmlFile.write(" - " + returnEmptyIfNone(innerTest.name))
                htmlFile.write("<div class='innertestcontent'>")
                divCounter = 2
                prevTest = currentTest
            htmlFile.write("<div class='innertests' onclick='oneClick(event,this)'>")
            htmlFile.write("<img class='" + currentTest + "' src='data:image/png;base64," + currentColor + "'/>")
            htmlFile.write(returnEmptyIfNone(innerTest.name) + ", duration: " + returnEmptyIfNone(innerTest.duration) +
                           "ms")
            htmlFile.write("<div class='innertestcontent'>")
            htmlFile.write("<span>Start: " + returnEmptyIfNone(innerTest.startTime) + "&emsp; End: " +
                           returnEmptyIfNone(innerTest.endTime) + "&emsp; Duration: " +
                           returnEmptyIfNone(innerTest.duration) + "&emsp; Logfile: " +
                           "<span class='displaylogspan' onclick='displayLog(event,this)'>" +
                           returnEmptyIfNone(innerTest.logfile) + "</span></span>")
            for subInnerTest in innerTest.subInnerTests:
                if subInnerTest is not None:
                    if innerTest.logfile not in logFiles:
                        logFiles.append(innerTest.logfile)
                    subColor, subTest = getColorFromResult(subInnerTest.result)
                    htmlFile.write("<div onclick='oneClick(event,this);searchClick(this)'>")
                    htmlFile.write("<img class='" + subTest + "' src='data:image/png;base64," + subColor + "'/>")
                    htmlFile.write(returnEmptyIfNone(subInnerTest.errorMessage))
                    pos = locateLinesInLog(os.path.join(outDir, innerTest.logfile), subInnerTest.timeStamp)
                    htmlFile.write("<div class='innertestcontent " + innerTest.logfile + " " +
                                   str(pos) + "' onclick='threeClick(event,this)'>")
                    htmlFile.write("</div></div>")
            htmlFile.write("</div></div>")
        htmlFile.write("</div></div></div></div>")
        for logs in logFiles:
            htmlFile.write("<div style='display:none' id='" + logs + "'>")
            with open(os.path.join(outDir, logs), "r+") as logFile:
                logLines = logFile.readlines()
                for logLine in logLines:
                    htmlFile.write(logLine + "<br>")
                htmlFile.write("</div>")
        htmlFile.write("</body></html>")

    htmlFile.close()
    prettifyHTMLandAddTemplate(os.path.join(outDir, file))


def prettifyHTMLandAddTemplate(htmlFile):
    htmlFile = open(htmlFile + ".html", "r+")
    prevHtml = htmlFile.read()
    soup = BS(prevHtml)
    newHTML = soup.prettify()
    htmlFile.seek(0)
    htmlFile.write(HTMLTemplate())
    htmlFile.write(newHTML)
    htmlFile.truncate()
    htmlFile.close()


def createPDF(file, outDir, trxRoot):
    headers = ["Test name", "Result", "Innertest", "Innertest Result"]
    table = []
    tableStyle = TableStyle([('Grid'),(0,0),(-1,-1)], 1, green)
    table.append(headers)
    table.append([trxRoot.name, str(trxRoot.result), "place", "place"])
    for innerTest in trxRoot.innerTests:
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

def drawPieChart():
    global testCounters
    global colors
    sizes = []
    chartcolors = []
    labels = []
    totalTests = 0
    for key, counter in testCounters.iteritems():
        totalTests += counter
    for test, counter in testCounters.iteritems():
        sizes.append(counter)
        if str.lower(test) in colors:
            chartcolors.append(colors[str.lower(test)])
        else:
            chartcolors.append(colors['other'])
        percentage = "%.2f%%" % (100 * float(counter)/float(totalTests))
        labels.append("{} {} {}".format(counter, test, "(" + str(percentage) + ")"))
    plt.figure(figsize=(4, 1))
    pieWedgesCollection = plt.pie(sizes, colors=chartcolors)[0]
    for wedge in pieWedgesCollection:
        wedge.set_lw(0)
    plt.axis('equal')
    plt.legend(loc=2, prop={'size': 7}, bbox_to_anchor=(1, 1), labels=labels, frameon=False)
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.32, box.height])
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format, transparent=True, dpi=200, bbox_inches='tight')
    return sio


def getColorFromResult(result):
    global icons
    result = str.lower(result)
    if result in icons:
        color = icons[result]
    else:
        color = icons['other']
    return color, result


def HTMLTemplate():
    global icons
    iconsForJS = {'passed': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABPSURBVDhPY/j//z9D5MGQ/2pk4yKgEf8ZGCYfwiZJIj405z9DAzYJkvH0UYMIYtoZNB2cJojB6PpoZRC5eNQgwpiaBlGtGAGlCcoLtv8MAGpW768pGjUHAAAAAElFTkSuQmCC',
                  'other': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABRSURBVDhPY/j//z9DkvP9/44WZGLnB0Aj/jMw9PtjkSQV+z/5z9CJTYJk/HjUIIKYdgY9BqcJYjC6PloZRC4eNYgwpqZBVCtGQGmC8oLtPwMA+OUMDFAYXwwAAAAASUVORK5CYII=',
                  'warning': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABPSURBVDhPY/j//z/Dg6kW/++TjTOARvxnYHg8A5skiXjGvP8Mj7BJkIx7Rg0iiGlnUA84TRCD0fXRyiBy8ahBhDE1DaJaMQJKE5QXbP8ZAFl2bvxyi2akAAAAAElFTkSuQmCC',
                  'failed': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABPSURBVDhPY/j//z/Dg6kW/++TjTOARvxnYHg8A5skiXjGvP8Mj7BJkIx7Rg0iiGlnUA84TRCD0fXRyiBy8ahBhDE1DaJaMQJKE5QXbP8ZAFl2bvxyi2akAAAAAElFTkSuQmCC',
                  'error': 'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuOWwzfk4AAABRSURBVDhPY/j//z/DAzeL//cdycRuGUAj/jMwPPbBIkkq9pn3n+ERNgmScc+oQQQx7QzqAacJYjC6PloZRC4eNYgwpqZBVCtGQGmC8oLtPwMA/YkMwOzZCVcAAAAASUVORK5CYII='
                  }
    return """

    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style type="text/css">
    *{
      font-family:arial, sans-serif;
    }
    body{
        overflow-y:scroll;
        background-color: #F4F5F9;
        min-width:560px;
    }
    #textresultarea{
        display:inline-block;
        max-width:50%;
    }

    #iconarea img{
        height: 160px;
        margin-left: 14px;
    }
    #header{
      margin: 25px 0 25px 0;
      display:inline-block;
      width:100%;
    }
    #summaryarea{
      height: auto;
      overflow: hidden;
      width:100%;
      border: 1px solid black;
      border-left: none;
      border-right: none;
    }
    #iconarea{
        display:inline-block;
      min-width: 200px;
      margin-left: 25px;
    }
    #chartarea{
      width: auto;
    }
    #chart{
      height: 200px;
      width: auto;
      display: inline-block;

    }
    #chartlist{
      display: inline-block;
      float: right;
    }
    li{
      list-style-type: square;
      font-size: 1.5em;
    }
    span{
      font-size:0.6em;
    }
    .spancounter{
        font-size:1em;
    }
    #innertestcontainer{
      margin: 0 0 0 200px;
      padding:10px;
      font-size: 1.5em;
    }
    .innertestcontent .innertestcontent {
      border:1px solid black;
      padding:5px;
      font-family:monospace;
    }
    .innertestcontent .innertestcontent .innertestcontent{
        overflow-y:scroll;
    }
    .remove{
      display:none;
    }
    .innertestcontent{
      display:none;
      margin-left: 50px;
      font-size:0.9em;
      vertical-align:middle;
    }
    .innertestcontent i{
    font-size:15px;
    }
    .innertests{
      cursor: pointer;
      -webkit-user-select:none;
      -moz-user-select: none;
      -ms-user-select: none;
      margin-top:5px;
    }
    .locatedLine{
        background-color:yellow;
        font-size:1em;
        font-family:monospace;
    }
    #biglog{
        font-family:monospace;
        border:1px solid black;
        height: 50vh;
        max-width: 60%;
        padding: 10px;
        overflow:scroll;
        position:fixed;
        right: 10px;
        top:10px;
        background-color: white;
        resize:both;
    }
    .displaylogspan{
        color: blue;
        text-decoration: underline;
        font-size: 1em;
    }


    </style>
    <script type="text/javascript">
    """ + "var passed = '" + icons['passed'] + "';\n" +\
           "var passednon = '" + iconsForJS['passed'] + "';\n" +\
           "var error = '" + icons['error'] + "';\n" +\
           "var errornon = '" + iconsForJS['error'] + "';\n" +\
            "var failed = '" + icons['error'] + "';\n" +\
            "var failednon = '" + iconsForJS['error'] + "';\n" +\
           "var warning = '" + icons['warning'] + "';\n" +\
           "var warningnon = '" + iconsForJS['warning'] + "';\n" +\
           "var other = '" + icons['other'] + "';\n" +\
           "var othernon = '" + iconsForJS['other'] + "';\n" + """
           var listofresults = ['passed','error','failed','warning'];
    window.onload = function () {
        var outerdiv = document.getElementById("innertestcontainer");
        var outerdivchildren = outerdiv.children;
        var fromnumber = 1;
        var tonumber = 0;
        for (var i = 0; i < outerdivchildren.length; i++) {
            var incnumber = outerdivchildren[i].children[2].children.length;
            tonumber += incnumber;
            var str = "Test " + fromnumber + "-" + tonumber + ": ";
            outerdivchildren[i].getElementsByTagName("span")[0].innerHTML = str;
            fromnumber+=incnumber;
        }
    };

    function amIclicked(e, element)
    {
      if (!e) var e = window.event;
      e.cancelBubble = true;
      if (e.stopPropagation) e.stopPropagation()
        e = e || event;
      var target = e.target || e.srcElement;

      if(target.id==element.id)
        return true;
      else
        return false;
    }
    function oneClick(event, element)
    {
      if(amIclicked(event, element))
      {
        var thetype = element.getElementsByTagName("img")[0].className;
        if(listofresults.indexOf(thetype) < 0){
            var thetype = "other";
        }
        if(element.getElementsByTagName("div")[0].style.display === "none"||element.getElementsByTagName("div")[0].style.display === ''){
          element.getElementsByTagName("div")[0].style.display = "block";
          var thebase64 = eval(thetype + "non");
          var base64img = "data:image/png;base64,";
          var source = base64img + thebase64;
          element.getElementsByTagName("img")[0].setAttribute("src",source);
        } else {
          element.getElementsByTagName("div")[0].style.display = "none";
            var thebase64 = eval(thetype);
            var base64img = "data:image/png;base64,";
            var source = base64img + thebase64;
          element.getElementsByTagName("img")[0].setAttribute("src",source);
        }
      }
    }

    function returnLogLines(log, linenumber){
        var thelog = document.getElementById(log);
        var logdata = thelog.innerHTML.split("<br>");
        var logstring = "";
        if (linenumber >= 0) {
            for (var i = linenumber - 5; i < linenumber + 6; i++) {
                if (i >= 0 && i <= logdata.length-1) {
                    if (i == linenumber) {
                        logstring += ("<span class='locatedline'>" + logdata[linenumber] + "</span><br>");
                        if (logdata[i+1]) {
                            while(logdata[i].trim().split(" ")[1] === logdata[i+1].trim().split(" ")[1]){
                                logstring +=("<span class='locatedline'>" + logdata[i+1] + "</span><br>");
                                i = i + 1;
                            }
                        }
                    } else {
                        logstring += (logdata[i] + "<br>");
                    }
                }
            }
        } else {
            for(var i = 0; i < logdata.length; i++){
                if (i == linenumber){
                    logstring += ("<span class='locatedline'>" + logdata[i] + "</span><br>");
                    if(logdata[i+1]){
                        while(logdata[i].trim().split(" ")[1] === logdata[i+1].trim().split(" ")[1]){
                            logstring +=("<span class='locatedline'>" + logdata[i+1] + "</span><br>")
                            i = i + 1;
                        }
                    }
                }else{
                    logstring += (logdata[i] + "<br>");
                }
            }
        }
        return logstring;
    }

    function threeClick(event, element)
    {
        if(amIclicked(event, element))
        {
            var str = element.className;
            str = str.split(" ");
            var thelog = str[1];
            var theline = str[2];
            var div = document.createElement("div");
            div.innerHTML = returnLogLines(thelog, theline);
            div.setAttribute('id','biglog');
            document.body.appendChild(div);
            var scrollto = div.getElementsByTagName("span")[0];
            scrollto.scrollIntoView();
        }
        window.addEventListener('mousedown', function(event){
            var box = document.getElementById('biglog');
            if (event.target != box && event.target.parentNode != box && box != null){
                box.parentNode.removeChild(box);
            }
        });
    }

    function searchClick(clicked) {
        var clickedDivs = clicked.getElementsByTagName("div");
        if (clickedDivs[0].style.display === "block" && clickedDivs[0].innerHTML.split(",").length < 3) {
            var str = clickedDivs[0].className;
            str = str.split(" ");
            var thelog = str[1];
            var theline = parseInt(str[2]);
            var div = clickedDivs[0];
            div.innerHTML = returnLogLines(thelog, theline)
        }
}
    function displayLog(event, element) {
        if(amIclicked(event, element)){
            var log = element.innerText;
            var div = document.createElement("div");
            div.innerHTML = returnLogLines(log, -1);
            div.setAttribute('id','biglog');
            document.body.appendChild(div);
        }
        window.addEventListener('mousedown', function(event){
            var box = document.getElementById('biglog');
            if (event.target != box && event.target.parentNode != box && box != null){
                box.parentNode.removeChild(box);
            }
        });
}

    </script>
    </head>"""



def main():
    generateTestReport(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
