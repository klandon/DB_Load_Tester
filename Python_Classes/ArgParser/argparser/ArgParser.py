import sys  


class ArgParser:
    ParsedArgs = {}
           
    def __init__(self,SystemArgs):
        for i in range(len(sys.argv)):
            if i != 0:
                k,v = str(sys.argv[i]).split("=")
                self.ParsedArgs[k] = v

    def CheckNeededArgs(self,needArgsList):
        hasNeededArgs = False
        try:
            if set(needArgsList).issubset(self.ParsedArgs):
                hasNeededArgs = True
            else:
                hasNeededArgs = False
                raise Exception("You are missing one or more need args \n" + str(needArgsList))
        except Exception as eX:
            hasNeededArgs = False
            print(eX.message + "\n")
        return hasNeededArgs

            
            
            
 
    