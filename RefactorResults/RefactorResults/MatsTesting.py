#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET
import datetime
from re import split
import datetime
import timeit
import Tkinter as TK
#from time import strptime

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
gui.mainloop()