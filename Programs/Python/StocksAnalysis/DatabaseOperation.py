import pymysql
from ImportSettings import ImportSettings

class DatabaseOperation:

    def __init__(self):
        return
    
    def ConnectDB(self):
        settingObj = ImportSettings()
        #settingObj.ImportJsonFile()
        connection = pymysql.connect(
            host=settingObj.host,
            user=settingObj.userName,
            password = settingObj.password,
            database =settingObj.dbName,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection:
            with connection.cursor() as cursor:
                sql = "Create table if not exists aTestTable2 (id INT NOT NULL AUTO_INCREMENT, email varchar(255) NOT NULL, PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
                cursor.execute(sql)
            connection.commit()
        
        return 0
x= DatabaseOperation()
y=x.ConnectDB()
print(y)

