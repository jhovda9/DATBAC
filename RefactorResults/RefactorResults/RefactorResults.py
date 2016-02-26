"""This program is part of "Presentasjon av resultat av automatisk testing av software" by Hovda and Jonassen. """

import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import green
from BeautifulSoup import BeautifulSoup as BS
import os
import sys
import datetime

class TRXTest(object):
    innerTests = []
    def __init__(self, name, result, errorMessage):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage

class InnerTest(object):
    def __init__(self, name, result, errorMessage, detailedFile, subInnerTests = [], startTime = "", endTime = "", duration = ""):
        self.name = name
        self.result = result
        self.errorMessage = errorMessage
        self.detailedFile = detailedFile
        self.subInnerTests = list(subInnerTests)
        self.startTime = startTime
        self.endTime = endTime
        self.duration = duration

    def calculateResult(self):
        result = "Passed"
        for subInner in self.subInnerTests:
            if subInner.result != "Passed":
                result = subInner.result
                break
        self.result = result

class SubInnerTest(object):
    def __init__(self, result, errorMessage, timeStamp):
        self.result = result
        self.errorMessage = errorMessage
        self.timeStamp = timeStamp

def initializeTRXStructure(path):
    testElement = ET.parse(path)
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text, testElement.find("ErrorMessage").text)
    for innerTest in testElement.find("InnerTests").iter("InnerTest"):
        testObject.innerTests.append(InnerTest(innerTest.find("TestName").text, innerTest.find("TestResult").text,
                                               innerTest.find("ErrorMessage").text, innerTest.find("DetailedResultsFile").text))
    return testObject

def parseInnerTest(trxTest, outdir):
    
    for inner in trxTest.innerTests:
        root = ET.parse(os.path.join(outdir,inner.detailedFile))
        inner.logfile = root.find("logfile").text
        inner.startTime = root.find("starttime").text
        inner.endTime = root.find("endtime").text
        inner.duration = root.find("duration").text
        for subinnertest in root.findall("subinnertest"):
            inner.subInnerTests.append(SubInnerTest(subinnertest.find("result").text,subinnertest.find("text").text,subinnertest.find("endtime").text))


def generateTestReport(outDir):
    trxFile = findTRX(outDir)
    if trxFile==None:
        print  "No .trx file found in " + outDir
        return
        
    createHTML(trxFile,outDir)


def findTRX(outDir):
    for file in os.listdir(outDir):
        if file.endswith(".trx"):
            return file
    
def parseTRX(path):
    file = open()

def createTestObject(testElement):
    detailedResultsFile = "No file exists"
    if testElement.find("DetailedResultsFile") != None:
        detailedResultsFile = testElement.find("DetailedResultsFile").text
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text, testElement.find("ErrorMessage").text,
                      detailedResultsFile)
    return testObject


def createTestHierarchy(root):
    baseTest = createTestObject(root)
    if root.find("InnerTests") != None:
        for test in root.find("InnerTests"):
            baseTest.innerTests.append(createTestObject(test))
    return baseTest

def createHTML(file, outDir):
    wasPassed=False
    wasError=False
    wasOther=False
    divCounter = 0
    trxFile = os.path.join( outDir, file  )
    htmlFile = open( os.path.join( outDir, file + ".html"), "wb")
    root = initializeTRXStructure(trxFile)
    parseInnerTest(root,outDir)
    htmlFile.write(HTMLTemplate())
    
    # HEADER

    htmlFile.write("""<body><div id="header">""")
    htmlFile.write("<h1> Title: " + root.name + "</h1>")
    htmlFile.write("<h1> Result: " + root.result + "</h1>")
    htmlFile.write("<h3> ErrorMessage: " + root.errorMessage + "</h3> </div>")
    htmlFile.write("""<div id="summaryarea"><div id="chartarea"><div id="chart"></div><div id="chartlist"><ul>""")
    htmlFile.write("<li>" + "# of passes" + "</li>")
    htmlFile.write("<li>" + "# of fails" + "</li>")
    htmlFile.write("<li>" + "# of aborts" + "</li>")
    htmlFile.write("""</ul></div></div><div id="iconarea">""")
    if root.result=="Passed":
        htmlFile.write("""<i class="material-icons green"> done </i>""")
    else:
        htmlFile.write("""<i class="material-icons red"> error </i>""")

    # MAIN
    htmlFile.write("""</div></div><div id="innertestcontainer">""")
    for innerTest in root.innerTests:

        if innerTest.result=="Passed" and wasPassed==False:
            for div in range(0,divCounter):
                htmlFile.write("</div>")
            divCounter = 0
            wasPassed=True
            wasError=False
            wasOther=False
            htmlFile.write("""<div class="innertests" onclick="oneClick(event,this)">""")
            divCounter+= 1
            htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
            htmlFile.write(innerTest.result)
            htmlFile.write("""<div class="innertestcontent">""")
            divCounter+= 1
        elif innerTest.result=="Error" and wasError==False:
            for div in range(0,divCounter):
                htmlFile.write("</div>")
            divCounter = 0
            wasPassed = False
            wasError = True
            wasOther = False
            htmlFile.write("""<div class="innertests" onclick="oneClick(event,this)">""")
            divCounter += 1
            htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
            htmlFile.write(innerTest.result)
            htmlFile.write("""<div class="innertestcontent">""")
            divCounter+= 1
        elif innerTest.result=="Warning" and wasOther==False:
            for div in range(0,divCounter):
                htmlFile.write("</div>")
            divCounter = 0
            wasPassed = False
            wasError = False
            wasOther = True
            htmlFile.write("""<div class="innertests" onclick="oneClick(event,this)">""")
            divCounter+= 1
            htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")
            htmlFile.write(innerTest.result)
            htmlFile.write("""<div class="innertestcontent">""")
            divCounter+= 1
        htmlFile.write("""<div class="innertests" onclick="oneClick(event,this)">""")
        if innerTest.result=="Passed":
            htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
        elif innerTest.result=="Error":
            htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
        else:
            htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")

        htmlFile.write( innerTest.name )
        htmlFile.write("""<div class="innertestcontent">""")
        htmlFile.write("<span>Start: " + innerTest.startTime + "&emsp; End: "+ innerTest.endTime + "&emsp; Duration: " + innerTest.duration + "</span>")

        for subInnerTest in innerTest.subInnerTests:
            htmlFile.write("""<div onclick="oneClick(event,this)">""")
            if subInnerTest.result=="Passed":
                htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
            elif subInnerTest.result=="Failed":
                htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
            else:
                htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")
            htmlFile.write(subInnerTest.errorMessage)
            htmlFile.write("""<div class="innertestcontent" onclick="threeClick(event,this)">""")
            consoleLines = locateLinesInLog(os.path.join( outDir, innerTest.logfile), subInnerTest.timeStamp, 3, 3)
            for line in consoleLines:
                htmlFile.write(line + "<br>")
            htmlFile.write("</div></div>")
        htmlFile.write("</div></div>")     
    htmlFile.write("</div></div></div></div></body></html>")
    htmlFile.close()
    prettifyHTML(os.path.join( outDir, file) )


