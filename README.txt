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
	*.sql : this file can have any name but all queries must be ";" terminated			
					* note each statement is consider self contained so if you need temp tables in the call
						You need to terminate the entire statement not the creation only.
						This file can reside any where on the host

Required tables for logging in SQL Server :
	All required tables and the comparison proc are locate in file LogDBObjects.sql in the directory same as StartLoadtesting.py.
	*Currently logging is only supported on MSSQL.
	
	Tables : Description
		PythonLoadTesting : Holds the test results 
								Columns : 	PythonLoadTesting (PK,"Used as ID")
											TestName 	(Passed in from CLie to identify a test, no unique restriction so be careful)
											EntryDate	(when the thread finished running the test it is auto generated on insert)
											QueryId 	(Correlates to the PythonLoadtestingQueries Table)
											QueryTime 	(The time the thread recording on how long it took to run the query and spool results)
		PythonLoadTestingQueries : Holds the queries	
								Columns	: 	PythonLoadTestingQueries(PK,"Used as ID")
											TestName 	(Passed in from CLie to identify a test, no unique restriction so be careful)
											EntryDate	(when the thread finished running the test it is auto generated on insert)
											QueryId 	(Generate by the python script based on the query as it sits in the test file ".sql")
											Query 		(the actualy TSQL statement from the query file that will be used)
		Comparison Proc : usp_GetLoadTestResults
			Sample call : exec usp_GetLoadTestResults @Testname = 'Test1_Single', @TestName2='Test1_Multi'
			Sample results set:
			QueryID     FirstTestMin                            FirstTestAVG                            FirstTestMAx                            FirstTestExecs SecondTestMin                           SecondTestAvg                           SecondTestMax                           SecondTestExec MinChange                               AvgChange                               MaxChange                               DifferenceInExecs
			----------- --------------------------------------- --------------------------------------- --------------------------------------- -------------- --------------------------------------- --------------------------------------- --------------------------------------- -------------- --------------------------------------- --------------------------------------- --------------------------------------- -----------------
			1           73.84203                                114.712324                              200.13370                               558            0.06238                                 0.225202                                3.20503                                 5469           73.77965                                114.487122                              196.92867                               0
			2           67.27255                                113.114943                              195.71413                               575            0.03499                                 0.170503                                1.35735                                 5560           67.23756                                112.944440                              194.35678                               0
			3           66.42348                                114.552576                              195.67633                               563            0.03426                                 0.177596                                1.64766                                 5552           66.38922                                114.374980                              194.02867                               0
			4           0.01619                                 0.099529                                1.20580                                 567            0.03481                                 0.074942                                1.40561                                 5659           -0.01862                                0.024587                                -0.19981                                0
			5           0.02496                                 0.103648                                1.41479                                 583            0.03170                                 0.072046                                1.38885                                 5519           -0.00674                                0.031602                                0.02594                                 0
			6           0.01605                                 0.095267                                0.89785                                 567            0.07344                                 0.145036                                1.57398                                 5572           -0.05739                                -0.049769                               -0.67613                                0
			7           0.06486                                 0.388286                                1.97369                                 584            0.03340                                 0.092620                                1.40112                                 5564           0.03146                                 0.295666                                0.57257                                 0
			8           0.08011                                 0.395574                                2.28637                                 555            0.07061                                 0.210636                                1.52364                                 5586           0.00950                                 0.184938                                0.76273                                 0
			9           0.07544                                 0.395668                                1.85943                                 577            0.03308                                 0.087850                                1.57871                                 5534           0.04236                                 0.307818                                0.28072                                 0
			10          0.01677                                 0.097845                                0.94609                                 601            0.01389                                 0.029013                                1.29998                                 5535           0.00288                                 0.068832                                -0.35389                                0
			11          0.01474                                 0.099817                                1.54554                                 556            0.01417                                 0.029543                                1.30410                                 5648           0.00057                                 0.070274                                0.24144                                 0
			12          0.01442                                 0.096347                                0.72396                                 531            0.01397                                 0.030837                                2.72711                                 5627           0.00045                                 0.065510                                -2.00315                                0
			13          0.01505                                 0.098015                                1.17200                                 544            0.01445                                 0.029179                                2.72336                                 5502           0.00060                                 0.068836                                -1.55136                                0
			14          0.01902                                 0.096211                                0.86574                                 538            0.01448                                 0.028555                                1.30266                                 5467           0.00454                                 0.067656                                -0.43692                                0
			15          0.01515                                 0.095970                                1.30859                                 547            0.01464                                 0.027992                                3.12138                                 5480           0.00051                                 0.067978                                -1.81279                                0
			16          25.54127                                226.992544                              3457.97227                              551            0.03527                                 0.098675                                1.58813                                 5543           25.50600                                226.893869                              3456.38414                              0
			17          20.87300                                213.170159                              3429.93448                              523            0.03436                                 0.099023                                3.15787                                 5640           20.83864                                213.071136                              3426.77661                              0
			18          16.82325                                205.619239                              3461.53305                              492            0.03515                                 0.100723                                1.57560                                 5544           16.78810                                205.518516                              3459.95745                              0

			TotalNumberOfExecutionsTest1
			----------------------------
			10012

			TotalNumberOfExecutionsTest2
			----------------------------
			100001


			

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
			

	
	
	