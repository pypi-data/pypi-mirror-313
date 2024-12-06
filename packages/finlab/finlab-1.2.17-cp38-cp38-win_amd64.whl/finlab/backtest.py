import sys
import warnings
import datetime
import numpy as np
import pandas as pd
from typing import Union
from pandas.tseries.offsets import DateOffset
from pandas.tseries.frequencies import to_offset

import finlab
from finlab.market_info import get_market_info
from finlab import data, market_info
from finlab.core import mae_mfe as maemfe
from finlab.core import report
from finlab.utils import check_version, requests, set_global
from finlab.core.backtest_core import backtest_, get_trade_stocks
from finlab.dataframe import FinlabDataFrame


def warning_resample(resample):

    if '+' not in resample and '-' not in resample:
        return

    if '-' in resample and not resample.split('-')[-1].isdigit():
        return

    if '+' in resample:
        r, o = resample.split('+')
    elif '-' in resample:
        r, o = resample.split('-')

    warnings.warn(f"The argument sim(..., resample = '{resample}') will no longer support after 0.1.37.dev1.\n"
                  f"please use sim(..., resample='{r}', offset='{o}d')", DeprecationWarning)


def download_backtest_encryption_function_factory():

    encryption_time = datetime.datetime.now()
    encryption = ''

    def ret():

        nonlocal encryption_time
        nonlocal encryption

        if datetime.datetime.now() < encryption_time + datetime.timedelta(days=1) and encryption:
            return encryption

        res = requests.get('https://asia-east2-fdata-299302.cloudfunctions.net/auth_backtest',
                           {'api_token': finlab.get_token(), 'time': str(datetime.datetime.now())})

        if not res.ok:
            try:
                result = res.json()
            except:
                result = None

            print(result)
            return ''

        d = res.json()

        if 'v' in d and 'v_msg' in d and finlab.__version__ < d['v']:
            print(d['v_msg'])

        if 'msg' in d:
            print(d['msg'])

        encryption_time = datetime.datetime.now()
        encryption = d['encryption']

        return encryption
    return ret


download_backtest_encryption = download_backtest_encryption_function_factory()


def calc_essential_price(price, dates):

    dt = min(price.index.values[1:] - price.index.values[:-1])

    indexer = price.index.get_indexer(dates + dt)

    valid_idx = np.where(
        indexer == -1, np.searchsorted(price.index, dates, side='right'), indexer)
    valid_idx = np.where(valid_idx >= len(price), len(price) - 1, valid_idx)

    return price.iloc[valid_idx]


def arguments(price, close, high, low, open_, position, resample_dates=None, fast_mode=False):

    resample_dates = price.index if resample_dates is None else resample_dates
    position = position.astype(float).fillna(0)

    if fast_mode:
        date_index = pd.to_datetime(resample_dates)
        position = position.reindex(date_index, method='ffill')
        price = calc_essential_price(price, date_index)
        close = calc_essential_price(close, date_index)
        high = calc_essential_price(high, date_index)
        low = calc_essential_price(low, date_index)
        open_ = calc_essential_price(open_, date_index)

    if pd.__version__ >= '2.2.0':
        resample_dates = pd.Series(resample_dates).astype(np.int64).values
    else:
        resample_dates = pd.Series(resample_dates).view(np.int64).values

    return [price.values,
            close.values,
            high.values,
            low.values,
            open_.values,
            price.index.view(np.int64),
            price.columns.astype(str).values,
            position.values,
            position.index.view(np.int64),
            position.columns.astype(str).values,
            resample_dates
            ]


