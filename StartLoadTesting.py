#!/usr/bin/env python
# Author : Kristopher Landon
#Release : ODBC Load Tester Beta 
#Release # : 0.0.2
#Date : 05/30/2014 
#License : Not for public release


import threading
import time
import random
import multiprocessing
import FileHandler
import sys
from pydal import PyDAL
from argparser import ArgParser
import datetime


print ('Hello, now starting the ODBC load tester script based on the query file you provided')

############ File Testing and checks ############
try:
    #dataTarget = sys.argv[1]
    #testName = sys.argv[2]
    #logResultToDB = sys.argv[3]
    #logDB = sys.argv[4]
    #testFileArg = sys.argv[5]
    #showQueries = int(sys.argv[6])
    #iterationsToRun = int(sys.argv[7])
    #maxThreads = int(sys.argv[8])
    #showProgressIterations = int(sys.argv[9])

    Args = ArgParser.ArgParser(sys.argv)
    print(Args.ParsedArgs)
    dataTarget = Args.ParsedArgs['Target']
    testName = Args.ParsedArgs['TestName']
    logResultToDB = Args.ParsedArgs['LogResults']
    logDB = Args.ParsedArgs['LogDB']
    testFileArg = Args.ParsedArgs['TestFile']
    showQueries = int(Args.ParsedArgs['ShowQueries'])
    iterationsToRun = int(Args.ParsedArgs['Iterations'])
    maxThreads = int(Args.ParsedArgs['MaxThreads'])
    showProgressIterations = int(Args.ParsedArgs['ShowRemaining'])
    settingsFile = Args.ParsedArgs["SettingsFile"]

except:
    print(sys.exc_info())
    sys.exit()

print ('Testing ' + str(testFileArg) + ' file for acceptance')
print ('Testing File ' + testFileArg + ' for bad queries and un-safe queries')
testHandler = FileHandler.FileProcessor()
isAccepted = testHandler.CheckFileFormat(testFileArg)
if isAccepted == 1:
    print ('File was accepted and seems to be in good standing order')
    scriptsToRun = testHandler.ParseFile(testFileArg)
    cleanScripts = testHandler.CheckSafeQueries(scriptsToRun)
    print (str(testHandler.qTotal) + ' Total Number of Queries : ' + str(
        testHandler.qRejected) + ' Total Number Of Rejected Queries ' + str(
        testHandler.qAccepted) + ' Total Number of Accepted Queries')
if (logResultToDB == '1'):
    print('You have selected to save the results to a database with the destination named ' + str(logDB))
    LoggingServer = PyDAL.DataAccessLayer(settingsFile)
    LoggingCommand = 'INSERT INTO python_load_testing(test_name ,query_id ,query_time)'
    LoggingQueryCommand = 'INSERT INTO python_load_test_queries(test_name, query_id, query ) '

############ File Testing and checks ############

#print testHandler.TestVar
print ('Testing ODBC connection \n')
TestServer = PyDAL.DataAccessLayer(settingsFile)
print ('Leveraging DataSources from file')
TestServer.PrintListOfDS()
print ('Trying to connect to server and retrieve DB Version :')
TestServer.TestConn(dataTarget)
print ('\n')
if showQueries == 1:
    print('Using Queries below for testing:')
    for idx, item in enumerate(cleanScripts):
        print ('Query #' + str(idx + 1) + ' ' + item + '\n')
        if (logResultToDB == '1'):
            #debugging #print (LoggingQueryCommand + " VALUES('" + str(test name) + "','" + str(idx + 1) + "','" + str(item) + "')")
            LoggingServer.ExecuteTestTimeOnly(
                LoggingQueryCommand + " VALUES('" + str(testName) + "','" + str(idx + 1) + "','" + str(item).replace(
                    "'", "''") + "')", logDB, 1)

print ('Starting Test')

#define test method
def IssueTest(idx, queryToTest):
    try:
        TotalTime = str(TestServer.ExecuteTestTimeOnly(queryToTest, dataTarget, 1))
        TestResult = 'Query ID : ' + str(idx + 1) + ' : ' + TotalTime + ' : ' + str(datetime.datetime.now())
        if (logResultToDB == '1'):
            LoggingServer.ExecuteTestTimeOnly(
                LoggingCommand + " VALUES('" + str(testName) + "','" + str(idx + 1) + "','" + str(
                    round(float(TotalTime), 8)) + "')", logDB, 1)
    except:
        print(sys.exc_info())
    print (TestResult)

#Get CPU Core Count
cpuCoreCount = str(multiprocessing.cpu_count())
print ('CPU core count ' + cpuCoreCount)

#Start Threads that need to run
currIteration = 0
threads = []

while currIteration <= iterationsToRun:
    if (threading.active_count() <= maxThreads):
        randomQiD = random.randint(0, len(cleanScripts) - 1)
        randomQ = cleanScripts[randomQiD]
        thread = threading.Thread(target=IssueTest, args=[randomQiD, randomQ])
        thread.start()
        threads.append(threads)
        currIteration += 1
    else:
        time.sleep(1)
        if (showProgressIterations == 1):
            print (
            'Current Progress ' + str(currIteration) + ' out of ' + str(iterationsToRun) + ' have been completed')







