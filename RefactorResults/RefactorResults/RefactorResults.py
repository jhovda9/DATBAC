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
          'warning': '#DF9538'
          }


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

    #Returns passed if tests are empty
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
    testObject = TRXTest(testElement.find("TestName").text, testElement.find("TestResult").text,
                         testElement.find("ErrorMessage").text)
    for innerTest in testElement.find("InnerTests").iter("InnerTest"):
        testObject.innerTests.append(InnerTest(innerTest.find("TestName").text, innerTest.find("TestResult").text,
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


def generateTestReport(outDir):
    trxFile = findTRX(outDir)
    if trxFile == None:
        print "No .trx file found in " + outDir
        return

    createHTML(trxFile,outDir)


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

def createHTML(file, outDir):
    divCounter = 0
    currentTest = ""
    prevTest = ""
    logFiles = []
    trxFile = os.path.join(outDir, file)
    htmlFile = open(os.path.join(outDir, file + ".html"), "wb")
    root = initializeTRXStructure(trxFile)
    parseInnerTest(root, outDir)
    errorList, totalTests = parseErrorMessage(root.errorMessage)

    # HEADER
    if root is not None:
        htmlFile.write("<!DOCTYPE html><html><head><title>" + root.name + "</title>")
        htmlFile.write("<body><div id='header'>")
        htmlFile.write("<div id='iconarea'>")
        if root.result == "Passed":
            htmlFile.write("<i class='material-icons green'> done </i>")
        else:
            htmlFile.write("<i class='material-icons red'> error </i>")
        htmlFile.write("</div><div id='textresultarea'>")
        htmlFile.write("<h1> Title: " + root.name + "</h1>")
        htmlFile.write("<h1> Result: " + root.result + "</h1>")
        htmlFile.write("<h3> ErrorMessage: " + root.errorMessage + "</h3> </div>")
        base64 = drawPieChart(errorList, totalTests)
        htmlFile.write("<div id='summaryarea'><div id='chartarea'><div id='chart'>")
        htmlFile.write("<img src='data:image/png;base64,%s'" %base64.getvalue().encode("base64").strip())
        htmlFile.write("</div><div id='chartlist'><ul>")
        htmlFile.write("</ul></div></div></div></div>")

    # MAIN
    if root.innerTests is not None:
        htmlFile.write("<div id='innertestcontainer'>")
        for innerTest in root.innerTests:
            currentColor, currentTest = getColorFromResult(innerTest.result)
            if currentTest != prevTest:
                for div in range(0, divCounter):
                    htmlFile.write("</div>")
                htmlFile.write("<div class='innertests' onclick='oneClick(event,this)'>")
                htmlFile.write(" <i class='material-icons' style='color:" + currentColor + "' >add_box</i>")
                htmlFile.write("<span class='spancounter'></span>" + innerTest.result  )
                htmlFile.write("<div class='innertestcontent'>")
                divCounter = 2
                prevTest = currentTest
            htmlFile.write("<div class='innertests' onclick='oneClick(event,this)'>")
            htmlFile.write("<i class='material-icons' style=' color:" + currentColor + "' >add_box</i>")
            htmlFile.write(innerTest.name + ", duration: " + innerTest.duration + "ms")
            htmlFile.write("<div class='innertestcontent'>")
            htmlFile.write("<span>Start: " + innerTest.startTime + "&emsp; End: " + innerTest.endTime +
                           "&emsp; Duration: " + innerTest.duration + "&emsp; Logfile: " +
                           "<a href='" + innerTest.logfile + "' target='_blank'>" + innerTest.logfile + "</a></span>")
            for subInnerTest in innerTest.subInnerTests:
                if innerTest.logfile not in logFiles:
                    logFiles.append(innerTest.logfile)
                subColor = getColorFromResult(subInnerTest.result)[0]
                htmlFile.write("<div onclick='oneClick(event,this);searchClick(this)'>")
                htmlFile.write("<i class='material-icons' style='color:" + subColor + "'>add_box</i>")
                htmlFile.write(subInnerTest.errorMessage)
                pos, lines = locateLinesInLog(os.path.join(outDir, innerTest.logfile), subInnerTest.timeStamp)
                htmlFile.write("<div class='innertestcontent " + innerTest.logfile + " " +
                               str(pos) + "' onclick='threeClick(event,this)'>")
                htmlFile.write("</div></div>")
            htmlFile.write("</div></div>")
        htmlFile.write("</div></div></div></div>")
        for logs in logFiles:
            htmlFile.write("<div style='display:none' id='" + logs + "'>")
            logFile = open(os.path.join(outDir, logs), "r+")
            logLines = logFile.readlines()
            for logLine in logLines:
                htmlFile.write(logLine + "<br>")
            htmlFile.write("</div>")
        htmlFile.write("</body></html>")

    htmlFile.close()
    prettifyHTMLandAddTemplate(os.path.join(outDir, file))


def prettifyHTMLandAddTemplate(file):
    file = open(file + ".html","r+")
    prevHtml = file.read()
    soup = BS(prevHtml)
    newHTML = soup.prettify()
    file.seek(0)
    file.write(HTMLTemplate())
    file.write(newHTML)
    file.truncate()
    file.close()


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


def locateLinesInLog(filePath, timeStamp):
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
    return lo, lines


def parseErrorMessage(errorMessage):
    valueString = []
    pairString = errorMessage[:-1].split("(")[1].split(",")
    totalNumberofTests = int(pairString[0].split(":")[1].split("/")[1].strip())
    for value in pairString:
        result = value.split(":")[0].strip()
        number = int(value.split(":")[1].split("/")[0].strip())
        valueString.append([result, number])
    return valueString, totalNumberofTests


def drawPieChart(errorList, totalTests):
    sizes = []
    colors = []
    labels = []
    for message in errorList:
        if message[1] != 0:
            sizes.append(message[1])
            colors.append(getColorFromResult(message[0])[0])
            percentage = "%.2f%%" % (100 * float(message[1])/float(totalTests))
            labels.append("{} {} {}".format(message[1], message[0], "(" + str(percentage)+ ")"))
    plt.figure(figsize=(4, 1))
    pieWedgesCollection = plt.pie(sizes, colors=colors)[0]
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
    global colors
    result = str.lower(result)
    if result in colors:
        color = colors[result]
    else:
        color = '#4138df'
    return color, result



def HTMLTemplate():
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
    #iconarea .material-icons{
      font-size: 190px;
    }

    .material-icons.red { color: #DF4138; }
    .material-icons.green { color: #26C154; }
    .material-icons.orange { color: orange; }
    .material-icons.blue { color: blue; }

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


    </style>
    <script type="text/javascript">

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
            var str = element.className;
            str = str.split(" ");
            var thelog = document.getElementById(str[1]);
            var theline = str[2];
            var logdata = thelog.innerHTML.split("<br>");
            var div = document.createElement("div");
            var logstring = "";
            for(var i = 0; i < logdata.length; i++){
                if (i == theline){
                    logstring += ("<span class='locatedline'>" + logdata[i] + "</span><br>");
                    while(logdata[i].trim().split(" ")[1] === logdata[i+1].trim().split(" ")[1]){
                        logstring +=("<span class='locatedline'>" + logdata[i+1] + "</span><br>")
                        i = i + 1;
                    }
                }else{
                    logstring += (logdata[i] + "<br>");
                }
            }
            div.innerHTML = logstring;
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
            var txtdiv = document.getElementById(str[1]);
            var linenumber = parseInt(str[2]);
            var div = clickedDivs[0];
            var logdatalines = txtdiv.innerHTML.split("<br>");
            div.innerHTML = "";
            for (var i = linenumber - 5; i < linenumber + 6; i++) {
                if (i >= 0 && i <= logdatalines.length-1) {
                    if (i == linenumber) {
                        div.innerHTML += ("<span class='locatedline'>" + logdatalines[linenumber] + "</span><br>");
                         while(logdatalines[i].trim().split(" ")[1] === logdatalines[i+1].trim().split(" ")[1]){
                            div.innerHTML +=("<span class='locatedline'>" + logdatalines[i+1] + "</span><br>")
                            i = i + 1;

                        }
                    } else {
                        div.innerHTML += (logdatalines[i] + "<br>");
                    }
                }
            }

        }
}

    </script>
    </head>"""


def main():
    generateTestReport( sys.argv[1] )

if __name__ == "__main__":
    sys.exit(main())
