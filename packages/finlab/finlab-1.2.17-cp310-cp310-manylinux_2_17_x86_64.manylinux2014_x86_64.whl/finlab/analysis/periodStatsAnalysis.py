import numpy as np
import pandas as pd
from finlab.analysis import Analysis

class PeriodStatsAnalysis(Analysis):

    def __init__(self):
        """分析台股策略的不同時期與大盤指標作比較

        Examples:
            可以執行以下程式碼來產生分析結果：

            ``` py
            report.run_analysis('PeriodStatsAnalysis')
            ```

            產生的結果：

            
            |                                      |   benchmark |   strategy |
            |:-------------------------------------|------------:|-----------:|
            | ('overall_daily', 'calmar_ratio')    |   0.149192  |  0.0655645 |
            | ('overall_daily', 'sortino_ratio')   |   0.677986  |  0.447837  |
            | ('overall_daily', 'sharpe_ratio')    |   0.532014  |  0.306351  |
            | ('overall_daily', 'profit_factor')   |   1.20022   |  1.07741   |
            | ('overall_daily', 'tail_ratio')      |   0.914881  |  0.987751  |
            | ('overall_daily', 'return')          |   0.0835801 |  0.0478957 |
            | ('overall_daily', 'volatility')      |   0.182167  |  0.312543  |
            | ('overall_monthly', 'calmar_ratio')  |   0.155321  |  0.0731378 |
            | ('overall_monthly', 'sortino_ratio') |   0.697382  |  0.439003  |
            | ('overall_monthly', 'sharpe_ratio')  |   0.524943  |  0.307292  |
            | ('overall_monthly', 'profit_factor') |   1.75714   |  1.27059   |
            | ('overall_monthly', 'tail_ratio')    |   1.03322   |  0.903335  |
            | ('overall_monthly', 'return')        |   0.0836545 |  0.0479377 |
            | ('overall_monthly', 'volatility')    |   0.186989  |  0.316178  |
            | ('overall_yearly', 'calmar_ratio')   |   0.436075  |  0.127784  |
            | ('overall_yearly', 'sortino_ratio')  |   0.738327  |  0.694786  |
            | ('overall_yearly', 'sharpe_ratio')   |   0.407324  |  0.350986  |
            | ('overall_yearly', 'profit_factor')  |   2.2       |  1.66667   |
            | ('overall_yearly', 'tail_ratio')     |   1.71647   |  1.359     |
            | ('overall_yearly', 'return')         |   0.0814469 |  0.0663674 |
            | ('overall_yearly', 'volatility')     |   0.284742  |  0.419087  |
        """
        self.results = None

        def safe_division(n, d):
            return n / d if d else 0

        calc_cagr = (
            lambda s: (s.add(1).prod()) ** safe_division(365.25, (s.index[-1] - s.index[0]).days) - 1 
            if len(s) > 1 else 0)

        def calc_calmar_ratio(pct):
            s = pct.add(1).cumprod().iloc[1:]
            return safe_division(calc_cagr(pct), abs(s.calc_max_drawdown()))

        self.metrics = [
                ("calmar_ratio", calc_calmar_ratio),
                ('sortino_ratio', lambda s: safe_division(s.mean(), s[s < 0].std())
                    * (safe_division(len(s), (s.index[-1] - s.index[0]).days) * 365) ** 0.5),
                ('sharpe_ratio', lambda s: safe_division(s.mean(), s.std())
                    * (safe_division(len(s), (s.index[-1] - s.index[0]).days) * 365) ** 0.5),
                ('profit_factor', lambda s: safe_division((s > 0).sum(), (s < 0).sum())),
                ('tail_ratio', lambda s: -safe_division(s.quantile(0.95), (s.quantile(0.05)))),
                ('return', lambda s: calc_cagr(s)),
                ('volatility', lambda s: s.std() * np.sqrt(safe_division(len(s), (s.index[-1] - s.index[0]).days) * 365)),
                ]

    def calc_stats(self, series):

        ########################################
        # calculate yearly metric performance
        ########################################
        pct = series.pct_change().fillna(0)

        def eval_f(m, s):
            if isinstance(m, str):
                return getattr(s, m)()
            else:
                return m[1](s)


        yearly = {}

        for m in self.metrics:

            name = m if isinstance(m, str) else m[0]
            s = pct.groupby(pct.index.year).apply(lambda s: eval_f(m, s))
            yearly[name] = s.values.tolist()

        yearly['year'] = s.index.values.tolist()

        ########################################
        # calculate recent days performance
        ########################################
        recent_days = [20, 60, 120, 252, 756]
        recent = {}
        for m in self.metrics:
            name = m if isinstance(m, str) else m[0]
            recent[name] = []
            for d in recent_days:
                recent[name].append(eval_f(m, pct.iloc[-d:]))

        recent['days'] = recent_days

        ########################################
        # calculate overall performance
        ########################################
        overall_daily = {}
        overall_monthly = {}
        overall_yearly = {}

        pct_m = series.resample('M').last().dropna().pct_change().iloc[1:]
        pct_y = series.resample('Y').last().dropna().pct_change().iloc[1:]

        for m in self.metrics:
            name = m if isinstance(m, str) else m[0]
            overall_daily[name] = eval_f(m, pct)
            overall_monthly[name] = eval_f(m, pct_m) if len(pct_m) > 1 else 0
            overall_yearly[name] = eval_f(m, pct_y) if len(pct_y) > 1 else 0

        return {'yearly': yearly, 
                'recent': recent, 
                'overall_daily': overall_daily, 
                'overall_monthly': overall_monthly, 
                'overall_yearly': overall_yearly}

    def analyze(self, report):

        ret = {}
        ret['strategy'] = self.calc_stats(report.daily_creturn)
        ret['benchmark'] = self.calc_stats(report.daily_benchmark)

        self.results = ret

        return ret

    def display(self):

        if self.results is None:
            return

        from IPython.display import HTML

        t = ''
        result = self.results
        result['benchmark']['recent']['days'] = ['M', 'Q', 'HY', 'Y', '3Y']
        result['strategy']['recent']['days'] = ['M', 'Q', 'HY', 'Y', '3Y']

        df = pd.DataFrame({'benchmark': pd.DataFrame({cat: result['benchmark'][cat] for cat in ['overall_daily', 'overall_monthly', 'overall_yearly']}).unstack(),
        'strategy': pd.DataFrame({cat: result['strategy'][cat] for cat in ['overall_daily', 'overall_monthly', 'overall_yearly']}).unstack()})

        def highlight_max(s, props=''):
            return np.where(s == np.nanmax(s.values), props, '')

        t += df.style.apply(highlight_max, props='color:white;color:blue', axis=1).to_html()

        for cat in ['yearly', 'recent']:

            metric_names = result['strategy'][cat].keys()

            index_name = {
                'yearly': 'year',
                'recent': 'days',
            }[cat]

            for mname in metric_names:

                if mname == index_name:
                    continue

                df = pd.DataFrame([result['strategy'][cat][mname], result['benchmark'][cat][mname]], columns=result['strategy'][cat][index_name], index=['strategy', 'benchmark'])

                def make_pretty(styler, df, title):
                    styler.set_caption(title)
                    styler.background_gradient(axis=None, vmin=df.min().min(), vmax=df.max().max(), cmap="YlGnBu")
                    return styler

                t += df.style.format(precision=2).pipe(lambda v: make_pretty(v, df, mname)).to_html() + '<br />'
        return HTML(t)