def prettifyHTML(file):
    file = open(file + ".html","r+")
    uglyHtml = file.read()
    soup = BS(uglyHtml)
    prettyHTML = soup.prettify()
    file.seek(0)
    file.write(prettyHTML)
    file.truncate()
    file.close

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

def locateLinesInLog(filePath, timeStamp, preLines, postLines):
    fil = open(filePath, "r+")
    lines = fil.readlines()
    stamp = datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S,%f")
    lo = 0
    hi = len(lines)
    while lo < hi:
        mid = (hi + lo)/2
        try:
            currStamp = datetime.datetime.strptime(lines[mid][0:23],"%Y-%m-%d %H:%M:%S,%f")
        except ValueError:
            mid = mid - 1
        if currStamp < stamp:
            lo = mid+1
        else:
            hi = mid
    ret = []
    for i in range(preLines+1)[::-1]:
        if lo-i < 0:
            continue
        try:
            ret.append(lines[lo-i])
        except  :
            continue
    for i in range(postLines+1)[1:]:
        try:
            ret.append(lines[lo+i])
        except IndexError:
            continue
    return ret

def HTMLTemplate():
    return """<!DOCTYPE html>
    <html>
    <head>
    <title>Prototype</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style type="text/css">
    *{
      font-family:arial, sans-serif;
    }
    body {overflow-y:scroll;}

    #iconarea .material-icons{
      font-size: 190px;
    }

    .material-icons.red { color: red; }
    .material-icons.green { color: green; }
    .material-icons.orange { color: orange; }

    #header h1, h3{
      margin: 25px 0 25px 100px;
    }
    #summaryarea{
      height: auto;
      overflow: hidden;
      border: 1px solid black;
      border-left: none;
      border-right: none;
    }
    #iconarea{
      display: inline-block;
      float: right;
      width: 10%;
      min-width: 200px;
      border-left: 1px solid black;
    }
    #chartarea{
      display: inline-block;
      width: auto;
      overflow: hidden;
    }
    #chart{
      border: 1px solid black;
      border-radius: 255px;
      height: 150px;
      width: 150px;
      margin: 20px 0 0 20px;
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

    #innertestcontainer{
      margin: 0 100px 0 100px;
      padding:10px;
      font-size: 1.5em;
    }

    .innertestcontent .innertestcontent {
      font-size:0.9em;
      border:1px solid black;
      padding:5px;
      font-family:monospace;
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


    </style>
    <script type="text/javascript">
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
        
        if(element.getElementsByTagName("div")[0].style.display === "none"||element.getElementsByTagName("div")[0].style.display === ''){
          element.getElementsByTagName("div")[0].style.display = "block";
          element.getElementsByTagName("i")[0].innerHTML = "indeterminate_check_box";
        } else {
          element.getElementsByTagName("div")[0].style.display = "none";
          element.getElementsByTagName("i")[0].innerHTML = "add_box";
        }

      }
    }

    function threeClick(event, element)
    {
      if(amIclicked(event, element))
      {
        alert("TODO:implement")
      }
    }

    </script>
    </head>"""

def main():
    generateTestReport( sys.argv[1] )

if __name__ == "__main__":
    sys.exit(main())