def line_notify(report=None, line_access_token: str = '', test: bool = False, name=''):
    """傳送回測結果之目前部位、近期換股訊息至Line聊天室。

    Args:
        report (Report):
            回測完的結果報告。

        line_access_token (str):
            於Line Notify取得的access_token(權杖)。至[Line Notify](https://notify-bot.line.me/zh_TW/ )登入Line帳號後，點選個人頁面，點選「發行權杖」，選擇欲接收訊息的聊天室(可選擇1對1接收Line Notify通知、或是選擇其他群組聊天室)，即可取得權杖。
        test (bool):
            是否進行傳送訊息測試。

        name (str):
            策略名稱，預設為空字串。

    Examples:
        欲進行測試，則設定`test`參數為True。

        ``` py
        from finlab import backtest

        line_access_token = 'xxxxxxxxxxxx'
        backtest.line_notify(line_access_token=line_access_token, test=True)
        ```

        若成功收到通知，則權杖設定已完畢，可直接在`sim`回測模組中開啟使用，或單獨調用此函式發送回測換股訊息。
        於sim中使用:

        ``` py
        from finlab import backtest

        line_access_token = 'xxxxxxxxxxxx'
        position = ...
        report = backtest.sim(position, notification_enable =True, line_access_token = line_access_token)
        ```

        已回測完，單獨傳訊息用:

        ``` py
        from finlab import backtest

        line_access_token = 'xxxxxxxxxxxx'
        report = backtest.sim(position)
        backtest.line_notify(report, line_access_token=line_access_token)
        ```

    """
    if test:
        message = 'Finlab line_notify 測試成功'
    else:
        if not isinstance(report, finlab.core.report.Report):
            raise Exception('Please provide a valid backtest report.')
        hold = []
        enter = []
        exit = []
        for i, p in report.position_info().items():
            if isinstance(p, dict):
                if i[:4].isdigit():
                    if p['status'] in ['exit'] and pd.isnull(report.current_trades.loc[i].exit_date):
                        hold.append(
                            f"{i}: {p['entry_date'][:10]}, {str(p['entry_price'])}")
                    if p['status'] in ['hold', 'sl', 'tp']:
                        hold.append(
                            f"{i}: {p['entry_date'][:10]}, {str(p['entry_price'])}")
                    if p['status'] in ['enter']:
                        enter.append(f"{i}: {p['entry_date'][:10]}的下個交易日進場")
                    if p['status'] in ['exit', 'sl', 'tp', 'sl_enter', 'tp_enter']:
                        exit.append(f"{i}: {p['exit_date'][:10]}的下個交易日出場")
        message_lines = [f'目前策略{name} 進場日及進場價格：']
        message_lines.extend(hold)
        message_lines.append('------------------------------')
        message_lines.append('近期操作：')
        message_lines.append('-策略新增')
        if len(enter) > 0:
            message_lines.extend(enter)
        else:
            message_lines.append('尚無')
        message_lines.append('-策略移除')
        if len(exit) > 0:
            message_lines.extend(exit)
        else:
            message_lines.append('尚無')
        message = "\n".join(message_lines)

    headers = {
        "Authorization": "Bearer " + line_access_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params={'message': message})
    if test:
        if eval(r.text)['status'] == 401:
            print(f'測試失敗。{r.text}')
        elif eval(r.text)['status'] == 200:
            print('測試成功，可開始使用finlab line_notify')


