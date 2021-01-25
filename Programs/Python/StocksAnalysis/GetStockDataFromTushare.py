from datetime import date, datetime, timedelta
from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Date, Float, Integer, Time, VARCHAR
from ImportSettings import ImportSettings
import tushare as ts


Base = declarative_base()

class StockBase():
    def __init__(self):
        # get the database setting
        self.setting = ImportSettings()

        # initialize the database connection
        self.engine = create_engine('mysql+pymysql://'+ self.setting.userName + ':'+ self.setting.password + '@'+self.setting.host + ':'+ str(self.setting.port)+'/'+self.setting.dbName)

        ts.set_token('79cfeef7606afc45b9676ddcf9937471802ae79224210f48c6a28536')
        self.pro = ts.pro_api()
        return
    
    def GetStockTable(self,stockTableName,rs_index):        
        if stockTableName == 'stock_basic':
            data = self.pro.query('stock_basic',exchange='',list_status='L',fields='ts_code,symbol,name,area,industry,list_date')
            print(data)
            print(type(data))

            data.to_sql(
                'stock_basic',
                self.engine,
                if_exists = 'replace',
                #index=True,
                #index_label = 'ts_code',
                dtype = {
                    "ts_code":String(20),
                    "symbol": String(20),
                    "name":String(20),
                    "area": String(10),
                    "industry": String(20),
                    "list_date": Date
                }
            )
        elif(stockTableName == 'TransHistory'):     # Transaction history table  

            ts.set_token('79cfeef7606afc45b9676ddcf9937471802ae79224210f48c6a28536')
            # loop each day in the date zone 2010.1.1 to Nowaday
            startDate = date(year=2010,month = 1,day = 1)
            endDate = date.today() - timedelta(days=1)    # end date is yesterday
            
            # loop every day for the transaction history
            i = startDate
            while i<=endDate:

                df = ts.get_tick_data('000001', date = '2019-12-12',src = 'tt')
                if df != None:
                    col_name = df.columns.tolist()
                    col_name.insert(0,"ts_code")    #add a column 'ts_code'
                    df2 = df.reindex(columns=col_name,fill_value = rs_index)
                    col_name = df2.columns.tolist()
                    col_name.insert(1,'date')   #add a column 'date'
                    df3 = df2.reindex(columns=col_name,fill_value = i)
                    df3.to_sql(
                        'TransHistory',
                        self.engine,
                        if_exists = 'replace',
                        index=False,
                        dtype = {
                            "ts_code":String(20),
                            "data": Date,
                            "time":Time,
                            "price": Float,
                            "change": String(20),
                            "volume": Integer,
                            "amount":Integer,
                            "type":String(4)
                        }
                    )

                i += timedelta(days=1)
        else: 
            print("switch error accour!")
        return

x = StockBase()
# x.GetStockTable('TransHistory')
x.GetStockTable('stock_basic','600050')
x.GetStockTable('TransHistory','688981')


        