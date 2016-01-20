#!/usr/bin/env python

#
# Generated Mon Jan 05 08:03:27 2009 by generateDS.py.
#

import sys
import getopt
from string import lower as str_lower
from xml.dom import minidom
from xml.dom import Node

#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write('    ')

def quote_xml(inStr):
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_attrib(inStr):
    s1 = (isinstance(inStr, basestring) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('"', '&quot;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class _MemberSpec(object):
    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type(self): return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container


#
# Data representation classes.
#

class SummaryResult(object):
    subclass = None
    superclass = None
    def __init__(self, TestName='', TestResult='', ErrorMessage='', DetailedResultsFile='', InnerTests=None):
        self.TestName = TestName
        self.TestResult = TestResult
        self.ErrorMessage = ErrorMessage
        self.DetailedResultsFile = DetailedResultsFile
        self.InnerTests = InnerTests
    def factory(*args_, **kwargs_):
        if SummaryResult.subclass:
            return SummaryResult.subclass(*args_, **kwargs_)
        else:
            return SummaryResult(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_TestName(self): return self.TestName
    def set_TestName(self, TestName): self.TestName = TestName
    def get_TestResult(self): return self.TestResult
    def set_TestResult(self, TestResult): self.TestResult = TestResult
    def validate_TestResult(self, value):
        # validate type TestResult
        pass
    def get_ErrorMessage(self): return self.ErrorMessage
    def set_ErrorMessage(self, ErrorMessage): self.ErrorMessage = ErrorMessage
    def get_DetailedResultsFile(self): return self.DetailedResultsFile
    def set_DetailedResultsFile(self, DetailedResultsFile): self.DetailedResultsFile = DetailedResultsFile
    def get_InnerTests(self): return self.InnerTests
    def set_InnerTests(self, InnerTests): self.InnerTests = InnerTests
    def export(self, outfile, level, namespace_='', name_='SummaryResult'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='SummaryResult')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='SummaryResult'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='SummaryResult'):
        showIndent(outfile, level)
        outfile.write('<%sTestName>%s</%sTestName>\n' % (namespace_, quote_xml(self.get_TestName()), namespace_))
        showIndent(outfile, level)
        outfile.write('<%sTestResult>%s</%sTestResult>\n' % (namespace_, quote_xml(self.get_TestResult()), namespace_))
        if self.get_ErrorMessage() != None :
            if self.get_ErrorMessage() != "" :
                showIndent(outfile, level)
                outfile.write('<%sErrorMessage>%s</%sErrorMessage>\n' % (namespace_, quote_xml(self.get_ErrorMessage()), namespace_))
        if self.get_DetailedResultsFile() != None :
            if self.get_DetailedResultsFile() != "" :
                showIndent(outfile, level)
                outfile.write('<%sDetailedResultsFile>%s</%sDetailedResultsFile>\n' % (namespace_, quote_xml(self.get_DetailedResultsFile()), namespace_))
        if self.get_InnerTests() != None :
            if self.InnerTests:
                self.InnerTests.export(outfile, level, namespace_, name_='InnerTests')
    def exportLiteral(self, outfile, level, name_='SummaryResult'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('TestName=%s,\n' % quote_python(self.get_TestName()))
        showIndent(outfile, level)
        outfile.write('TestResult=%s,\n' % quote_python(self.get_TestResult()))
        showIndent(outfile, level)
        outfile.write('ErrorMessage=%s,\n' % quote_python(self.get_ErrorMessage()))
        showIndent(outfile, level)
        outfile.write('DetailedResultsFile=%s,\n' % quote_python(self.get_DetailedResultsFile()))
        if self.InnerTests:
            showIndent(outfile, level)
            outfile.write('InnerTests=InnerTests(\n')
            self.InnerTests.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'TestName':
            TestName_ = ''
            for text__content_ in child_.childNodes:
                TestName_ += text__content_.nodeValue
            self.TestName = TestName_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'TestResult':
            TestResult_ = ''
            for text__content_ in child_.childNodes:
                TestResult_ += text__content_.nodeValue
            self.TestResult = TestResult_
            self.validate_TestResult(self.TestResult)    # validate type TestResult
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'ErrorMessage':
            ErrorMessage_ = ''
            for text__content_ in child_.childNodes:
                ErrorMessage_ += text__content_.nodeValue
            self.ErrorMessage = ErrorMessage_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'DetailedResultsFile':
            DetailedResultsFile_ = ''
            for text__content_ in child_.childNodes:
                DetailedResultsFile_ += text__content_.nodeValue
            self.DetailedResultsFile = DetailedResultsFile_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'InnerTests':
            obj_ = InnerTests.factory()
            obj_.build(child_)
            self.set_InnerTests(obj_)
# end class SummaryResult


class InnerTests(object):
    subclass = None
    superclass = None
    def __init__(self, InnerTest=None):
        if InnerTest is None:
            self.InnerTest = []
        else:
            self.InnerTest = InnerTest
    def factory(*args_, **kwargs_):
        if InnerTests.subclass:
            return InnerTests.subclass(*args_, **kwargs_)
        else:
            return InnerTests(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_InnerTest(self): return self.InnerTest
    def set_InnerTest(self, InnerTest): self.InnerTest = InnerTest
    def add_InnerTest(self, value): self.InnerTest.append(value)
    def insert_InnerTest(self, index, value): self.InnerTest[index] = value
    def export(self, outfile, level, namespace_='', name_='InnerTests'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='InnerTests')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='InnerTests'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='InnerTests'):
        for InnerTest_ in self.get_InnerTest():
            InnerTest_.export(outfile, level, namespace_, name_='InnerTest')
    def exportLiteral(self, outfile, level, name_='InnerTests'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('InnerTest=[\n')
        level += 1
        for InnerTest in self.InnerTest:
            showIndent(outfile, level)
            outfile.write('InnerTest(\n')
            InnerTest.exportLiteral(outfile, level)
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'InnerTest':
            obj_ = InnerTest.factory()
            obj_.build(child_)
            self.InnerTest.append(obj_)
# end class InnerTests


class InnerTest(object):
    subclass = None
    superclass = None
    def __init__(self, TestName='', TestResult='', ErrorMessage='', DetailedResultsFile=''):
        self.TestName = TestName
        self.TestResult = TestResult
        self.ErrorMessage = ErrorMessage
        self.DetailedResultsFile = DetailedResultsFile
    def factory(*args_, **kwargs_):
        if InnerTest.subclass:
            return InnerTest.subclass(*args_, **kwargs_)
        else:
            return InnerTest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_TestName(self): return self.TestName
    def set_TestName(self, TestName): self.TestName = TestName
    def get_TestResult(self): return self.TestResult
    def set_TestResult(self, TestResult): self.TestResult = TestResult
    def validate_TestResult(self, value):
        # validate type TestResult
        pass
    def get_ErrorMessage(self): return self.ErrorMessage
    def set_ErrorMessage(self, ErrorMessage): self.ErrorMessage = ErrorMessage
    def get_DetailedResultsFile(self): return self.DetailedResultsFile
    def set_DetailedResultsFile(self, DetailedResultsFile): self.DetailedResultsFile = DetailedResultsFile
    def export(self, outfile, level, namespace_='', name_='InnerTest'):
        showIndent(outfile, level)
        outfile.write('<%s%s' % (namespace_, name_))
        self.exportAttributes(outfile, level, namespace_, name_='InnerTest')
        outfile.write('>\n')
        self.exportChildren(outfile, level + 1, namespace_, name_)
        showIndent(outfile, level)
        outfile.write('</%s%s>\n' % (namespace_, name_))
    def exportAttributes(self, outfile, level, namespace_='', name_='InnerTest'):
        pass
    def exportChildren(self, outfile, level, namespace_='', name_='InnerTest'):
        showIndent(outfile, level)
        outfile.write('<%sTestName>%s</%sTestName>\n' % (namespace_, quote_xml(self.get_TestName()), namespace_))
        showIndent(outfile, level)
        outfile.write('<%sTestResult>%s</%sTestResult>\n' % (namespace_, quote_xml(self.get_TestResult()), namespace_))
        if self.get_ErrorMessage() != None :
            if self.get_ErrorMessage() != "" :
                showIndent(outfile, level)
                outfile.write('<%sErrorMessage>%s</%sErrorMessage>\n' % (namespace_, quote_xml(self.get_ErrorMessage()), namespace_))
        if self.get_DetailedResultsFile() != None :
            if self.get_DetailedResultsFile() != "" :
                showIndent(outfile, level)
                outfile.write('<%sDetailedResultsFile>%s</%sDetailedResultsFile>\n' % (namespace_, quote_xml(self.get_DetailedResultsFile()), namespace_))
    def exportLiteral(self, outfile, level, name_='InnerTest'):
        level += 1
        self.exportLiteralAttributes(outfile, level, name_)
        self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, name_):
        pass
    def exportLiteralChildren(self, outfile, level, name_):
        showIndent(outfile, level)
        outfile.write('TestName=%s,\n' % quote_python(self.get_TestName()))
        showIndent(outfile, level)
        outfile.write('TestResult=%s,\n' % quote_python(self.get_TestResult()))
        showIndent(outfile, level)
        outfile.write('ErrorMessage=%s,\n' % quote_python(self.get_ErrorMessage()))
        showIndent(outfile, level)
        outfile.write('DetailedResultsFile=%s,\n' % quote_python(self.get_DetailedResultsFile()))
    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)
    def buildAttributes(self, attrs):
        pass
    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'TestName':
            TestName_ = ''
            for text__content_ in child_.childNodes:
                TestName_ += text__content_.nodeValue
            self.TestName = TestName_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'TestResult':
            TestResult_ = ''
            for text__content_ in child_.childNodes:
                TestResult_ += text__content_.nodeValue
            self.TestResult = TestResult_
            self.validate_TestResult(self.TestResult)    # validate type TestResult
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'ErrorMessage':
            ErrorMessage_ = ''
            for text__content_ in child_.childNodes:
                ErrorMessage_ += text__content_.nodeValue
            self.ErrorMessage = ErrorMessage_
        elif child_.nodeType == Node.ELEMENT_NODE and \
            nodeName_ == 'DetailedResultsFile':
            DetailedResultsFile_ = ''
            for text__content_ in child_.childNodes:
                DetailedResultsFile_ += text__content_.nodeValue
            self.DetailedResultsFile = DetailedResultsFile_
# end class InnerTest


from xml.sax import handler, make_parser

class SaxStackElement:
    def __init__(self, name='', obj=None):
        self.name = name
        self.obj = obj
        self.content = ''

#
# SAX handler
#
class Sax_SummaryResultHandler(handler.ContentHandler):
    def __init__(self):
        self.stack = []
        self.root = None

    def getRoot(self):
        return self.root

    def setDocumentLocator(self, locator):
        self.locator = locator
    
    def showError(self, msg):
        print '*** (showError):', msg
        sys.exit(-1)

    def startElement(self, name, attrs):
        done = 0
        if name == 'SummaryResult':
            obj = SummaryResult.factory()
            stackObj = SaxStackElement('SummaryResult', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'TestName':
            stackObj = SaxStackElement('TestName', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'TestResult':
            stackObj = SaxStackElement('TestResult', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'ErrorMessage':
            stackObj = SaxStackElement('ErrorMessage', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'DetailedResultsFile':
            stackObj = SaxStackElement('DetailedResultsFile', None)
            self.stack.append(stackObj)
            done = 1
        elif name == 'InnerTests':
            obj = InnerTests.factory()
            stackObj = SaxStackElement('InnerTests', obj)
            self.stack.append(stackObj)
            done = 1
        elif name == 'InnerTest':
            obj = InnerTest.factory()
            stackObj = SaxStackElement('InnerTest', obj)
            self.stack.append(stackObj)
            done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def endElement(self, name):
        done = 0
        if name == 'SummaryResult':
            if len(self.stack) == 1:
                self.root = self.stack[-1].obj
                self.stack.pop()
                done = 1
        elif name == 'TestName':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_TestName(content)
                self.stack.pop()
                done = 1
        elif name == 'TestResult':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_TestResult(content)
                self.stack.pop()
                done = 1
        elif name == 'ErrorMessage':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_ErrorMessage(content)
                self.stack.pop()
                done = 1
        elif name == 'DetailedResultsFile':
            if len(self.stack) >= 2:
                content = self.stack[-1].content
                self.stack[-2].obj.set_DetailedResultsFile(content)
                self.stack.pop()
                done = 1
        elif name == 'InnerTests':
            if len(self.stack) >= 2:
                self.stack[-2].obj.set_InnerTests(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        elif name == 'InnerTest':
            if len(self.stack) >= 2:
                self.stack[-2].obj.add_InnerTest(self.stack[-1].obj)
                self.stack.pop()
                done = 1
        if not done:
            self.reportError('"%s" element not allowed here.' % name)

    def characters(self, chrs, start, end):
        if len(self.stack) > 0:
            self.stack[-1].content += chrs[start:end]

    def reportError(self, mesg):
        locator = self.locator
        sys.stderr.write('Doc: %s  Line: %d  Column: %d\n' % \
            (locator.getSystemId(), locator.getLineNumber(), 
            locator.getColumnNumber() + 1))
        sys.stderr.write(mesg)
        sys.stderr.write('\n')
        sys.exit(-1)
        #raise RuntimeError

USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
Options:
    -s        Use the SAX parser, not the minidom parser.
"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)


#
# SAX handler used to determine the top level element.
#
class SaxSelectorHandler(handler.ContentHandler):
    def __init__(self):
        self.topElementName = None
    def getTopElementName(self):
        return self.topElementName
    def startElement(self, name, attrs):
        self.topElementName = name
        raise StopIteration


def parseSelect(inFileName):
    infile = file(inFileName, 'r')
    topElementName = None
    parser = make_parser()
    documentHandler = SaxSelectorHandler()
    parser.setContentHandler(documentHandler)
    try:
        try:
            parser.parse(infile)
        except StopIteration:
            topElementName = documentHandler.getTopElementName()
        if topElementName is None:
            raise RuntimeError, 'no top level element'
        topElementName = topElementName.replace('-', '_').replace(':', '_')
        if topElementName not in globals():
            raise RuntimeError, 'no class for top element: %s' % topElementName
        topElement = globals()[topElementName]
        infile.seek(0)
        doc = minidom.parse(infile)
    finally:
        infile.close()
    rootNode = doc.childNodes[0]
    rootObj = topElement.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0)
    return rootObj


def saxParse(inFileName):
    parser = make_parser()
    documentHandler = Sax_SummaryResultHandler()
    parser.setDocumentHandler(documentHandler)
    parser.parse('file:%s' % inFileName)
    rootObj = documentHandler.getRoot()
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0)
    return rootObj


def saxParseString(inString):
    parser = make_parser()
    documentHandler = Sax_SummaryResultHandler()
    parser.setDocumentHandler(documentHandler)
    parser.feed(inString)
    parser.close()
    rootObj = documentHandler.getRoot()
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0)
    return rootObj


def parse(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = SummaryResult.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="SummaryResult")
    return rootObj


def parseString(inString):
    doc = minidom.parseString(inString)
    rootNode = doc.documentElement
    rootObj = SummaryResult.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="SummaryResult")
    return rootObj


def parseLiteral(inFileName):
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    rootObj = SummaryResult.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('from SummaryResult import *\n\n')
    sys.stdout.write('rootObj = SummaryResult(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="SummaryResult")
    sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-s':
        saxParse(args[1])
    elif len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')

