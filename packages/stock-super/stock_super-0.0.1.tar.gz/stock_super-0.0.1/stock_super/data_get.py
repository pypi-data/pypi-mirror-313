# main.py
from stock_super.data_fetcher import get_stock_id, get_stock_data
from stock_super.data_processor import create_dataframe, process_data
import pandas as pd

def data_get(stock_name, start_date, end_date):
    """主函数"""
    # 获取股票代码
    stock_id = get_stock_id(stock_name)
    if not stock_id:
        print("无法获取股票代码")
        return None

    # 获取股票数据
    response = get_stock_data(stock_id, start_date, end_date)
    if not response:
        print("无法获取股票数据")
        return None

    # 创建DataFrame
    df = create_dataframe(response)
    if df is None:
        print("无法创建DataFrame")
        return None

    # 处理DataFrame
    df = process_data(df)
    if df is None:
        print("无法处理DataFrame")
        return None

    return df

if __name__ == "__main__":
    # 示例调用
    stock_name = '新集能源'
    start_date = '20240901'
    end_date = '20240913'
    result_df = data_get(stock_name, start_date, end_date)
    
    if result_df is not None:
        print(result_df)