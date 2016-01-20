#!/usr/bin/env python

#Author : Kristopher Landon
#Release : PYODBC General class for MSSQL,Vertica
#Release # : 3.1.0
#Original Date : 02/24/2014
#License : Not for public release 

import sys
import pyodbc
import os
import xml.etree.ElementTree as ET
from pydal import DataSource
import time
import codecs
import pymssql
import psycopg2
import vertica_python

class DataAccessLayer:
    ''' Class to be used for database access leverage psycopg2 vertica_python pymssql pyodbc class is now deprecaed use DataAccessLayer2'''

    def __init__(self,settingsfile):
        "Standard init for class must have the server settings xml file"
        #Generate local repo for databases settings
        self.datasources = self.load_settings_file(settingsfile)
 
 
 ######### Internal Methods #########       

        #create new db connection based on the source name

    #create conn
    def create_new_conn(self,datasourceName,is_autocommit = True):
        try:
            #Load Data source by name
            dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)

            #load params incase of the data source type
            newConn_param = self.get_direct_con_settings(datasourceName)

            #Decide which class to instantuate
            if dsource.databaseType.lower() == 'postgresql' and dsource.connectionType.lower() == 'direct':
                newConn = psycopg2.connect(host=newConn_param['server'],port=newConn_param['port'],database=newConn_param['database'],user=newConn_param['uid'],password=newConn_param['pwd'])
                newConn.autocommit(is_autocommit)
            if dsource.databaseType.lower() == 'redshift' and dsource.connectionType.lower() == 'direct':
                newConn = psycopg2.connect(host=newConn_param['server'],port=newConn_param['port'],database=newConn_param['database'],user=newConn_param['uid'],password=newConn_param['pwd'])
                newConn.autocommit(is_autocommit)
            if dsource.databaseType.lower() == 'vertica' and dsource.connectionType.lower() == 'direct':
                newConn = vertica_python.connect(host=newConn_param['server'],port=newConn_param['port'],database=newConn_param['database'],user=newConn_param['uid'],password=newConn_param['pwd'])
                newConn.autocommit(is_autocommit)
            if dsource.databaseType.lower() == 'mssql' and dsource.connectionType.lower() == 'direct':
                newConn = pymssql.connect(host=newConn_param['server'],port=newConn_param['port'],database=newConn_param['database'],user=newConn_param['uid'],password=newConn_param['pwd'])
                newConn.autocommit(is_autocommit)
            else:
                newConn = pyodbc.connect(dsource.connectionString,autocommit=is_autocommit)
        except:
            if newConn is None:
                print("Connection could not be made please check your configuration settings or that the server is alive")
                print(sys.exc_info())
        finally:
            return newConn
    #Load Connection Settings from XML
    def load_settings_file(self,fileName):
        sourcesList = []
        dict = {}
        try:
            if os.path.isfile(fileName):
                tree = ET.parse(fileName).getroot()
                for server in tree.findall('server'):
                    dict.clear();
                    dict.update({'name':server.find('./name').text})
                    dict.update({'connectionType':server.find('./connectionType').text})
                    dict.update({'databaseType':server.find('./databaseType').text})
                    dict.update({'connectionString':server.find('./connectionString').text})
                    dict.update({'versionQuery':server.find('./versionQuery').text})
                    sourcesList.append(DataSource.Source(dict))  
            else:
                raise Exception('Missing Settings File')
            return sourcesList
        except:
            print (sys.exc_info()) 
            sys.exit(-1)
    #Check query for safety
    def check_query(self,queryToCheck):
        safe = 0
        try:
            if 'INSERT' in queryToCheck.upper() or 'DELETE' in queryToCheck.upper() or 'DROP' in queryToCheck.upper() or 'ALTER' in queryToCheck.upper() or 'TRUNCATE' in queryToCheck.upper() or 'UPDATE' in queryToCheck.upper() :
                safe = 0
            else:
                safe = 1
        except:
            print (sys.exc_info()) 
            sys.exit(-1)
        return safe
    
######### Internal Methods ######### 
 
