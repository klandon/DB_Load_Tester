import sys

#Base class to hold datasources from settings file
class Source:
    def __init__(self,sourceProp):
        try:
            self.connectionType = sourceProp['connectionType']
            self.databaseType = sourceProp['databaseType']
            self.connectionString = sourceProp['connectionString']
            self.name = sourceProp['name']
            self.versionQuery = sourceProp['versionQuery']
            self.is_mssql = False
            self.mssql_server = None
            self.mssql_user = None
            self.mssql_password = None
            self.mssql_db = None
            self.mssql_port = None

            if 'mssql' in str(self.databaseType).lower() or 'freetds' in str(self.connectionString).lower():
                parse_odbc = str(self.connectionString).split(';')
                mssql_dict = dict(s.split('=') for s in filter(None,parse_odbc))
                self.is_mssql = True
                self.mssql_password = mssql_dict['PWD']
                self.mssql_server = mssql_dict['SERVER']
                self.mssql_user = mssql_dict['UID']

                #optional
                if "PORT" not in mssql_dict or mssql_dict["PORT"] == "":
                    self.mssql_port = 5433
                else:
                    self.mssql_port = mssql_dict['PORT']
                if "DATABASE" not in mssql_dict or mssql_dict["DATABASE"] == "":
                    self.mssql_db = "master"
                else:
                    self.mssql_db = mssql_dict['DATABASE']

        except:
            print (sys.exc_info())