def sim(position: Union[pd.DataFrame, pd.Series],
        resample: Union[str, None] = None, resample_offset: Union[str, None] = None,
        trade_at_price: Union[str, pd.DataFrame] = 'close',
        position_limit: float = 1, fee_ratio: float = 1.425/1000,
        tax_ratio: float = 3/1000, name: str = '未命名', stop_loss: Union[float, None] = None,
        take_profit: Union[float, None] = None, trail_stop: Union[float, None] = None, touched_exit: bool = False,
        retain_cost_when_rebalance: bool = False, stop_trading_next_period: bool = True, live_performance_start: Union[str, None] = None,
        mae_mfe_window: int = 0, mae_mfe_window_step: int = 1, market: Union[str, market_info.MarketInfo] = 'AUTO', upload: bool = True, fast_mode=False,
        notification_enable: bool = False, line_access_token: str = '') -> report.Report:
    """Simulate the equity given the stock position history. 回測模擬股票部位所產生的淨值報酬率。

    Args:
        position (pd.DataFrame or pd.Series):
            買賣訊號紀錄。True 為持有， False 為空手。 若選擇做空position，只要將 sim(position) 改成負的 sim(-position.astype(float))即可做空。

        resample (str, None, pd.DataFrame, pd.Series, finlab.dataframe.FinlabDataFrame):
            交易週期。將 position 的訊號以週期性的方式論動股票，預設為每天換股。其他常用數值為 W、 M 、 Q （每週、每月、每季換股一次），也可以使用 W-Fri 在週五的時候產生新的股票清單，並且於下週交易日下單。

            * `D`: Daily
            * `W`: Weekly
            * `W-Wed`: Every Wednesday
            * `M`: Monthly
            * `MS`: Start of every month
            * `Q`: Quarterly
            * `QS`: Start of every quarter

            !!!note
                'D'與'None'的差別？
                resample='D' 的意義為每天隨股價變化做再平衡，就算當天股票清單沒變，但股票漲跌後，部位大小會變化，而 resample='D' 會強制再平衡，平均分散風險。

                但是當 resample=None 的話，假如清單不變，則不會強制再平衡，只有清單改變時，才做再平衡。適用情境在較常選到大波段標的的趨勢策略，較有機會將強勢股留下，而不會汰強留弱做再平衡。

            另外 `resample` 也接受 pd.DataFrame 以及 pd.Series，並且將其 index 用來當成換股的時間點，例如以下的範例：

            ``` py
            from finlab import backtest, data

            rev = data.get('monthly_revenue:當月營收')
            position = ...

            # 月營收發布時才換股
            backtest.sim(position, resample=rev)
            ```



        resample_offset (str or None):
            交易週期的時間位移，例如。

            - '1D': 位移一天
            - '1H': 位移一小時

        trade_at_price (str or pd.DataFrame):
            選擇回測之還原股價以收盤價或開盤價計算，預設為'close'。可選'close'、'open'、'open_close_avg'、'high_low_avg'或 'price_avg'。

        position_limit (float): maximum amount of investing a stock.
            單檔標的持股比例上限，控制倉位風險。預設為None。範例：0.2，代表單檔標的最多持有 20 % 部位。

        fee_ratio (float): fee ratio of buying or selling a stock.
            交易手續費率，預設為台灣無打折手續費 0.001425。可視個人使用的券商優惠調整費率。

        tax_ratio (float): tax ratio of selling a stock.
            交易稅率，預設為台灣普通股一般交易交易稅率 0.003。若交易策略的標的皆為ETF，記得設成 0.001。

        name (str): name of the strategy.
            策略名稱，預設為 未指名。策略名稱。相同名稱之策略上傳會覆寫。命名規則:全英文或開頭中文，不接受開頭英文接中文。

        stop_loss (float):
            停損基準，預設為None，不執行停損。範例：0.1，代表從再平衡開始，虧損 10% 時產生出場訊號。

        take_profit (float):
            停利基準，預設為None，不執行停利。範例：0.1，代表從再平衡開始， 10% 時產生出場訊號。

        trail_stop (float):
            移動停損停利基準，預設為None，不執行。範例：0.1，代表從最高點開始下跌，跌至 10% 時產生出場訊號。

        touched_exit (bool):
            是否在回測時，使用觸價停損停利？預設為 False。

        retain_cost_when_rebalance (bool):
            預設回測時，會將進場股票進場成本更新到到新的 rebalance 的當天價格，假如希望保留原本的進場價格當成停損停利的依據，可以設定為 `True`

        stop_trading_next_period (bool):
            當期已經停損停利，則下一期不買入，預設為 True。

        live_performance_start (str):
            策略建構的日期，例如 `2022-01-01` 此日期之前，策略未撰寫，此日期之後則視為與實單有類似效果，實際不影響回測的結果，單純紀錄而已。

        mae_mfe_window (int):
            計算mae_mfe於進場後於不同持有天數下的數據變化，主要應用為edge_ratio (優勢比率)計算。預設為0，則Report.display_mae_mfe_analysis(...)中的edge_ratio不會顯現。

        mae_mfe_window_step (int):
            與mae_mfe_window參數做搭配，為時間間隔設定，預設為1。若mae_mfe_window設20，mae_mfe_window_step設定為2，相當於python的range(0,20,2)，以2日為間距計算mae_mfe。

        market (str or MarketInfo):
            可選擇`'TW_STOCK', 'CRYPTO'`，分別為台股或加密貨幣，
            或繼承 finlab.market_info.MarketInfo 開發回測市場類別。

        upload (bool):
            上傳策略，預設為True，上傳策略。
            範例： False，不上傳，可用 finlab.backtest.sim(position, upload=False, ...).display() 快速檢視策略績效。

        fast_mode (bool):
            預設為False，若設定為True，則會使用快速模式，快速模式會忽略所有的停利停損設定，並且只有換股日進行報酬率模擬，因此會有一些誤差，當持有較多檔股票時，可以大幅加速回測速度。

    Returns:
        (finlab.analysis.Report):回測數據報告

    Examples:
        Assume the history of portfolio is construct as follows: When market close on 2021-12-31, the portfolio {B: 0.2, C: 0.4} is calculated. When market close on 2022-03-31, the portfolio {A:1} is calculated.


        |            | Stock 2330 | Stock 1101 | Stock 2454 |
        |------------|------------|------------|------------|
        | 2021-12-31 | 0%         | 20%        | 40%        |
        | 2022-03-31 | 100%       | 0%         | 0%         |
        | 2022-06-30 | 100%       | 0%         | 0%         |


        With the portfolio, one could backtest the equity history as follows:

        ``` py
        import pandas as pd
        from finlab import backtest

        position = pd.DataFrame({
            '2330': [0, 1, 1],
            '1101': [0.2, 0, 0],
            '2454': [0.4, 0, 0]
        }, index=pd.to_datetime(['2021-12-31', '2022-03-31', '2022-06-30']))

        report = backtest.sim(position)
        ```

    """

    in_pyodide = "pyodide" in sys.modules and "js" in sys.modules

    if in_pyodide:
        upload = True

    # check version
    check_version()

    if notification_enable and line_access_token == '':
        raise Exception(
            'line_access_token is required when enabling notifications. Please provide a valid token.')

    if isinstance(position, FinlabDataFrame):
        position = position.index_str_to_date()

    if (trail_stop is not None or stop_loss is not None or take_profit is not None) and fast_mode:
        raise Exception(
            'fast_mode cannot be used with trail_stop, stop_loss or take_profit.')

    # check type of position
    if not isinstance(position.index, pd.DatetimeIndex):
        raise TypeError("Expected the dataframe to have a DatetimeIndex")

    if isinstance(position, pd.Series) and position.name is None:
        raise Exception(
            'Asset name not found. Please asign asset name by "position.name = \'2330\'".')

    # auto detect market type
    # todo: use less hacky method to identify the market
    market = get_market_info(position, user_market_info=market)

    if not isinstance(market, market_info.MarketInfo):
        raise Exception("It seems like the market has"
                        "not been specified well when using the hold_until"
                        " function. Please provide the market='TW', "
                        "market='US' or market=MarketInfo")

    # determine trading price
    price = trade_at_price
    if isinstance(trade_at_price, str):
        price = market.get_trading_price(trade_at_price, adj=True)

    assert isinstance(price, pd.DataFrame)

    if isinstance(trade_at_price, pd.DataFrame) and touched_exit:
        print('**WARNING: Using trade_at_price as dataframe without high, and low price. Candle information is not completed.')
        print('           The backtest result can be incorrect when touched_exit=True.')
        print('           If the complete backtest result is required, please implement MarketInfo with get_price function.')
        print('           MarketInfo details: https://doc.finlab.tw/reference/market_info/')
        print('           And use backtest.sim(..., market=MarketInfo) during backtest, so that the correct information is accessable from backtest.sim().')

    try:
        if isinstance(live_performance_start, str):
            live_performance_start = datetime.datetime.fromisoformat(
                live_performance_start)
    except:
        raise Exception(
            "**ERROR: live_performance_start string format not valid. It should be ISO format, i.e. YYYY-MM-DD.")

    def reindex_if_needed(df, ref_df):
        if df.shape != ref_df.shape:
            df = df.reindex_like(ref_df)
        return df

    close = price
    high = price
    low = price
    open_ = price
    if touched_exit:

        high = reindex_if_needed(market.get_price('high', adj=True), price)
        low = reindex_if_needed(market.get_price('low', adj=True), price)
        open_ = reindex_if_needed(market.get_price('open', adj=True), price)

    if trade_at_price != 'close':
        close = reindex_if_needed(market.get_price(
            'close', adj=True).reindex_like(price), price)

    # check position types
    if isinstance(position, pd.Series):
        if position.name in price.columns:
            position = position.to_frame()
        else:
            raise Exception(
                'Asset name not found. Please asign asset name by "position.name = \'2330\'".')

    # check position is valid
    # if position.abs().sum().sum() == 0 or len(position.index) == 0:
    #     raise Exception('Position is empty and zero stock is selected.')

    # format position index
    if isinstance(position.index[0], str):
        position = FinlabDataFrame(position).index_str_to_date()

    if not isinstance(position.index, pd.DatetimeIndex):
        raise Exception("The DataFrame index is not of type DatetimeIndex!")

    # if position date is very close to price end date, run all backtesting dates
    assert len(position.shape) >= 2
    delta_time_rebalance = position.index[-1] - position.index[-3]
    backtest_to_end = position.index[-1] + \
        delta_time_rebalance > price.index[-1]

    tz = position.index.tz
    now = datetime.datetime.now(tz=tz)

    # check if position date is daily (pd.Timestamp hour, minute, second is 0)
    is_daily = (position.index.hour == 0).all()\
        and (position.index.minute == 0).all()\
        and (position.index.second == 0).all()

    # set now to yesterday's end if is_daily position
    if is_daily and datetime.datetime.now(tz=market.tzinfo()) < market.market_close_at_timestamp():
        now = now.replace(hour=23, minute=59, second=0,
                          microsecond=0) - datetime.timedelta(days=1)

    present_data_date = max(price.index[-1], now) if backtest_to_end else position.index[-1]

    position = position[(position.index <= present_data_date)]
    backtest_end_date = price.index[-1] if backtest_to_end else position.index[-1]

    # resample dates
    dates = None
    next_trading_date = position.index[-1]
    if isinstance(resample, pd.DataFrame) or isinstance(resample, pd.Series):

        if isinstance(resample.index, pd.DatetimeIndex):
            dates = resample.index.tolist()
        elif isinstance(resample, FinlabDataFrame):
            dates = resample.index_str_to_date().index.tolist()

        dates = [d for d in dates if position.index[0]
                 <= d and d <= present_data_date]
        next_trading_date = dates[-1]

    elif isinstance(resample, pd.DatetimeIndex):

        dates = resample.tolist()
        dates = [d for d in dates if position.index[0]
                 <= d and d <= present_data_date]
        next_trading_date = dates[-1]

    elif isinstance(resample, str):

        if pd.__version__ >= '2.2.0':
            old_resample_strings = ['M', 'BM', 'SM',
                                    'CBM', 'Q', 'BQ', 'A', 'Y', 'BY']
            if resample in old_resample_strings:
                resample += 'E'

        # add additional day offset
        offset_days = 0
        if '+' in resample:
            offset_days = int(resample.split('+')[-1])
            resample = resample.split('+')[0]
        if '-' in resample and resample.split('-')[-1].isdigit():
            offset_days = -int(resample.split('-')[-1])
            resample = resample.split('-')[0]

        # generate rebalance dates
        alldates = pd.date_range(
            position.index[0],
            present_data_date + datetime.timedelta(days=360),
            freq=resample, tz=tz)

        alldates += DateOffset(days=offset_days)

        if resample_offset is not None:
            alldates += to_offset(resample_offset)

        dates = [d for d in alldates if position.index[0]
                 <= d and d <= present_data_date]

        # calculate the latest trading date
        if price.index[-1] > dates[-1]:
            dates += [min(set(alldates) - set(dates))]

        next_trading_date = dates[-1]

    elif resample is None:
        # user set resample to None. Rebalance everyday might cause over transaction.
        # remove rebalance date if portfolio is the same.
        change = (position.diff().abs().sum(axis=1) != 0) | (
            (position.index == position.index[0]) & position.iloc[0].notna().any())
        position = position.loc[change]

    if stop_loss is None or stop_loss == 0:
        stop_loss = 1

    if take_profit is None or take_profit == 0:
        take_profit = np.inf

    if trail_stop is None or trail_stop == 0:
        trail_stop = np.inf

    if dates is not None:
        position = position.reindex(dates, method='ffill')

    encryption = download_backtest_encryption()

    if encryption == '':
        raise Exception('Cannot perform backtest, permission denied.')

    args = arguments(price, close, high, low, open_,
                     position, dates, fast_mode=fast_mode)

    creturn_value = backtest_(*args,
                              encryption=encryption,
                              fee_ratio=fee_ratio, tax_ratio=tax_ratio,
                              stop_loss=stop_loss, take_profit=take_profit, trail_stop=trail_stop,
                              touched_exit=touched_exit, position_limit=position_limit,
                              retain_cost_when_rebalance=retain_cost_when_rebalance,
                              stop_trading_next_period=stop_trading_next_period,
                              mae_mfe_window=mae_mfe_window, mae_mfe_window_step=mae_mfe_window_step, periodically_rebalance=resample is not None)

    total_weight = position.abs().sum(axis=1).clip(1, None)
    org_position_index = position.index

    position = position.div(total_weight.where(total_weight != 0, np.nan), axis=0).fillna(0)\
                       .clip(-abs(position_limit), abs(position_limit))

    creturn_dates = dates if dates and fast_mode else price.index

    creturn = (pd.Series(creturn_value, creturn_dates)
               # remove the begining of creturn since there is no pct change
               .pipe(lambda df: df[(df != 1).cumsum().shift(-1, fill_value=1) != 0])
               # remove the tail of creturn for verification
               .loc[:backtest_end_date]
               # replace creturn to 1 if creturn is None
               .pipe(lambda df: df if len(df) != 0 else pd.Series(1, position.index)))

    position = position.loc[creturn.index[0]:]

    price_index = args[5]
    position_columns = args[9]
    trades, operation_and_weight = get_trade_stocks(position_columns,
                                                    price_index, touched_exit=touched_exit)

    ####################################
    # refine mae mfe dataframe
    ####################################
    def refine_mae_mfe():
        if len(maemfe.mae_mfe) == 0:
            return pd.DataFrame()

        m = pd.DataFrame(maemfe.mae_mfe)
        nsets = int((m.shape[1]-1) / 6)

        metrics = ['mae', 'gmfe', 'bmfe', 'mdd', 'pdays', 'return']

        tuples = sum([[(n, metric) if n == 'exit' else (n * mae_mfe_window_step, metric)
                       for metric in metrics] for n in list(range(nsets)) + ['exit']], [])

        m.columns = pd.MultiIndex.from_tuples(
            tuples, names=["window", "metric"])
        m.index.name = 'trade_index'
        m[m == -1] = np.nan

        exit = m.exit.copy()

        if touched_exit and len(m) > 0 and 'exit' in m.columns:
            m['exit'] = (exit
                         .assign(gmfe=exit.gmfe.clip(-abs(stop_loss), abs(take_profit)))
                         .assign(bmfe=exit.bmfe.clip(-abs(stop_loss), abs(take_profit)))
                         .assign(mae=exit.mae.clip(-abs(stop_loss), abs(take_profit)))
                         .assign(mdd=exit.mdd.clip(-abs(stop_loss), abs(take_profit))))

        return m

    m = refine_mae_mfe()

    ####################################
    # refine trades dataframe
    ####################################
    def convert_datetime_series(df):
        cols = ['entry_date', 'exit_date', 'entry_sig_date', 'exit_sig_date']
        df[cols] = df[cols].apply(
            lambda s: pd.to_datetime(s).dt.tz_localize(tz))
        return df

    def assign_exit_nat(df):
        cols = ['exit_date', 'exit_sig_date']
        df[cols] = df[cols].loc[df.exit_index != -1]
        return df

    trades = (pd.DataFrame(trades,
                           columns=['stock_id', 'entry_date', 'exit_date',
                                    'entry_sig_date', 'exit_sig_date', 'position',
                                    'period', 'entry_index', 'exit_index'])
              .rename_axis('trade_index')
              .pipe(convert_datetime_series)
              .pipe(assign_exit_nat)
              )

    if len(trades) != 0:
        trades = trades.assign(**{'return':  (m.iloc[:, -1])})

        if touched_exit:
            min_return = (1 - fee_ratio) * (1 - abs(stop_loss)) * \
                (1 - tax_ratio - fee_ratio) - 1
            max_return = (1 - fee_ratio) * (1 + abs(take_profit)
                                            ) * (1 - tax_ratio - fee_ratio) - 1
            trades['return'] = trades['return'].clip(min_return, max_return)

    r = report.Report(
        creturn=creturn,
        position=position,
        fee_ratio=fee_ratio,
        tax_ratio=tax_ratio,
        trade_at=trade_at_price,
        next_trading_date=next_trading_date,
        market_info=market)

    r.resample = resample if isinstance(resample, str) else None
    r.stop_loss = stop_loss
    r.take_profit = take_profit
    r.trail_stop = trail_stop
    r.live_performance_start = live_performance_start

    r.mae_mfe = m

    r.trades = trades

    # calculate weights
    if len(operation_and_weight['weights']) != 0:
        r.weights = pd.Series(operation_and_weight['weights'])
        r.weights.index = r.position.columns[r.weights.index]
    else:
        r.weights = pd.Series(dtype='float64')

    # calculate next weights
    if len(operation_and_weight['next_weights']) != 0:
        r.next_weights = pd.Series(operation_and_weight['next_weights'])
        r.next_weights.index = r.position.columns[r.next_weights.index]
    else:
        r.next_weights = pd.Series(dtype='float64')

    r.weights.name = org_position_index[operation_and_weight['weight_time']]
    r.next_weights.name = org_position_index[operation_and_weight['next_weight_time']]

    # calculate actions
    if len(operation_and_weight['actions']) != 0:
        # find selling and buying stocks
        r.actions = pd.Series(operation_and_weight['actions'])
        r.actions.index = r.position.columns[r.actions.index]
    else:
        r.actions = pd.Series(dtype=object)

    # fill stock id to trade history
    snames = market.get_asset_id_to_name()
    industry = market.get_industry()

    def f_id_to_name(
        sid): return f"{sid + ' ' + snames[sid] if sid in snames else sid}"

    def f_id_to_industry(
        sid): return f"{industry[sid] if sid in industry else ''}"

    if len(r.actions) != 0:

        actions = r.actions

        sell_sids = actions[actions == 'exit'].index
        sell_instant_sids = actions[(actions == 'sl') | (actions == 'tp')
                                    | (actions == 'sl_enter') | (actions == 'tp_enter')].index
        buy_sids = actions[actions == 'enter'].index

        if len(trades):
            # check if the sell stocks are in the current position
            assert len(set(sell_sids) -
                       set(trades.stock_id[trades.exit_sig_date.isnull()])) == 0

            # fill exit_sig_date and exit_date
            temp = trades.loc[trades.stock_id.isin(
                sell_sids), 'exit_sig_date'].fillna(r.position.index[-1])
            trades.loc[trades.stock_id.isin(sell_sids), 'exit_sig_date'] = temp

            temp = trades.loc[trades.stock_id.isin(
                sell_instant_sids), 'exit_sig_date'].fillna(price.index[-1])
            trades.loc[trades.stock_id.isin(
                sell_instant_sids), 'exit_sig_date'] = temp.to_numpy()

            r.trades = pd.concat([r.trades, pd.DataFrame({
                'stock_id': buy_sids,
                'entry_date': pd.NaT,
                'entry_sig_date': r.position.index[-1],
                'exit_date': pd.NaT,
                'exit_sig_date': pd.NaT,
            })], ignore_index=True)

            r.trades['exit_sig_date'] = pd.to_datetime(r.trades.exit_sig_date)

    if len(trades) != 0:
        r.trades['industry'] = r.trades.stock_id.map(f_id_to_industry)
        r.trades['stock_id'] = r.trades.stock_id.map(f_id_to_name)

    if hasattr(r, 'actions') and len(r.actions) != 0:
        r.actions.index = r.actions.index.map(f_id_to_name)

    r.weights.index = r.weights.index.map(f_id_to_name)
    r.next_weights.index = r.next_weights.index.map(f_id_to_name)

    r.add_trade_info('trade_price', market.get_trading_price(
        trade_at_price, adj=False), ['entry_date', 'exit_date'])
    
    if len(r.trades) != 0 and not fast_mode:
        r.run_analysis("Liquidity", display=False)

    # add mae mfe to report
    if len(trades) != 0:
        trades = r.trades
        mae_mfe = r.mae_mfe
        exit_mae_mfe = mae_mfe['exit'].copy().drop(columns=['return'])
        r.trades = pd.concat([trades, exit_mae_mfe], axis=1)
        r.trades.index.name = 'trade_index'

        r.calculate_current_trades()

    if in_pyodide:
        set_global('backtest_report', {
            'report': r.to_json(),
            'position': r.position_info2()
        })
        return r

    if notification_enable:
        line_notify(r, line_access_token, name=name)

    if upload:
        r.upload(name)
        if not in_pyodide:
            r.display()

    return r