######### Extenal Methods #########

    #Print List of data source
    def print_list_of_ds(self):
        "Print List of the loaded data sources"
        i = 0
        try:
            for ds in self.datasources:
                print('#################### ' + str(i) +' ####################' )
                print(self.datasources.index(ds))
                print('Reference Name : ' + ds.name)
                print('Connection Type : ' +ds.connectionType)
                print('Database Type : ' +ds.databaseType)
                print('Is Recognized as MSSQL : ' + str(ds.is_mssql))
                print('Connection String : ' +ds.connectionString)
                print('Version Query : ' +ds.versionQuery)
                print('#################### ' + str(i) +' ####################' )
                i = i + 1
        except:
            print (sys.exc_info()) 
            sys.exit(-1)       
      
    #Test connection of a single data source

    #explode the ODBC conn string for direct connections
    def get_direct_con_settings(self,datasourceName):
        "Get list of direct connect settings"
        dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)
        source_string = dsource.connectionString
        split_params = {}
        try:
            for setting in source_string.split(";"):
                nd = dict(setting.split("=") for kv in setting)
                if len(nd) > 0:
                    (nk,nv), = nd.items()
                    split_params[str(nk).lower()] = nv
        except:
            print(sys.exc_info())
        finally:
            return split_params

    #general connection test
    def test_conn(self,testsource):
        try:
            dsource = next((ds for ds in self.datasources if ds.name == testsource),None)
            newConn = self.create_new_conn(dsource.name)
            cursor = newConn.cursor()
            cursor.execute(dsource.versionQuery)
            row = cursor.fetchone()
            if row:
                print ('version:',row[0])
            newConn.close()         
        except:
            print(sys.exc_info())
            sys.exit(-1)  
    
    #Test All connections for servers in settings file

    #test all data source connections in settings file
    def test_all_connections(self):
        while True:
            for rotatingSource in self.datasources:
                try:
                    print('#################### ' + rotatingSource.name +' ####################' )
                    print('Testing Connection for source and getting version info for  : ' + rotatingSource.name)
                    newConn = self.create_new_conn(rotatingSource)
                    cursor = newConn.cursor()
                    cursor.execute(rotatingSource.versionQuery)
                    row = cursor.fetchone()
                    if row:
                        print ('version:',codecs.decode(row[0],'UTF-16'))
                    newConn.close()
                    print('#################### ' + rotatingSource.name +' ####################' )
                except:
                    print(sys.exc_info())
                    continue
            break

    #databases to report -1 after a select statement for performance reasons
    def execute_test_time_only_cp(self,query,datasourceName,skipValidation,odbcConnection):
        if bool(self.check_query(query)) == 1 or skipValidation == 1:
            totalTime = 0
            try:
                tic = time.clock()
                cursor = odbcConnection.cursor()
                SomethingToHoldResultinMem = cursor.execute(query).rowcount       
                toc = time.clock()
                totalTime = toc - tic
            except:
                print(sys.exc_info())
                sys.exit(-1) 
            return totalTime

    #return scalar returns single value Value (first column of first row)
    def execute_scalar(self,query,datasourceName,skipValidation):
        scalarValue = None
        if bool(self.check_query(query)) == 1 or skipValidation == 1:
            try:
                newConn = self.create_new_conn(datasourceName)
                cursor = newConn.cursor()
                cursor.execute(query)
                row = cursor.fetchone()
                if row:
                    scalarValue = row[0]
                newConn.commit()
                newConn.close()         
            except:
                print(sys.exc_info())
                sys.exit(-1) 
            return scalarValue 
              
    #return set

     #return scalar returns single value Value (first column of first row)

    #execute scaler no return
    def execute_scalar_noreturn(self,query,datasourceName,skipValidation):
        scalarValue = None
        if bool(self.check_query(query)) == 1 or skipValidation == 1:
            try:
                newConn = self.create_new_conn(datasourceName)
                cursor = newConn.cursor()
                cursor.execute(query)
                newConn.commit()
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1)
            return scalarValue

    #return data set reader
    def execute_reader(self,query,datasourceName,skipValidation):
        dbReader = None
        if bool(self.check_query(query)) == 1 or skipValidation == 1:
            try:
                newConn = self.create_new_conn(datasourceName)
                cursor = newConn.cursor()
                cursor.execute(query)
                dbReader = cursor.fetchall()
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1) 
            return dbReader

    #Load Batch
    def load_batch(self,query,query_params,datasourceName,skipValidation):
        if bool(self.CheckQuery(query)) == 1 or skipValidation == 1:
            try:
                newConn = self.create_new_conn(datasourceName)
                cursor = newConn.cursor()
                cursor.executemany(query,query_params)
                newConn.commit()
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1)

    #databases to report -1 after a select statement for performance reasons
    def execute_row_count(self,query,datasourceName,skipValidation):
        dbRowCouter = None
        if bool(self.check_query(query)) == 1 or skipValidation == 1:
            try:
                newConn = self.create_new_conn(datasourceName)
                cursor = newConn.cursor()
                dbRowCouter = cursor.execute(query).rowcount  
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1) 
            return dbRowCouter

    #execute time test only
    def execute_time_test_only(self,query,datasourceName,skipValidation):
        if bool(self.check_query(query)) == 1 or skipValidation == 1:
            totalTime = 0
            try:
                tic = time.clock()
                newConn = self.create_new_conn(datasourceName)
                cursor = newConn.cursor()
                SomethingToHoldResultinMem = cursor.execute(query).rowcount  
                newConn.close()
                toc = time.clock()
                totalTime = toc - tic
            except:
                print(sys.exc_info())
                sys.exit(-1) 
            return totalTime

    #check param for SQL style injection issue
    def check_param_for_safety(self,paramToBeChecked):

        listOfUnsafeWords = ["INSERT","DROP","CREATE","LOGIN","DELETE","TRUNCATE",";","CREATE","DATABASE"]

        allParamsPassed = False

        try:
            for sqlParam,sqlParamValue in paramToBeChecked.items():
                for word in listOfUnsafeWords:
                    if word in sqlParamValue.upper():
                        raise Exception("Parameter : " + sqlParam + " contains un-safe keyword " + word +" please revise or seek assistance!")
                    else:
                        allParamsPassed = True
        except Exception as eX:
            print(eX.message + "\n" + str(sys.exc_info()))
            sys.exit(-1)

        return allParamsPassed

    #open connection execution for non conn handled processes without a return set
    def execute_openconn_process(self,query_to_run,database_connection,is_commit = True):
        try:
            cursor = database_connection.cursor()
            cursor.execute(query_to_run)
            if is_commit == True:
                database_connection.commit()

        except:
            print("Issue executing command : " + query_to_run)
            print(sys.exc_info())

    #open connection execution for non conn handled processes with return sets
    def execute_openconn_process_with_return(self,query_to_run,database_connection,is_commit = True):
        return_set = None
        try:
            cursor = database_connection.cursor()
            return_set = cursor.execute(query_to_run)
            if is_commit == True:
                database_connection.commit()
        except:
            print("Issue executing command : " + query_to_run)
            print(sys.exc_info())

        finally:
            return return_set


