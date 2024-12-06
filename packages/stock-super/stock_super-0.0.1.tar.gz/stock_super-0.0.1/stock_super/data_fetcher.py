# stock_super/data_fetcher.py
import requests
from .config import REQUEST_HEADERS

# 创建一个会话对象，可以保持连接，提高请求效率
session = requests.Session()

def get_stock_id(stock_name):
    """根据股票名称获取股票代码"""
    getcode_url = f"https://searchapi.eastmoney.com/api/suggest/get?input={stock_name}&type=14"
    response = session.get(getcode_url, headers=REQUEST_HEADERS).json()
    if 'QuotationCodeTable' in response and 'Data' in response['QuotationCodeTable']:
        return response['QuotationCodeTable']['Data'][0]['QuoteID']
    else:
        print("无法获取股票代码")
        return None

def get_stock_data(stock_id, start_date, end_date):
    """根据股票代码获取股票数据"""
    getdata_params = {
        "beg": start_date,
        "end": end_date,
        "secid": stock_id,
    }
    getdata_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f59,f60,f61&rtntype=6&klt=101&fqt=1"
    response = session.get(getdata_url, headers=REQUEST_HEADERS, params=getdata_params).json()
    if 'data' in response and 'klines' in response['data']:
        return response
    else:
        print("无法获取股票数据")
        return None