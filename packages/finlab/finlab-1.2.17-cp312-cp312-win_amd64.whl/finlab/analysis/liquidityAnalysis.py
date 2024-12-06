import pandas as pd
from finlab import data
from finlab.analysis import Analysis
from finlab.market_info import TWMarketInfo


class LiquidityAnalysis(Analysis):

  def __init__(self, required_volume=200000, required_turnover=1000000):
    """分析台股策略流動性風險項目的機率

    !!! note
        參考[VIP限定文章](https://www.finlab.tw/customized_liquidityanalysis/)更了解流動性檢測內容細節。
    Args:
        required_volume (int): 要求進出場時的單日成交股數至少要多少？
        required_turnover (int): 要求進出場時的單日成交金額至少要多少元？避免成交股數夠，但因低價股因素，造成胃納量仍無法符合資金需求。

    Examples:
        ``` py

        # better syntax
        report.run_analysis('LiquidityAnalysis', required_volume=100000)

        # original syntax
        from finlab.analysis.liquidityAnalysis import LiquidityAnalysis
        report.run_analysis(LiquidityAnalysis(required_volume=100000))
        ```
    """

    self._required_volume = required_volume
    self._required_turnover = required_turnover
    self._result = None

  def is_market_info_supported(self, market_info):
    return 'TWMarketInfo' in str(market_info)

  def calculate_trade_info(self, report):

    # calculate trade bar return
    adj_trade_price = report.market_info.get_trading_price(report.trade_at, adj=True)
    adj_previous_close = report.market_info.get_trading_price('close', adj=True).shift()

    # calculate money flow
    trade_price = report.market_info.get_trading_price(report.trade_at, adj=False)
    volume = report.market_info.get_price('volume', adj=False)

    signal_dates = ["entry_date", "exit_date"]

    ret = [
      ["pct_change", adj_trade_price / adj_previous_close - 1, signal_dates],
      ["turnover", trade_price * volume, signal_dates],
      ["volume", volume, signal_dates]
    ]

    is_tw = isinstance(report.market_info, TWMarketInfo)


    if is_tw:
        flagged = data.get('etl:is_flagged_stock')
        ret += [
          ["類別", flagged, signal_dates],
          # ["處置股", ~data.get('etl:disposal_stock_filter').shift(fill_value=False), signal_dates],
          # ["警示股", ~data.get('etl:disposal_stock_filter').shift(fill_value=False), signal_dates],
          # ["全額交割股", ~data.get('etl:full_cash_delivery_stock_filter').shift(fill_value=False), signal_dates]
        ]

    return ret

  def analyze(self, report):
    trades = report.get_trades()

    if isinstance(report.market_info, TWMarketInfo):
      entry_pct_range = (trades.entry_date >= '2015-6-1') * 0.03 + 0.07
      exit_pct_range = (trades.exit_date >= '2015-6-1') * 0.03 + 0.07
    else:
      entry_pct_range = 0.1
      exit_pct_range = 0.1

    long_position = trades.position > 0

    entry_buy_at_top = long_position & (trades['pct_change@entry_date'] > entry_pct_range * 0.95)
    entry_sell_at_bottom = (~long_position) & (trades['pct_change@entry_date'] < -entry_pct_range * 0.95)

    exit_sell_at_bottom = long_position & (trades['pct_change@exit_date'] < -exit_pct_range * 0.95)
    exit_buy_at_top = (~long_position) & (trades['pct_change@exit_date'] > exit_pct_range * 0.95)

    trade_pct_count = trades['pct_change@entry_date'].notna() & trades['pct_change@exit_date'].notna()

    ret_dict = {
      'buy_high': [entry_buy_at_top.mean(), exit_buy_at_top.mean()],
      'sell_low': [entry_sell_at_bottom.mean(), exit_sell_at_bottom.mean()],
      'low_volume_stocks': [(trades['volume@entry_date'] < self._required_volume).mean(),
                     (trades['volume@exit_date'] < self._required_volume).mean()],
      'low_turnover_stocks': [(trades['turnover@entry_date'] < self._required_turnover).mean(),
                     (trades['turnover@exit_date'] < self._required_turnover).mean()],
    }

    is_tw = isinstance(report.market_info, TWMarketInfo)
    if is_tw:
        
        trades['類別@entry_date'] = trades['類別@entry_date'].fillna(0).astype(int)
        trades['類別@exit_date'] = trades['類別@exit_date'].fillna(0).astype(int)
        
        trades['警示股@entry_date'] = (trades['類別@entry_date'] & 0x1) != 0
        trades['處置股@entry_date'] = (trades['類別@entry_date'] & 0x2) != 0
        trades['全額交割股@entry_date'] = (trades['類別@entry_date'] & 0x4) != 0

        trades['警示股@exit_date'] = (trades['類別@exit_date'] & 0x1) != 0
        trades['處置股@exit_date'] = (trades['類別@exit_date'] & 0x2) != 0
        trades['全額交割股@exit_date'] = (trades['類別@exit_date'] & 0x4) != 0

        trades.drop(columns=['類別@entry_date', '類別@exit_date'], inplace=True)

        ret_dict = {**ret_dict, **{
            '警示股': [trades['警示股@entry_date'].mean(), trades['警示股@exit_date'].mean()],
            '處置股': [trades['處置股@entry_date'].mean(), trades['處置股@exit_date'].mean()],
            '全額交割股':[trades['全額交割股@entry_date'].mean(), trades['全額交割股@exit_date'].mean()]
        }}

    self._result = pd.DataFrame(ret_dict)

    self._result.index = ['entry', 'exit']

    return self._result.to_dict()

  def display(self):

    def percentage(v):
        return str(round(v*100, 1)) + '%'

    def make_pretty(styler):
        styler.set_caption("低流動性交易")
        styler.format(percentage)
        styler.background_gradient(axis=None, vmin=0, vmax=0.5, cmap="YlGnBu")
        return styler

    return self._result.style.pipe(make_pretty)