############################### DEPRECATED SOON Do Not Use ###############################

      #Load Connection Settings from XML

    #Check query for safety
    def CheckQuery(self,queryToCheck):
        "Method is deprecated please do not use"
        safe = 0
        try:
            if 'INSERT' in queryToCheck.upper() or 'DELETE' in queryToCheck.upper() or 'DROP' in queryToCheck.upper() or 'ALTER' in queryToCheck.upper() or 'TRUNCATE' in queryToCheck.upper() or 'UPDATE' in queryToCheck.upper() :
                safe = 0
            else:
                safe = 1
        except:
            print (sys.exc_info())
            sys.exit(-1)
        return safe

    #load settings from server settings file xml
    def LoadSettingsFile(self,fileName):
        "Method is deprecated please do not use"
        sourcesList = []
        dict = {}
        try:
            if os.path.isfile(fileName):
                tree = ET.parse(fileName).getroot()
                for server in tree.findall('server'):
                    dict.clear();
                    dict.update({'name':server.find('./name').text})
                    dict.update({'connectionType':server.find('./connectionType').text})
                    dict.update({'databaseType':server.find('./databaseType').text})
                    dict.update({'connectionString':server.find('./connectionString').text})
                    dict.update({'versionQuery':server.find('./versionQuery').text})
                    sourcesList.append(DataSource.Source(dict))
            else:
                raise Exception('Missing Settings File')
            return sourcesList
        except:
            print (sys.exc_info())
            sys.exit(-1)


