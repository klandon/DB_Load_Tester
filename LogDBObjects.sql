
/****** Object:  Table [dbo].[PythonLoadTesting]    Script Date: 7/25/2014 1:43:07 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[PythonLoadTesting](
	[PythonLoadTesting] [bigint] IDENTITY(1,1) NOT NULL,
	[TestName] [varchar](255) NOT NULL,
	[EntryDate] [datetime] NOT NULL,
	[QueryID] [int] NOT NULL,
	[QueryTime] [numeric](10, 5) NULL,
PRIMARY KEY CLUSTERED 
(
	[PythonLoadTesting] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[PythonLoadTesting] ADD  DEFAULT (getdate()) FOR [EntryDate]
GO


/****** Object:  Table [dbo].[PythonLoadTestingQueries]    Script Date: 7/25/2014 1:43:22 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[PythonLoadTestingQueries](
	[PythonLoadTestingQueries] [bigint] IDENTITY(1,1) NOT NULL,
	[TestName] [varchar](255) NULL,
	[EntryDate] [datetime] NOT NULL,
	[QueryID] [int] NULL,
	[Query] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[PythonLoadTestingQueries] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[PythonLoadTestingQueries] ADD  DEFAULT (getdate()) FOR [EntryDate]
GO

/****** Object:  StoredProcedure [dbo].[usp_GetLoadTestResults]    Script Date: 7/25/2014 1:43:46 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


/** ==================================================================================================================
Description		:	
	
Modification Log
By					Date		Description
---------------------------------------------------------------------------------------------------------------------
Kristopher Landon   06/04/2014	Show Stats from load test   
================================================================================================================== **/
CREATE PROCEDURE [dbo].[usp_GetLoadTestResults]
--params 
@TestName AS VARCHAR(255)
,@TestName2 AS VARCHAR(255)
AS
BEGIN

	SET NOCOUNT ON;
--Begin Work	
	BEGIN TRY
		
		SELECT DISTINCT  PythonLoadTestingQueries ,
		        TestName ,
		        EntryDate ,
		        QueryID ,
		        Query
		FROM dbo.PythonLoadTestingQueries
		WHERE TestName = @TestName
			OR TestName = @TestName2

		IF OBJECT_ID(N'tempdb..#FirstResult') IS NOT NULL
		DROP TABLE #FirstResult
		IF OBJECT_ID(N'tempdb..#SecondResult') IS NOT NULL
		DROP TABLE #SecondResult

		SELECT QueryID
				,MIN(QueryTime) AS  'Minimum'
				, AVG(QueryTime) AS 'Average'
				, MAX(QueryTime) AS 'Maximum'
				,COUNT(QueryID) AS 'NumberOfExecutions'
		INTO #FirstResult
		FROM dbo.PythonLoadTesting WITH(NOLOCK) 
		WHERE TestName = @TestName
		GROUP BY QueryID
		ORDER BY QueryID ASC


		SELECT QueryID
				,MIN(QueryTime) AS  'Minimum'
				, AVG(QueryTime) AS 'Average'
				, MAX(QueryTime) AS 'Maximum'
				,COUNT(QueryID) AS 'NumberOfExecutions'
		INTO #SecondResult
		FROM dbo.PythonLoadTesting WITH(NOLOCK) 
		WHERE TestName = @TestName2
		GROUP BY QueryID
		ORDER BY QueryID ASC


		SELECT  fr.QueryID ,
				fr.Minimum AS FirstTestMin ,
				fr.Average AS FirstTestAVG,
				fr.Maximum AS FirstTestMAx,
				fr.NumberOfExecutions AS FirstTestExecs,
				sr.Minimum AS SecondTestMin ,
				sr.Average AS SecondTestAvg,
				sr.Maximum AS SecondTestMax,
				sr.NumberOfExecutions AS SecondTestExec,
				fr.Minimum - sr.Minimum AS MinChange,
				fr.Average - sr.Average AS AvgChange,
				fr.Maximum - sr.Maximum AS MaxChange,
				fr.NumberOfExecutions - fr.NumberOfExecutions AS DifferenceInExecs
		FROM #FirstResult AS fr
		LEFT OUTER JOIN #SecondResult AS sr
			ON fr.QueryID = sr.QueryID
		ORDER BY fr.QueryID



		SELECT COUNT(*) AS 'TotalNumberOfExecutionsTest1'
		FROM dbo.PythonLoadTesting WITH(NOLOCK)
		WHERE TestName = @TestName

		SELECT COUNT(*) AS 'TotalNumberOfExecutionsTest2'
		FROM dbo.PythonLoadTesting WITH(NOLOCK)
		WHERE TestName = @TestName2

	END TRY
--Catch errors and return to user
	BEGIN CATCH			

			DECLARE  @ErrMsg nvarchar ( 4000 ),  @ErrSeverity int
			SELECT  @ErrMsg =   ERROR_MESSAGE (),  @ErrSeverity =   ERROR_SEVERITY ()
			RAISERROR ( @ErrMsg ,  @ErrSeverity ,  16 )
			RETURN			
	END CATCH

END 


GO


