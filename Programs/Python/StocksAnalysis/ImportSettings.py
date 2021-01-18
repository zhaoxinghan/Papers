import json
import os
from Singleton import Singleton

class ImportSettings:
    host = "localhost"
    port = '3369'
    userName = "zxh"
    password = "zxh"
    dbName = "stocksAnalysis"

    def __init__(self,fileName = "Settings.json"):
        with  open(os.path.dirname(os.path.abspath(__file__))+"/"+fileName,'r') as jsonFile:
            jsonStr = jsonFile.read()
        print(jsonStr)
        jsonObject = json.loads(jsonStr)

        self.host = jsonObject["DatabaseSetting"]["host"]
        self.port = int(jsonObject["DatabaseSetting"]["port"])
        self.userName = jsonObject["DatabaseSetting"]["userName"]
        self.password = jsonObject["DatabaseSetting"]["password"]
        self.dbName = jsonObject["DatabaseSetting"]["dbName"]

        # Table description files directory
        self.tablesDirectory = os.path.dirname(os.path.abspath(__file__))+jsonObject["TableDirectory"]
