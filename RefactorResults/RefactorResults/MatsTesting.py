#Test av command line
import sys
import getopt
import HTMLParser
import os
import xml.etree.ElementTree as ET
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

#class SubTest(object):

"""
class HTMLParser(HTMLParser.HTMLParser):
    def handle_data(self, data):
        print "Encountered data: %s" % data;


print os.getcwd()
file = open("test.html", "r")
parser = HTMLParser()
while True:
    parser.feed(file.readline())
    raw_input()
"""

file = open("IciIpsTest.trx", "r")
root = ET.fromstring(file.read())
subtests = root.find("InnerTests")
for child in subtests:
    print child.find("TestResult").text