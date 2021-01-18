from DatabaseOperation import  DatabaseOperation

from ImportSettings import ImportSettings

class CreateTableFromFile:
    def __init__(self):
        self.__tablesDir= ImportSettings().tablesDirectory
        return 

    def CreateTable(self,fileName):
        with open(self.__tablesDir+fileName,'r') as file:
            fileStr = ''
            for line in file.readlines():
                line = line.strip()
                fileStr += line

            fileStr = "create table if not exists "+ fileName + ' ('+ fileStr + ');'
            dbOp = DatabaseOperation()
            dbOp.ExcuteSQL(fileStr)
        return 0
    

x= CreateTableFromFile()
x.CreateTable("stock_basic")


    
