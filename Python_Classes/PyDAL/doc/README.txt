###Python Load Tester###
###WARNING!!!!!!!!! This program can cause harm to production or targeted systems###

Command : StartLoadTesting.py

Flags : Required : Description

	Target 			: Y : Target DB from the serversettings.xml file
	TestName 		: Y : Name of the test you are running
	LogResults		: Y : Bit for do you want to log results
	LogDB			: Y : Database where to log results from the serversettings.xml
	TestFile		: Y : This should be the formatted query file, each query has to be ";" terminated
	ShowQueries 	: Y : Prints the list of queries and their ids at the beginning of the run
	Iterations		: Y : How many iteration calls you want to make
	MaxThreads		: Y : how many threads do you want to simulate *note higher the threads higher the thread wait
	ShowRemaining	: Y : show remaining iterations
	
Required Files :
	serversettings.xml : This holds all of the connection information do not change the name and it must reside in the directory of startloadtesting.py
	Somefile.sql : this file can have any name but all queries must be ";" terminated			
					* note each statement is consider self contained so if you need temp tables in the call
						You need to terminate the entire statement not the creation only.
						This file can reside any where on the host

Required tables for logging in SQL Server :
	All required tables and the comparison proc are locate in file LogDBObjects.sql in the directory same as StartLoadtesting.py.
	*Currently logging is only supported on MSSQL.
	
	Tables : Description
		PythonLoadTesting : Holds the test results 
								Columns : 	PythonLoadTesting (PK,"Used as ID")
											TestName (Passed in from CLie to identify a test, no unique restriction so be careful)
											EntryDate	(when the thread finished running the test it is auto generated on insert)
											QueryId (Correlates to the PythonLoadtestingQueries Table)
											QueryTime (The time the thread recording on how long it took to run the query and spool results)
		PythonLoadTestingQueries : Holds the queries	
								Columns	: 	PythonLoadTestingQueries(PK,"Used as ID")
											TestName (Passed in from CLie to identify a test, no unique restriction so be careful)
											EntryDate	(when the thread finished running the test it is auto generated on insert)
											QueryId (Generate by the python script based on the query as it sits in the test file ".sql")
											Query (the actualy TSQL statement from the query file that will be used)



SeverSettings.xml example :

	<servers>
		<server>
			<name>LoggingTarget</name>
			<connectionType>ODBC</connectionType>
			<databaseType>MSSQL12</databaseType>
			<connectionString>DRIVER={TDS};TDS_Version=4.2;SERVER=10.1.244.150;DATABASE=TestDB;PORT=1433;UID=kris.tester;PWD=kris.tester;</connectionString>
			<versionQuery>SELECT @@VERSION</versionQuery>
		</server>
		<server>
			<name>TestTarget</name>
			<connectionType>ODBC</connectionType>
			<databaseType>MSSQL12</databaseType>
			<connectionString>DRIVER={TDS};TDS_Version=4.2;SERVER=10.1.244.150;DATABASE=TestDB;PORT=1433;UID=kris.tester;PWD=kris.tester;</connectionString>
			<versionQuery>SELECT @@VERSION</versionQuery>
		</server>
	</servers>

		*Note the above example defines two SQL servers. You can use this against any ODBC compatible system as long as you have the correct drivers installed
			On windows the connection drive and driver for SQL will be different, you will need to set DRIVER={Microsoft SQL} or which ever ODBC driver you have for SQL,
			and you will need to remove the "TDS_Version" option from the string.
			You can define any number of connections but the tester will only use one per test for logging and one for targeting.
			

Sample Command:
	python StartLoadTesting.py Target=SFDB10 TestName=Test1_Single LogResults=1 LogDB=Logging TestFile="C:\ShareFile\KristopherLandon\My Files & Folders\Projects\Items_Partition\Testing_Beta\Test1_SingleT.txt" ShowQueries=1 Iterations=10000 MaxThreads=100 ShowRemaining=0
		Translation of command:
			The test will be ran against "SFDB10" as defined in the serversettings.xml
			You do want to log results
			You will log results into "Logging" as defined in the serversettings.xml
			The test file you are using is Test1_SingleT.txt in location as shown
			You do want to see a print out of the queries at the top of the screen refresh
			you will run 10000 iterations at 100 threads which means 100 threads will process the 10k iterations are exhausted
			you do not want to see the remaining iteration count, not this may not show on large runs if select as 1, givent the thread could execute faster that the screen refresh
			

	
	
	