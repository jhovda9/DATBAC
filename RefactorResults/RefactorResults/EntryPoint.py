import RefactorResults as RR
import os
path = "D:Dropbox/SharedBachelor2016/TestData/xm3"
root = RR.initializeTRXStructure(os.path.join(path, RR.findTRX(path)))
RR.parseInnerTest(root, path)