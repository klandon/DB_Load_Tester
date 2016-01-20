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
        except:
            print (sys.exc_info())