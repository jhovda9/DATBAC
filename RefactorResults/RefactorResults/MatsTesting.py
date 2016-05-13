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
import random
#from time import strptime

filepath = "D:Desktop/NASTLauncherResult.trx"


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

def oldlocateLinesInLog(filePath, timeStamp, preLines, postLines):
    preLines = 2
    postLines = 2
    lines = []
    file = open(filePath, "r+")
    time = datetime.datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S,%f")
    for i in range(preLines):
        lines.append("")
    x = -1
    while True:
        line = file.readline()
        x += 1
        if not line: 
            break
        try:
            if time <= datetime.datetime.strptime(line[0:23],"%Y-%m-%d %H:%M:%S,%f"):
                lines.append(line)
                break
        except ValueError:
            continue
        else:
            for i in range(preLines):
                if i != preLines-1:
                    lines[i] = lines[i+1]
                else:
                    lines[preLines - 1] = line
    for i in range(postLines):
        lines.append(file.readline())
    file.close()
    return x

def timer():
    trxtest = RefactorResults.initializeTRXStructure("D:TONSofTEST/NASTLauncherResult.trx")
    RefactorResults.parseInnerTest(trxtest, "D:TONSofTEST")
    for innertest in trxtest.innerTests:
        for subinner in innertest.subInnerTests:
            locateLinesInLog(os.path.join("D:TONSofTEST", innertest.logFile), subinner.timeStamp)

#Timer for single logfile
def timerSingle():
    file = open("D:Desktop/Acu.txt")
    lines = file.readlines()
    file.close()
    stamp = random.randint(0,len(lines)-1)
    timeStamp = lines[stamp][0:23]
    locateLinesInLog("D:Desktop/Acu.txt", timeStamp)

    


def timer2():
    trxtest = RefactorResults.initializeTRXStructure("D:TONSofTEST/NASTLauncherResult.trx")
    RefactorResults.parseInnerTest(trxtest, "D:TONSofTEST")
    for innertest in trxtest.innerTests:
        for subinner in innertest.subInnerTests:
            oldlocateLinesInLog(os.path.join("D:TONSofTEST", innertest.logFile), subinner.timeStamp, 2, 2)



#timer for single logfile
def timer2Single():
    file = open("D:Desktop/Acu.txt")
    lines = file.readlines()
    file.close()
    stamp = random.randint(0, len(lines)-1)
    timeStamp = lines[stamp][0:23]
    oldlocateLinesInLog("D:Desktop/Acu.txt", timeStamp, 2, 2)

print timeit.timeit(timerSingle, number = 1, setup= "import datetime")
#print timeit.timeit(timer2Single, number = 50, setup = "import datetime")