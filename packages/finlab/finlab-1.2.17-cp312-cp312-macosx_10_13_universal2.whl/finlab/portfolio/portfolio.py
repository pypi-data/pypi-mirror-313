import copy
import gzip
import json
import base64
import logging
import datetime
import requests
import numpy as np
import pandas as pd
from typing import NamedTuple, Dict, Tuple, Union

import finlab
from finlab.market_info import MarketInfo, TWMarketInfo
from finlab.core.report import Report

logger = logging.getLogger(__name__)


class PositionScheduler(NamedTuple):
    weights: pd.Series
    next_weights: pd.Series
    is_resample: bool
    actions: pd.Series
    next_trading_date: datetime.datetime
    trade_at: str
    market_info: MarketInfo
    stop_loss: float
    take_profit: float
    trail_stop: float
    total_weight: float = 1.0

    @classmethod
    def from_report(cls, report, total_weight):
        return cls(report.weights, report.next_weights, 
                   isinstance(report.resample, str), report.actions, 
                   report.next_trading_date, report.trade_at, 
                   report.market_info, report.stop_loss or 1, 
                   report.take_profit or np.inf,
                   report.trail_stop or 1, total_weight)

    @classmethod
    def _from_json_leaf(cls, pdata):

        next_trading_date = datetime.datetime.fromisoformat(pdata['positionConfig']['scheduled'])

        pp_df = pd.DataFrame(pdata['positions'])
        pp_df.index = pp_df.assetId + ' ' + pp_df.assetName
        weight = pp_df.currentWeight
        weight.name = 'weight'
        weight = weight[weight != 0]
        # drop duplicate index
        weight = weight[~weight.index.duplicated(keep='first')]
        next_weight = pp_df.nextWeight
        next_weight.name = 'next_weight'
        next_weight = next_weight[~next_weight.index.duplicated(keep='first')]
        next_weight = next_weight[next_weight != 0]
        actions = pp_df.action.map(
            lambda d: d['reason']).pipe(lambda d: d[d != '_'])
        total_weight = pdata['positionConfig']['weight'] if 'weight' in pdata['positionConfig'] else 1.0
        is_resample = pdata['positionConfig']['resample'] is not None

        # if pdata['positionConfig']['market'] == 'tw_stock':
        market_info = TWMarketInfo()
        # else:
        #     raise ValueError('Unknown market')


        return cls(weight, next_weight, is_resample, 
                   actions, next_trading_date, 
                   pdata['positionConfig']['entryTradePrice'], market_info, 
                   pdata['positionConfig'].get('sl', 1), 
                   pdata['positionConfig'].get('tp', np.inf), 
                   pdata['positionConfig'].get('ts', np.inf),
                   total_weight)

    @staticmethod
    def from_json(position):

        leaf_position = 'positionConfig' in position

        if leaf_position:
            return PositionScheduler._from_json_leaf(position)

        merged = {}
        for name, pp in position.items():
            merged[name] = PositionScheduler._from_json_leaf(pp)

        return merged

    @classmethod
    def from_cloud(cls, strategy_id):

        url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_get_strategy'

        res = requests.get(url, {
            'api_token': finlab.get_token(),
            'sid': strategy_id,
        })

        if res.status_code != 200:
            raise Exception(res.text)

        data = res.json()

        if data['position'] is None:
            raise Exception('No position data found')

        data = data['position']

        # pick the current version format
        if 'position2' in data:
            data = data['position2']

        # if 'position2' not existed, which means the structure is refactored
        elif 'position' in data:
            data = data['position']

        return PositionScheduler.from_json(data)
    
    def __repr__(self):
        return '<PortfolioScheduler>'



