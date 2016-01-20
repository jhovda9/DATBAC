import os
import unittest
import sys
import argparse
import csv
import traceback
import SummaryResult as sm
import TestDef
import testengineexception

def GetIterationParameters(filename):
	
	globalparams = {}
	iterationparameters = []

	if os.path.isfile( filename ):
		csv_file = csv.DictReader(open(filename, 'rb'), delimiter=';')
	
		#get a list of all global parameters
		tmp_globalparamlist = []
		for key in csv_file.fieldnames:
			if "global_" in key:
				tmp_globalparamlist.append(key)
	
		#copy all global parameters to globalparams
		#and the rest to iterationparameters
		for line in csv_file:
			for item in tmp_globalparamlist:
				if line[item]:
					if not item in globalparams:	#add only first occurence
						globalparams.update({item:line[item]})
				line.pop(item)
			iterationparameters.append(line)	

	return (globalparams,iterationparameters)

def main():
	testrunner_parser = argparse.ArgumentParser(description='Process arguments.....', fromfile_prefix_chars='@')
	testrunner_parser.add_argument('--testengine', type=str)

	testdeploydir = os.path.abspath(os.environ['TestDeploymentDir'])
	testoutputdir = os.path.abspath(os.environ['TestOutputDirectory'])
	softwareDropLocation = os.path.abspath(os.environ['TestLocation'])

	optionsfilename = '@' + os.path.join(testdeploydir, 'options.txt')
	testrunnerArgs, testEngineArgs = testrunner_parser.parse_known_args([optionsfilename])
	iterationParameters = os.path.join(testdeploydir, 'iterationparameters.csv')

	testResult=[]
	totalResult = sm.SummaryResult( testrunnerArgs.testengine, TestDef.TEST_INPROGRESS, 'No message')
	innerTests = sm.InnerTests()


	try:
		try:
			globalParams,iterationParams = GetIterationParameters(iterationParameters)
		except Exception as e:
			raise testengineexception.TestEngineError("Extract global parameter error:  %s" %(e) )
		#Create one instance of the correct test instance

		try:
			testModule = __import__(testrunnerArgs.testengine)  
			testClass = testModule.TestClass(testEngineArgs, testrunnerArgs.testengine, testoutputdir, softwareDropLocation)
		except Exception as e:
			raise testengineexception.TestEngineError("Import / instantiate testengine %s error: %s" %(testrunnerArgs.testengine, e) )

		#Run the test
		try:
			testClass.InitTest()
		except Exception as e:
			raise testengineexception.TestEngineError("InitTest %s error: %s" %(testrunnerArgs.testengine, e) )

		try:
			testClass.ApplyGlobalParameters(globalParams)
		except Exception as e:
			raise testengineexception.TestEngineError("ApplyGlobalParameters %s error: %s" %(testrunnerArgs.testengine, e) )
	
		try:
			#make sure we run the iteraion at least once, even if no iterations are given:
			if len(iterationParams) == 0:
				testClass.RunTestIteration( {}, 1)
			else:
				for counter,paramset in enumerate(iterationParams, start=1):
					testClass.RunTestIteration(paramset, counter)
		except Exception as e:
			raise testengineexception.TestEngineError("RunTestIteration %s error: %s" %(testrunnerArgs.testengine, e) )
	
		try:
			testClass.CleanUpTest()
		except Exception as e:
			raise testengineexception.TestEngineError("CleanUpTest %s error: %s" %(testrunnerArgs.testengine, e) )
	
		try:
			testResult = testClass.GetTestResult()
		except Exception as e:
			raise testengineexception.TestEngineError("GetTestResult %s error: %s" %(testrunnerArgs.testengine, e) )

	except testengineexception.TestEngineError as e:
		totalResult.set_TestResult( TestDef.TEST_ABORTED )
		stackTraceString = traceback.format_exc()
		totalResult.set_ErrorMessage( '%s\n%s' %(e, stackTraceString) )

	else:
		if totalResult.get_TestResult() != '':
			globalResult = totalResult.get_TestResult()
		else:
			globalResult = TestDef.TEST_PASSED
		testsPassed = 0
		testsWarning = 0
		testsError = 0
		testsAborted = 0
		totalTests = len(testResult)
		errMsg = ''
		for item in testResult:
			if item.get_TestResult() in TestDef.TestInProgressGroup or item.get_TestResult() in TestDef.TestInPassedGroup:
				globalResult = TestDef.TEST_PASSED
				errMsg = item.get_ErrorMessage()
				testsPassed=testsPassed+1
		for item in testResult:
			if item.get_TestResult() in TestDef.TestWarningGroup:
				globalResult = TestDef.TEST_WARNING
				errMsg = item.get_ErrorMessage()
				testsWarning=testsWarning+1
		for item in testResult:
			if item.get_TestResult() in TestDef.TestErrorGroup:
				globalResult = TestDef.TEST_ERROR
				errMsg = item.get_ErrorMessage()
				testsError=testsError+1
		for item in testResult:
			if item.get_TestResult() in TestDef.TestAbortGroup:
				globalResult = TestDef.TEST_ABORTED
				errMsg = item.get_ErrorMessage()
				testsAborted=testsAborted+1
	
		finalMessage = '%s (Passed: %d/%d, Warning: %d/%d, Error: %d/%d, Abort: %d/%d)' %(errMsg, testsPassed, totalTests, testsWarning, totalTests, testsError, totalTests, testsAborted, totalTests)
		totalResult.set_TestResult( globalResult )
		totalResult.set_ErrorMessage( finalMessage )

		innerTests = sm.InnerTests()
		for item in testResult:
			innerTests.add_InnerTest( item )
		totalResult.set_InnerTests( innerTests )

	reportFilename = os.path.join( os.path.abspath( os.path.join(testoutputdir, 'NASTLauncherResult.trx')))
	outfile = open( reportFilename, 'w')
	totalResult.export(outfile, 0)
	
	return 0

		  
if __name__ == "__main__":
	sys.exit(main())
