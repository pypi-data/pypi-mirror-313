#d
"""
1、安装对应库
pip install chinadata

"""
#2、如果使用通用行情接口，
from chinadata.pp import get_bar_data
df = get_bar_data(token='9e84ed87f29cf43fc70b5198b1e4cd4093',ts_code='150018.SZ', start_date='20180101', end_date='20181029',asset='FD')
print(df)
#3、如果使用其他接口（例如接口名称为stock_basic)，其他参数一致，请填写参数api_name='stock_basic'
from chinadata.qq import get_query_data
#基础信息
df = get_query_data(token='9e84ed87f29cf43fc70b5198b1e4cd4093',api_name='stock_basic',fields='ts_code,symbol,name,area,industry,list_date',exchange='',  )
print(df)

#日线接口
df = get_query_data(api_name='daily',token='9e84ed87f29cf43fc70b5198b1e4cd4093', ts_code='000001.SZ', start_date='20180701', end_date='20180718')
print(df)