class Portfolio(Report):

    def __init__(self, reports: Union[Dict[str, Tuple[Report, float]], Report]):
        """建構 Portfolio 物件。

            Parameters:
                - reports (Dict[str, Tuple[Report, float]]): 代表投資組合的字典，key 為資產名稱，value 是回測報告與部位。
                A dictionary representing the portfolio, where the keys are the names of the assets and the values are tuples containing the asset's report and weight.


            Example:
                **組合多個策略**
                ```
                from finlab import sim
                from finlab.portfolio import Portfolio

                # 請參閱 sim 函數的文件以獲取更多信息
                # https://doc.finlab.tw/getting-start/

                report_strategy1 = sim(...)
                report_strategy2 = sim(...)
                report_strategy3 = sim(...)

                portfolio = Portfolio({
                    'strategy1': (report_strategy1, 0.3),
                    'strategy2': (report_strategy2, 0.4),
                    'strategy3': (report_strategy3, 0.3),
                })
                ```
        """

        # mind user about this is the beta version
        logger.info(
            "Portfolio is in beta version, please report any issue to FinLab Team at https://discord.gg/tAr4ysPqvR")
        
        if isinstance(reports, Report):
            reports = {'strategy': (reports, 1.0)}

        # calculate overall creturn using daily return (portfolio['name'][1].creturn) and weight (portfolio['name'][0])
        # creating pct df
        self.portfolio = reports
        pct = pd.DataFrame({k: v[0].creturn.pct_change()
                           for k, v in reports.items()})
        weight = pd.Series({k: v[1] for k, v in reports.items()})

        # calculate overall creturn
        creturn = (pct * weight).sum(axis=1).add(1).cumprod()
        self.creturn = creturn

        # calculate position
        position = sum([v[0].position * weight.loc[k]
                       for k, v in reports.items()])
        self.position = position.fillna(0)

        # get any fee ratio from report
        sample_report = next(iter(reports.values()))[0]
        fee_ratio = sample_report.fee_ratio
        tax_ratio = sample_report.tax_ratio
        trade_at = sample_report.trade_at
        next_trading_date = min(
            [v[0].next_trading_date for k, v in reports.items()])
        market_info = sample_report.market_info

        super().__init__(creturn, self.position, fee_ratio, tax_ratio,
                         trade_at, next_trading_date, market_info)

        self.trades = pd.concat([v[0].trades for k, v in reports.items()])\
            .sort_values('entry_sig_date').reset_index(drop=True).tail(500)
        self.trades.index.name = 'trade_index'
        self.trades.sort_values('entry_sig_date', inplace=True)
        self.trades.reset_index(drop=True, inplace=True)
        self.trades = self.trades.tail(500)

        self.live_performance_start = self.trades.entry_sig_date.min()
        self.stop_loss = None
        self.take_profit = None
        self.trail_stop = None
        self.resample = None

        self.position_schedulers = {}

        for name, (report, weight) in reports.items():
            
            if '|' in name:
                raise ValueError('name should not contain "|"')
            
            if hasattr(report, 'position_schedulers'):
                if isinstance(report.position_schedulers, dict):
                    for sub_name, sub_scheduler in report.position_schedulers.items():
                        self.position_schedulers[name + '|' + sub_name] = sub_scheduler._replace(total_weight=sub_scheduler.total_weight * weight)
                else:
                    self.position_schedulers[name] = report.position_schedulers._replace(total_weight=report.position_schedulers.total_weight * weight)
            else:                
                if isinstance(report, Report):
                    self.position_schedulers[name] = PositionScheduler.from_report(report, weight)


        # check if the self.position_scheduler is a dict of PositionScheduler
        if not isinstance(self.position_schedulers, dict):
            raise ValueError('position_schedulers should be a dict of PositionScheduler')
        
        for name, scheduler in self.position_schedulers.items():
            if not isinstance(scheduler, PositionScheduler):
                raise ValueError('position_schedulers should be a dict of PositionScheduler')
            
            if not isinstance(scheduler.weights, pd.Series):
                print(name)
                raise ValueError('weights should be a pd.Series')
            
            if not isinstance(scheduler.next_weights, pd.Series):
                print(name)
                raise ValueError('next_weights should be a pd.Series')

    @classmethod
    def from_weight_function(cls, reports, weight_function):

        creturns = pd.DataFrame({k: r.creturn for k, r in reports.items()})
        weight = weight_function()
        assert creturns.columns in weight.columns
        assert weight.iloc[-1].notna().all()

        current_weight = weight.iloc[-1]
        ret = cls({k: (r, current_weight[k]) for k, r in reports.items()})
        ret.creturn = (creturns.pct_change() *
                       weight).sum(axis=1).add(1).cumprod()
        return ret

    def position_info2(self):

        # get position info for all reports in self.portfolio
        position = {}

        for name, (report, weight) in self.portfolio.items():
            pinfo = report.position_info2()
            # pinfo['market'] = report.market_info.get_name()

            if 'positionConfig' in pinfo:
                pinfo['positionConfig']['weight'] = weight
                position[name] = pinfo

            # handle recursive position
            else:
                for sub_name, sub_position in pinfo.items():
                    sub_position['positionConfig']['weight'] *= weight
                    position[f'{name}|{sub_name}'] = sub_position

        return position
