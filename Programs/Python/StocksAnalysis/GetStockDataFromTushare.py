from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Date, VARCHAR
from ImportSettings import ImportSettings
import tushare as ts


Base = declarative_base()

class StockBase(Base):
    # table name:
    __tablename__ = 'stock_base'

    # table structure
    ts_code = Column(String(20),primary_key  = True)
    symbol = Column(String(20))
    name = Column(String(20))
    area = Column(String(20))
    industry = Column(String(20))
    list_date = Column(Date)

# get the database setting
setting = ImportSettings()

# initialize the database connection
engine = create_engine('mysql+pymysql://'+ setting.userName + ':'+ setting.password + '@'+setting.host + ':'+ str(setting.port)+'/'+setting.dbName)

ts.set_token('79cfeef7606afc45b9676ddcf9937471802ae79224210f48c6a28536')
pro = ts.pro_api()
data = pro.query('stock_basic',exchage='',list_status='L',fields='ts_code,symbol,name,area,industry,list_date')
print(data)
print(type(data))

data.to_sql(
    'stock_basic',
    engine,
    if_exists = 'replace',
    index=False,
    dtype = {
        "ts_code":String(20),
        "symbol": String(20),
        "name":String(20),
        "area": String(10),
        "industry": String(20),
        "list_date": Date
    }
)