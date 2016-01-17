#Test av command line
import sys
import getopt
import HTMLParser
import os
print "Command line worked"
"""
opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["inputFile=", "outputLocation="])
for opt, arg in opts:
    if opt in ("-i", "--inputFile"):
        inputfile = arg
    if opt in ("-o", "--outputLocation"):
        outputLocation = arg
print inputfile
print outputLocation"""

class HTMLParser(HTMLParser.HTMLParser):
    def handle_data(self, data):
        print "Encountered data: %s" % data;
#print os.listdir(os.getcwd())
file = open("tes.html", "r")
parser = HTMLParser()
while True:
    parser.feed(file.readline())
    raw_input()