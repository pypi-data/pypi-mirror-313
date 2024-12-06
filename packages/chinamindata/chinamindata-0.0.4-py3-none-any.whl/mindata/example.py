# 示例调用
from china_min import fetch_stock_data

#可以获取大A股票分钟，freq取值1min'、'5min'、'15min'、'30min'、'60min'
df = fetch_stock_data( code = '000001.SZ', start_date = '2024-07-07 09:00:00',
                       token = 't7b36d8b64c00a0125e42ab1b69bd5a5777',
                       end_date = '2024-07-22 15:00:00',freq='60min',)


print(df)