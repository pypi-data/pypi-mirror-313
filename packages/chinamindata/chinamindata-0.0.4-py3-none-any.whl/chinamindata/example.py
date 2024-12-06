# 示例调用
from chinamindata.china_min import fetch_stock_data

#可以获取大A股票分钟，freq取值1min'、'5min'、'15min'、'30min'、'60min'
df = fetch_stock_data( code = '000001.SZ', start_date = '2024-07-07 09:00:00',
                       token = '637de0f1570f7273fa355e37d34ac5cd70',
                       end_date = '2024-07-22 15:00:00',freq='60min',)
print(df)

from chinamindata.china_min_open import fetch_stock_data
#可以获取大A股票分钟开盘竞价
df = fetch_stock_data(
                       token = '637de0f1570f7273fa355e37d34ac5cd70',
                      trade_date='20241122')
print(df)

from chinamindata.china_min_close import fetch_stock_data
#可以获取大A股票分钟闭盘竞价
df = fetch_stock_data(
                       token = '637de0f1570f7273fa355e37d34ac5cd70',
                      trade_date='20241122')
print(df)
# 示例调用

from chinamindata.china_list import fetch_stock_data
#可以获取大A股票、指数、基金
df = fetch_stock_data(
                       token = '637de0f1570f7273fa355e37d34ac5cd70',
                      type="SZSE")

print(df)