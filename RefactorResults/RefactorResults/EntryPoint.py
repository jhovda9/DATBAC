import RefactorResults as RR
import os
path = "D:TONSofTEST"
#path = "C:/Users/matsj/Source/Repos/DATBAC/RefactorResults/RefactorResults/"
#path = "C:Users/matsj/Source/Repos/DATBAC/RefactorResults/RefactorResults/HVC02.txt"

RR.generateTestReport(path)

"""
path = "D:Dropbox/SharedBachelor2016/TestData/xm3/Mcob02Ccpu.txt"
inStamp = "2016-02-22 10:36:21,765"
print RR.locateLinesInLog(path,inStamp,3,3)

"""
