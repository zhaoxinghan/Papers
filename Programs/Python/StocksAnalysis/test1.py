import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
import tushare as ts

# get query ts_code
def GetTsCode():
    '''
    return the query ts_code
    '''
    return '000010.SZ'


# get stock daily data from tushare
startDate   = '20100101'    # start query date
endDate     = '20201231'    # end query date

tsCode = GetTsCode()    # Get query ts_code

ts.set_token('79cfeef7606afc45b9676ddcf9937471802ae79224210f48c6a28536')
pro = ts.pro_api()
print("Get data from Tushare!")
df = pro.daily(ts_code = tsCode,start_date = startDate,end_date = endDate)
if(df is not None):
    print("Complete!")
    print("Now the "+tsCode + " DataFrame is as following: ")
    print(df)
else:
    print("fail!")
# get a new dataframe of MA3 and MA7
df['MA3'] = NaN
df['MA7'] = NaN

# fill MA3, if there is not enough data in the beginning, there will be NaN
for index,row in df.iterrows():
    if(index <2 ):
        df.loc[index,'MA3']= NaN
    else:
        sum = 0
        for i in range(3):    # get the sum of price in three days
           sum += df.loc[index-i,'close'] 
        df.loc[index,'MA3'] = sum / 3

# using the same way, fill the column MA7
for index,row in df.iterrows():
    if(index <7 ):
        df.loc[index,'MA7']= NaN
    else:
        sum = 0
        for i in range(7):    # get the sum of price in three days
           sum += df.loc[index-i,'close'] 
        df.loc[index,'MA7'] = sum / 7

# reindex the dataframe, add a new column named cross
df1 = df.reindex(columns = list(df.columns)+['cross'])

# find the row which the price is upwards cross the MA3 and MA7 curve , and MA3 > MA7
# cross upwaords, result is 1
# cross downwards, result is -1
# others, result is 0
for index,row in df.iterrows():
    if index > 7:
        cond1 = row['MA3']> row['MA7']
        cond2 = df1.loc[index-1,'MA3'] > df1.loc[index-1,'close'] and row['MA3'] < row['close']  # close price cross MA3 upwards
        cond3 = df1.loc[index-1,'MA3'] < df1.loc[index-1,'close'] and row['MA3'] > row['close']  # close price cross MA3 downwards
        if(cond1 and cond2):
            df1.loc[index,'cross'] = 1
        elif cond3:
            df1.loc[index,'cross'] = -1
        else:
            df1.loc[index,'cross'] = 0
# temp result
print('df1 generation completed, now we have the cross result!')

print("The sum of the cross point is as following:")
print(df1['cross'].value_counts()) 


# then we will find the max price in next several days
# you can change the variable winningDay to set the period. 
winCount = 0
winningDay = 10
count = 0
df2 = df1[df1.cross == 1]
for index,row in df2.iterrows():
    count+=1
    s = df1.loc[index:(index+winningDay), ['high']]
    s_max = s.max()
    if(s_max['high'] / row['close'] > 1.05):
        winCount+=1
print('we find the total sum of the win point is '+ str(winCount))
print('The percent of the win points is {:.0%}'.format(winCount/count))