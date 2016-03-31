#!/usr/bin/env python
#
#
#
##definition for ONE test

TEST_ABORTED =             "Aborted"
TEST_ERROR =               "Error"
TEST_INCONCLUSIVE =        "Inconclusive"
TEST_FAILED =              "Failed"
TEST_NOTRUNNABLE =         "NotRunnable"
TEST_NOTEXECUTED =         "NotExecuted"
TEST_DISCONNECTED =        "Disconnected"
TEST_WARNING =             "Warning"
TEST_INPROGRESS =          "InProgress"
TEST_PENDING =             "Pending"
TEST_PASSEDBUTRUNABORTED = "PassedButRunAborted"
TEST_COMPLETED =           "Completed"
TEST_PASSED =              "Passed"

TestAbortGroup      = [ TEST_ABORTED ]
TestErrorGroup      = [ TEST_ERROR, TEST_INCONCLUSIVE, TEST_FAILED, TEST_NOTRUNNABLE, TEST_NOTEXECUTED ]
TestWarningGroup    = [ TEST_DISCONNECTED, TEST_WARNING ]
TestInProgressGroup = [ TEST_INPROGRESS, TEST_PENDING ]
TestInPassedGroup   = [ TEST_PASSEDBUTRUNABORTED, TEST_COMPLETED, TEST_PASSED ]


#The current values we use:
TestAborted    = 0
TestError      = 1
TestWarning    = 2
TestInProgress = 3
TestPassed     = 4


#Override of a testresult for a subtest
TEST_RES_NOMODIFICATIONS = 0
TEST_RES_ALWAYSPASS = 1
TEST_RES_ALWAYSFAIL = 2
TEST_RES_PASS_WITH_WARNING_ONERROR = 3
TEST_RES_PASS_BUT_ALWAYS_WARN = 4





class TestDefinition:
		def __init__(self):
			self.TestName = "TestName"
			self.PythonScript = "PythonScript"
			self.ScriptArgs = "Args"
			self.Timeout = 0
	
class TestResult:
		def __init__(self):
			self.testNameField = "<TestName>"
			self.testResultField = "<TestResult>"
			self.errorMessageField = "<ErrorMessage>"
			self.detailedResultsFileField = "<FileName>"


