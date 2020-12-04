price_str= '30.14,29.58,26.36,32.82'
type(price_str)

print('旧的price_str id = ',id(price_str))
price_str = price_str.replace(' ','')
print('新的price_str id = ',id(price_str))
print(price_str)

price_array = price_str.split(',')
print(price_array)
price_array.append('32.82')
print(price_array)

date_base =  20170118
date_array = [str(date_base+ind) for ind, _ in enumerate(price_array)]
print(date_array)

print("new function begin!")

stock_tuple_list = [(date, price) for date, price in zip(date_array, price_array)]
print("20170119价格:",stock_tuple_list[1][1])
print(stock_tuple_list)




