from finlab.analysis import Analysis
from finlab import data
from finlab.dataframe import FinlabDataFrame
import pandas as pd
import numpy as np


class InequalityAnalysis(Analysis):

  def __init__(self, name, df=None, date_type='entry_sig_date', target='return'):

    """Analyze return of trades with condition inequality
    
    Args:
        name (str): name of the condition
        df (pd.DataFrame or None): value used in condition. If df is None, `data.get(name)` will be automatically perform to fetch the values.
        date_type (str): can be either `entry_date`, `entry_sig_date`, `exit_date`, `exit_sig_date`.
        target (str): the target to optimize. Any column name in report.get_trades()

    Examples:
        ``` py
        report.run_analysis('InequalityAnalysis', name='price_earning_ratio:股價淨值比')
        ```
    """

    self._name = name
    self._date_type = date_type
    self._target = target
    self._result = None
    self._min_samples = 50
    self._outlier_std = 3
    self._df = data.get(name) if df is None else df

    if isinstance(self._df, FinlabDataFrame):
        self._df = self._df.index_str_to_date()

    if not isinstance(self._df, pd.DataFrame) and not isinstance(self._df, FinlabDataFrame):
      raise Exception(f"InequalityAnalysis: df type is {type(df)} not supported!")

  def calculate_trade_info(self, report):
    return [
      [self._name, self._df, self._date_type]
    ]

  def analyze(self, report):

    x = f'{self._name}@{self._date_type}'
    y = self._target

    trades = report.get_trades()
    if x not in trades.columns:
      raise Exception(f'InequalityAnalysis: cannot find {x} in report.get_trades()')

    if y not in trades.columns:
      raise Exception(f'InequalityAnalysis: cannot find {x} in report.get_trades()')

    v = trades[[x, y]].sort_values(x)
    v = v.reset_index(drop=True)
    v.columns = ['x', 'y']
    v = v.dropna(how='any')
    outlier_std = self._outlier_std

    ymean = v.y.mean()
    ystd = v.y.std()
    v['y'] = v.y.clip(ymean - outlier_std * ystd, ymean + outlier_std * ystd)

    y_mean_lx = pd.Series(self.rcummean(v.y).values, index=v.index)
    y_mean_sx = pd.Series(self.cummean(v.y).values, index=v.index)

    v['y_mean_lx'] = y_mean_lx.values[::-1]
    v['y_mean_sx'] = y_mean_sx.values

    self._result = v
    return self._result

  @staticmethod
  def cummean(s):
    ret = s.cumsum() / np.arange(1, len(s)+1, 1) - s.mean()
    return ret

  @staticmethod
  def rcummean(s):
    return (s.sum() - s.cumsum()) / np.arange(len(s)+1, 1, -1) - s.mean()

  def display(self):

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    v = self._result
    x = self._name
    y = self._target
    min_samples = self._min_samples
    outlier_std = self._outlier_std

    if ':' in x:
      x = x.split(':')[-1]

    def to_xy(s):
      return {'x': s.index.values, 'y': s.values}

    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=(f"{x} < x", f"{x} > x", "", ""),
                        shared_yaxes=True, shared_xaxes=True,
                        vertical_spacing=0.02, horizontal_spacing=0.02)

    log_scale = (v.x.values >= 0).all() & (np.std(np.log(v.x.values+0.1)) < np.std(v.x.values+0.1))



    fig.add_trace(
        go.Scatter(**to_xy(v.y_mean_lx.iloc[min_samples:]), name=f'mean {y} (drop small x)', hovertemplate="%{y:.2%}"),
        row=1, col=2
    )

    fig.add_trace(
            go.Scatter(**to_xy(v.y_mean_lx.rolling(100, min_periods=1, center=True).mean().iloc[min_samples:]), hovertemplate="%{y:.2%}",
                          name=f'smooth {y} (drop small x)'),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(**to_xy(v.x.iloc[min_samples:]),  name=f'trades'),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(**to_xy(v.y_mean_sx.iloc[min_samples:]), name=f'mean {y} (drop large x)', hovertemplate="%{y:.2%}"),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(**to_xy(v.y_mean_sx.rolling(100, min_periods=1, center=True).mean().iloc[min_samples:]),hovertemplate="%{y:.2%}", name=f'smooth {y} (drop large x)'),
        row=1, col=1
    )

    s = v.x.copy()
    s.index = s.index[::-1]

    fig.add_trace(
        go.Scatter(**to_xy(s.iloc[:-min_samples]), name=f'trades'),
        row=2, col=2
    )

    fig.update_layout(height=500, width=800, title_text=f"Inequality Analysis")

    if log_scale:
      fig.update_layout(yaxis3=dict(type="log"),yaxis4=dict(type="log"))

    fig.update_layout(yaxis1=dict(title='平均報酬增加'), yaxis3=dict(title=f'{x}'))
    fig.update_layout(xaxis4=dict(autorange="reversed"))
    fig.update_layout(hovermode="x")
    fig.update_layout(xaxis3=dict(title="n trades"),xaxis4=dict(title="n trades"))
    fig.update_layout(showlegend=False)
    return fig
