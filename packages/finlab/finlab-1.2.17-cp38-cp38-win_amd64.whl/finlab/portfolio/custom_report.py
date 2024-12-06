import datetime
import logging
from finlab.core.report import Report
from finlab import backtest
import pandas as pd

logger = logging.getLogger(__name__)

def create_multi_asset_report(stock_list: dict, **kwargs):
    
    """根據提供的股票清單創建多資產報告。
    Create a multi-asset report based on the stock list provided.
    
    Args:
        stock_list (dict): 一個以股票代號為 key，權重大小為 value。 A dictionary with stock id as key and weight as value.

    Returns:
        Report: 一個包含回測結果的報告對象。A report object with the backtest result.

    Example:

        >>> from finlab.portfolio import create_multi_asset_report
        ...
        ...
        >>> report = create_multi_asset_report({'2330': 0.5, '1101': 0.5})
    """

    position = pd.DataFrame(0, index=pd.to_datetime(['2010-12-31', '2011-12-31', '2022-12-31', datetime.datetime.now().strftime('%Y-%m-%d')]), columns=list(stock_list.keys()))
    for stock, weight in stock_list.items():
        position[stock] = weight

    if 'resample' not in kwargs:
        kwargs['resample'] = 'Q'


    if 'upload' in kwargs and kwargs['upload']:
        logger.warning("The upload parameter is not supported in create_custom_report.")
        kwargs['upload'] = False

    report = backtest.sim(position, upload=False, **kwargs)
    return report

def create_custom_report(stock_list: dict, **kwargs):

    """根據提供的股票清單創建自定義報告。
    Create a custom report based on the stock list provided.
    
    Args:
        stock_list (dict): 一個以日期為鍵，股票代碼列表為值的字典。 A dictionary with date as key and a list of stock ids as value.

    Returns:
        Report: 一個包含回測結果的報告對象。A report object with the backtest result.

    Example:

        >>> from finlab.portfolio import create_custom_report
        ...
        ... stock_list = {
        ...     '2024-12-31': ['1101', '2330'],
        ...     '2024-06-30': ['1101']
        ... }
        ...
        >>> report = create_custom_report(stock_list)
    """

    position = pd.DataFrame(0, index=pd.to_datetime(list(stock_list.keys())), columns=list(set(sum(stock_list.values(), []))))
    for date, stocks in stock_list.items():
        position.loc[date, stocks] = 1

    if 'upload' in kwargs and kwargs['upload']:
        logger.warning("The upload parameter is not supported in create_custom_report.")

    kwargs['upload'] = False

    report = backtest.sim(position, upload=False)
    return report