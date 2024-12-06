# stock_super/data_processor.py
import pandas as pd
from .utils import to_numer

def create_dataframe(response):
    """从响应中创建DataFrame"""
    if response and 'data' in response and 'klines' in response['data']:
        stock_df = response['data']['klines']
        columns = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '涨跌幅', '涨跌额', '换手率']
        rows = [k.split(',') for k in stock_df]
        name = response['data']['name']
        code = response['data']['code']
        df = pd.DataFrame(rows, columns=columns)
        df.insert(0, '代码', code)
        df.insert(0, '名称', name)
        return df
    else:
        print("无法创建DataFrame")
        return None

def process_data(df):
    """处理DataFrame，转换数据类型"""
    if df is not None:
        # 设置不转换格式的字段
        i_cols = ['名称', '代码', '日期']
        df = to_numer(df, i_cols)
        return df
    return None