# stock_super/utils.py
import pandas as pd

def to_numer(df, i_cols):
    """将指定列的数据类型转换为数值类型"""
    trans_cols = list(set(df.columns) - set(i_cols))
    df[trans_cols] = df[trans_cols].apply(lambda s: pd.to_numeric(s, errors='coerce'))
    return df