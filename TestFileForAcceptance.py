#!/usr/bin/env python
#Author : Kristopher Landon
#Release : Vertica Load Tester Beta
#Release # : 0.0.1
#Date : 12/10/2013
#License : Not for public release 


import sys
import FileHandler


try:
	testFileArg = sys.argv[1]
except:
	print 'No test file passed as arg 1 or testfile is not readable'
	sys.exit()
else:
	print 'Testing ' + str(testFileArg) + ' file for acceptance'

print 'Continuing to check for encoding'

#test file for encoding
testHandler = FileHandler.FileProcessor()

isAccepted = testHandler.CheckFileFormat(testFileArg)

print str(isAccepted)

print 'List of statements accepted'

scriptList = testHandler.ParseFile(testFileArg)

for idx,item in enumerate(scriptList):
	print 'Query #' + str(idx + 1) + ' ' + item + '\n'
