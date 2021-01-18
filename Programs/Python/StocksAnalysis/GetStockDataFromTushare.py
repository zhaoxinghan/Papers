from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Date
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
engine = create_engine('mysql+mysqlconnector://'+ setting.userName + ':'+ setting.password + setting.host + ':'+ setting.port+'/'+setting.dbName)
DBSession = sessionmaker(bind=engine)

ts.set_token('79cfeef7606afc45b9676ddcf9937471802ae79224210f48c6a28536')
pro = ts.pro_api()
data = pro.query('stock_basic',exchage='',list_status='L',fields='ts_code,symbol,name,area,industry,list_date')
print(data)

session = DBSession()

session.add_all(data)
session.commit()