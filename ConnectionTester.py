from pydal import PyDAL
from argparser import ArgParser
import sys

a_parser = ArgParser.ArgParser(sys.argv)


a = PyDAL.DataAccessLayer(a_parser.ParsedArgs["SettingsFile"])

a.PrintListOfDS()


#a.TestConn("TestDB")

a.test_all_connections()


# result = a.ExecuteScalar('SELECT COUNT(*) from event_fact','Vertica')
# print result
# 
# result2 = a.ExecuteReader('SELECT * from event_fact limit 10','Vertica')
# for row in result2:
#     print row[0],row[1]
#     
# result = a.ExecuteRowCount('SELECT * from event_fact limit 10','Vertica')
# print result
