import pandas as pd
from finlab import data
from finlab.tools.event_study import create_factor_data
from tqdm import tqdm
from finlab.dataframe import FinlabDataFrame
import numpy as np

def corr(df):
    ret = df.corr().iloc[0, 1]
    return ret

def ndcg_k(k):
    from sklearn.metrics import ndcg_score
    def ndcg(df):
        s1 = (np.reshape(df.iloc[:,0].rank().values, (-1, len(df))))
        s2 = (np.reshape(df.iloc[:,1].rank().values, (-1, len(df))))
        return ndcg_score(s1, s2, k=k)
    return ndcg

ndcg20 = ndcg_k(20)
ndcg50 = ndcg_k(50)

def precision_at_rank(k):

    def ret(df):

        y_true = df.iloc[:, 0]
        y_score = df.iloc[:, 1]
        assert (k >= 0) & (k <= 1)
        # Get the indices of the top k scores
        selected = y_score.rank(pct=True) > k
        return y_true.rank(pct=True)[selected.values].mean()
        
    return ret


def calc_metric(factor, adj_close, days=[10, 20, 60, 120], func=corr):

    """計算因子

    Args:
        factor (pd.DataFrame): 因子
        adj_close (pd.DataFrame): 股價
        days (list, optional): 預測天數. Defaults to [10, 20, 60, 120].
        func (function, optional): 計算函數. Defaults to corr.

    Returns:
        pd.DataFrame: 因子計算結果

    Example:
        >>> factor = data.indicator('RSI')
        >>> adj_close = data.get('etl:adj_close')
        >>> calc_metric(factor, adj_close)

        | date       | factor_10 | factor_20 | factor_60 | factor_120 |
        |------------|-----------|-----------|-----------|------------|
        | 2010-01-01 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-02 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-03 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-04 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-05 | 0.1       | 0.2       | 0.3       | 0.4        |
    """

    if isinstance(factor, pd.DataFrame):
        factor = {'factor': factor}

    for fname, f in factor.items():
        factor[fname] = FinlabDataFrame(f).index_str_to_date()

    ics = {}

    total = len(days) * len(factor)
    with tqdm(total=total, desc="Processing") as pbar:
        for d in days:
            ret = adj_close.shift(-d-1) / adj_close.shift(-1) - 1

            for fname, f in factor.items():
                inter_col = f.columns.intersection(adj_close.columns)
                inter_index = f.index.intersection(adj_close.index)

                funstack = f.loc[inter_index, inter_col].unstack()
                ret_unstack = ret.loc[inter_index, inter_col].unstack()


                ics[f"{fname}_{d}"] = pd.DataFrame({
                    'ret': ret_unstack.values,
                    'f': funstack.values,
                }, index=funstack.index).dropna().groupby(level='date').apply(func)
                pbar.update(1)

    return pd.concat(ics, axis=1)


def ic(factor, adj_close, days=[10, 20, 60, 120]):
    """計算因子的IC

    Args:
        factor (pd.DataFrame): 因子
        adj_close (pd.DataFrame): 股價
        days (list, optional): 預測天數. Defaults to [10, 20, 60, 120].


    Returns:
        pd.DataFrame: 因子計算結果

    Example:
        >>> factor = data.indicator('RSI')
        >>> adj_close = data.get('etl:adj_close')
        >>> calc_metric(factor, adj_close)

        | date       | factor_10 | factor_20 | factor_60 | factor_120 |
        |------------|-----------|-----------|-----------|------------|
        | 2010-01-01 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-02 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-03 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-04 | 0.1       | 0.2       | 0.3       | 0.4        |
        | 2010-01-05 | 0.1       | 0.2       | 0.3       | 0.4        |
    """
    return calc_metric(factor, adj_close, days=days, func=corr)