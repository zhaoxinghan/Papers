from CreateTableFromFile import CreateTableFromFile

import tushare as ts

class GetStockBasicDataFromTushare:
    def __init__(self):
        pass

    def GetStockBasicData(self):
        ts.set_token('79cfeef7606afc45b9676ddcf9937471802ae79224210f48c6a28536')
        pro = ts.pro_api()
        data = pro.query('stock_basic',exchage='',list_status='L',fields='ts_code,symbol,name,area,industry,list_date')
        print(data)
        return data

    def CreateTable(self):
        file = CreateTableFromFile().CreateTable('stock_basic')
        return
    
    def ExportData2Table(self):
        self.CreateTable()
        data = self.GetStockBasicData()
        for stock_basic in data:
            




x= GetStockBasicDataFromTushare()
x.GetStockBasicData()
