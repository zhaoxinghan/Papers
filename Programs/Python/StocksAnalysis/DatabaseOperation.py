import pymysql
from ImportSettings import ImportSettings
from Singleton import Singleton

class DatabaseOperation(Singleton):
    def __init__(self):
        self.__connection = None
        self.__databaseSetting = ImportSettings()
        return

    def __Connect(self):
        if(self.__connection == None):
            self.__connection = pymysql.connect(
                host=self.__databaseSetting.host,
                user=self.__databaseSetting.userName,
                password = self.__databaseSetting.password,
                database =self.__databaseSetting.dbName,
            )
            print(self.__connection)
        return self.__connection
    
    def ExcuteSQL(self,sql):
        with self.__Connect().cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.__connection.commit()
            cursor.close()
        return rows


    
        