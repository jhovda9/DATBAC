import xml.etree.ElementTree as ET
import MatsTesting as Mats
import RefactorResults as RR
import os



def createHTML(file, outDir):
    htmlFile = open(outDir + "/" + file + ".html", "wb")
    root = RR.createTestHierarchy(ET.fromstring(open(file, "r").read()))
    htmlFile.write("""
<!DOCTYPE html>
<html>
<head>
  <title>Prototype</title>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <style type="text/css">
    *{
      font-family:arial, sans-serif;
    }
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
</head>
<body>
  <div id="header">
    """)
    htmlFile.write("<h1> Title: " + root.name + "</h1>")
    htmlFile.write("<h1> Result: " + root.result + "</h1>")
    htmlFile.write("<h3> ErrorMessage: " + root.errorMessage + "</h3> </div>")
    htmlFile.write("""
<div id="summaryarea">
    <div id="chartarea">
      <div id="chart"></div>
      <div id="chartlist">
        <ul>
        """)
    htmlFile.write("<li>" + "# of passes" + "</li>")
    htmlFile.write("<li>" + "# of fails" + "</li>")
    htmlFile.write("<li>" + "# of aborts" + "</li>")
    htmlFile.write("""
        </ul>
      </div>
    </div>
    <div id="iconarea">
    """)
    if root.result=="Passed":
      htmlFile.write("""<i class="material-icons green"> done </i>""")
    else:
      htmlFile.write("""<i class="material-icons red"> error </i>""")

    htmlFile.write("""
    </div>
  </div>
<div id="innertestcontainer">
    """)
    wasPassed=False
    wasError=False
    wasOther=False
    divCounter = 0

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

      if wasPassed:
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
          htmlFile.write("""
            <div onclick="oneClick(event,this)">
            """)
          if e.find("result").text=="Passed":
            htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
          elif e.find("result").text=="Failed":
            htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
          else:
            htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")

          htmlFile.write(e.find("text").text )
          htmlFile.write("""
              <div class="innertestcontent" onclick="threeClick(event,this)">"""
              + innerTest.name +"<br>"+ e.find("text").text + "<br>" + e.find("endtime").text +
              """
              <br><a href="#"> log.txt not yet implemented</a>
              </div></div>""")
        htmlFile.write("</div></div>")

      elif wasError:
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
          htmlFile.write("""
            <div onclick="oneClick(event,this)">
            """)
          if e.find("result").text=="Passed":
            htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
          elif e.find("result").text=="Failed":
            htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
          else:
            htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")

          htmlFile.write(e.find("text").text )
          htmlFile.write("""
              
              
              <div class="innertestcontent" onclick="threeClick(event,this)">"""
              + innerTest.name +"<br>"+ e.find("text").text + "<br>" + e.find("endtime").text +
              """
              <br><a href="#"> log.txt not yet implemented</a>
              </div></div>""")
        htmlFile.write("</div></div>")


      elif wasOther:
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
          htmlFile.write("""
            <div onclick="oneClick(event,this)">
            """)
          if e.find("result").text=="Passed":
            htmlFile.write(""" <i class="material-icons green" class="add">add_box</i>""")
          elif e.find("result").text=="Failed":
            htmlFile.write(""" <i class="material-icons red" class="add">add_box</i>""")
          else:
            htmlFile.write(""" <i class="material-icons orange" class="add">add_box</i>""")

          htmlFile.write(e.find("text").text )
          htmlFile.write("""
              <div class="innertestcontent" onclick="threeClick(event,this)">"""
              + innerTest.name +"<br>"+ e.find("text").text + "<br>" + e.find("endtime").text +
              """
              <br><a href="#"> log.txt not yet implemented</a>
              </div></div>""")
        htmlFile.write("</div></div>")
        

        

    htmlFile.write("</div>")
    

    htmlFile.write("""
      </div>
    </div>
  </div>
</body>
</html>
          """)


createHTML("NASTLauncherResult.trx", os.getcwd())