######### soon to be deprecated do not use #######
######### Extenal Methods #########

    #Print List of data source
    def PrintListOfDS(self):
        "Method is deprecated please do not use"
        i = 0
        try:
            for ds in self.datasources:
                print('#################### ' + str(i) +' ####################' )
                print(self.datasources.index(ds))
                print('Reference Name : ' + ds.name)
                print('Connection Type : ' +ds.connectionType)
                print('Database Type : ' +ds.databaseType)
                print('Connection String : ' +ds.connectionString)
                print('Version Query : ' +ds.versionQuery)
                print('#################### ' + str(i) +' ####################' )
                i = i + 1
        except:
            print (sys.exc_info())
            sys.exit(-1)

    #Test connection of a single data source
    def TestConn(self,testsource):
        "Method is deprecated please do not use"
        try:
            dsource = next((ds for ds in self.datasources if ds.name == testsource),None)
            newConn = pyodbc.connect(dsource.connectionString)
            cursor = newConn.cursor()
            cursor.execute(dsource.versionQuery)
            row = cursor.fetchone()
            if row:
                print ('version:',codecs.decode(row[0],'UTF-16'))
            newConn.close()
        except:
            print(sys.exc_info())
            sys.exit(-1)

    #Test All connections for servers in settings file
    def TestAllConnections(self):
        "Method is deprecated please do not use"
        try:
            for rotatingSource in self.datasources:
                print('#################### ' + rotatingSource.name +' ####################' )
                print('Testing Connection for source and getting version info for  : ' + rotatingSource.name)
                newConn = pyodbc.connect(rotatingSource.connectionString)
                cursor = newConn.cursor()
                cursor.execute(rotatingSource.versionQuery)
                row = cursor.fetchone()
                if row:
                    print ('version:',codecs.decode(row[0],'UTF-16'))
                newConn.close()
                print('#################### ' + rotatingSource.name +' ####################' )
        except:
            print(sys.exc_info())
            sys.exit(-1)

    #Connection for connection pooling use
    def CreateConnectionPool(self,datasourceName):
        "Method is deprecated please do not use"
        try:
            dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)
            newconn = pyodbc.connect(dsource.connectionString,autocommit=True)
        except:
            print(sys.exc_info())
            sys.exit(-1)
        return newconn

    #databases to report -1 after a select statement for performance reasons
    def ExecuteTestTimeOnlyCP(self,query,datasourceName,skipValidation,odbcConnection):
        "Method is deprecated please do not use"
        if bool(self.CheckQuery(query)) == 1 or skipValidation == 1:
            totalTime = 0
            try:
                tic = time.clock()
                cursor = odbcConnection.cursor()
                SomethingToHoldResultinMem = cursor.execute(query).rowcount
                toc = time.clock()
                totalTime = toc - tic
            except:
                print(sys.exc_info())
                sys.exit(-1)
            return totalTime

    #return scalar returns single value Value (first column of first row)
    def ExecuteScalar(self,query,datasourceName,skipValidation):
        "Method is deprecated please do not use"
        scalarValue = None
        if bool(self.CheckQuery(query)) == 1 or skipValidation == 1:
            try:
                dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)
                newConn = pyodbc.connect(dsource.connectionString,autocommit=True)
                cursor = newConn.cursor()
                cursor.execute(query)
                row = cursor.fetchone()
                if row:
                    scalarValue = row[0]
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1)
            return scalarValue

    #return set
    def ExecuteReader(self,query,datasourceName,skipValidation):
        "Method is deprecated please do not use"
        dbReader = None
        if bool(self.CheckQuery(query)) == 1 or skipValidation == 1:
            try:
                dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)
                newConn = pyodbc.connect(dsource.connectionString,autocommit=True)
                cursor = newConn.cursor()
                cursor.execute(query)
                dbReader = cursor.fetchall()
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1)
            return dbReader

    #databases to report -1 after a select statement for performance reasons
    def ExecuteRowCount(self,query,datasourceName,skipValidation):
        "Method is deprecated please do not use"
        dbRowCouter = None
        if bool(self.CheckQuery(query)) == 1 or skipValidation == 1:
            try:
                dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)
                newConn = pyodbc.connect(dsource.connectionString,autocommit=True)
                cursor = newConn.cursor()
                dbRowCouter = cursor.execute(query).rowcount
                newConn.close()
            except:
                print(sys.exc_info())
                sys.exit(-1)
            return dbRowCouter

    #databases to report -1 after a select statement for performance reasons
    def ExecuteTestTimeOnly(self,query,datasourceName,skipValidation):
        "Method is deprecated please do not use"
        if bool(self.CheckQuery(query)) == 1 or skipValidation == 1:
            totalTime = 0
            try:
                dsource = next((ds for ds in self.datasources if ds.name == datasourceName),None)
                tic = time.clock()
                newConn = pyodbc.connect(dsource.connectionString,autocommit=True)
                cursor = newConn.cursor()
                SomethingToHoldResultinMem = cursor.execute(query).rowcount
                newConn.close()
                toc = time.clock()
                totalTime = toc - tic
            except:
                print(sys.exc_info())
                sys.exit(-1)
            return totalTime

    #check param for SQL style injection issue
    def CheckParamForSafety(self,paramToBeChecked):
        "Method is deprecated please do not use"

        listOfUnsafeWords = ["INSERT","DROP","CREATE","LOGIN","DELETE","TRUNCATE",";","CREATE","DATABASE"]

        allParamsPassed = False

        try:
            for sqlParam,sqlParamValue in paramToBeChecked.items():
                for word in listOfUnsafeWords:
                    if word in sqlParamValue.upper():
                        raise Exception("Parameter : " + sqlParam + " contains un-safe keyword " + word +" please revise or seek assistance!")
                    else:
                        allParamsPassed = True
        except Exception as eX:
            print(eX.message + "\n" + str(sys.exc_info()))
            sys.exit(-1)

        return allParamsPassed


