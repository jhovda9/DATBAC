import xml.etree.ElementTree as ET
import MatsTesting as Mats
import RefactorResults as RR
from BeautifulSoup import BeautifulSoup as BS
import os


def createHTML(file, outDir):
  wasPassed=False
  wasError=False
  wasOther=False
  divCounter = 0

  htmlFile = open(outDir + "/" + file + ".html", "wb")
  with open("HTMLTemplate.html","r") as f:
    htmlFile.write(f.read())

  # HEADER

  root = RR.createTestHierarchy(ET.fromstring(open(file, "r").read()))
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

    root = ET.fromstring(open(innerTest.detailedFile, "r").read())
    htmlFile.write( innerTest.result )
    htmlFile.write("""<div class="innertestcontent">""")
    htmlFile.write("<span>Start: " + root.find("starttime").text + "&emsp; End: "+ root.find("endtime").text + "&emsp; Duration: " + root.find("duration").text + "</span>")
    xmlroot = ET.fromstring(open(innerTest.detailedFile, "r").read())

    for e in xmlroot.iter('subinnertest'):
      htmlFile.write("""<div onclick="oneClick(event,this)">""")
      if e.find("result").text=="Passed":
        htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
      elif e.find("result").text=="Failed":
        htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
      else:
        htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")

      htmlFile.write(e.find("text").text )
      htmlFile.write("""<div class="innertestcontent" onclick="threeClick(event,this)">"""
           + innerTest.name +"<br>"+ e.find("text").text + "<br>" + e.find("endtime").text +
          """<br><a href="#"> log.txt not yet implemented</a></div></div>""")

    htmlFile.write("</div></div>")
      
  htmlFile.write("</div></div></div></div></body></html>")
  htmlFile.close()
  prettifyHTML(file)


def prettifyHTML(file):
  file = open(file + ".html","r+")
  uglyHtml = file.read()
  soup = BS(uglyHtml)
  prettyHTML = soup.prettify()
  file.seek(0)
  file.write(prettyHTML)
  file.truncate()
  file.close

createHTML("NASTLauncherResult.trx", os.getcwd())

