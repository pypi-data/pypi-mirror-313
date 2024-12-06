from finlab.online.order_executor import Position, OrderExecutor
from finlab.online.enums import OrderCondition
from finlab.market_info import TWMarketInfo, get_market_info_by_name
from dataclasses import dataclass, field
from typing import Dict, Tuple, List, Optional
import pandas as pd
import requests
import datetime
import logging
import json
import copy
import math
import os

import finlab
from finlab.core.report import Report
from finlab.utils import get_tmp_dir
from .portfolio import Portfolio, PositionScheduler

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)


def position_type_check(position_name, data):
    if not isinstance(data.get('timestamp'), str):
        logger.warning(f"{position_name}: timestamp must be a string, got {type(data.get('timestamp'))} instead")
    if not isinstance(data.get('next_trading_time'), str):
        logger.warning(f"{position_name}: next_trading_time must be a string")
    if not isinstance(data.get('position'), list):
        logger.warning(f"{position_name}: position must be a float or int, got {type(data.get('position'))} instead")
    if not isinstance(data.get('allocation'), (float, int)):
        logger.warning(f"{position_name}: allocation must be a float or int, got {type(data.get('allocation'))} instead")
    if not isinstance(data.get('weight'), (float, int)):
        logger.warning(f"{position_name}: weight must be a float or int, got {type(data.get('weight'))} instead")
    if not isinstance(data.get('entry_at'), str):
        logger.warning(f"{position_name}: entry_at must be a string, got {type(data.get('entry_at'))} instead")
    if not isinstance(data.get('exit_at'), str):
        logger.warning(f"{position_name}: exit_at must be a string, got {type(data.get('exit_at'))} instead")
    if not isinstance(data.get('market'), str):
        if data.get('market', None) is None:
            data['market'] = 'tw_stock'
    if not isinstance(data.get('stop'), list):
        logger.warning(f"{position_name}: stop must be a list, got {type(data.get('stop'))} instead")
    if data.get('stop_loss') is not None and not isinstance(data.get('stop_loss'), (float, int)):
        logger.warning(f"{position_name}: stop_loss must be a float or int, got {type(data.get('stop_loss'))} instead")
    if data.get('take_profit') is not None and not isinstance(data.get('take_profit'), (float, int)):
        logger.warning(f"{position_name}: take_profit must be a float or int, got {type(data.get('take_profit'))} instead")
    if data.get('trail_stop') is not None and not isinstance(data.get('trail_stop'), (float, int)):
        logger.warning(f"{position_name}: trail_stop must be a float or int, got {type(data.get('trail_stop'))} instead")


def replace_inf_nan(data):
    if isinstance(data, float):
        if math.isinf(data) or math.isnan(data):
            return None
        return data
    elif isinstance(data, dict):
        return {k: replace_inf_nan(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_inf_nan(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(replace_inf_nan(item) for item in data)
    elif isinstance(data, set):
        return {replace_inf_nan(item) for item in data}
    else:
        return data


class PortfolioSyncManager():
    """
    投資組合類別，用於設定和獲取投資組合資訊。

    Attributes:
        path (str): 投資組合資訊的儲存路徑。

    Methods:
        __init__(self, path=None): 初始化投資組合類別。
        set(self, portfolio:Dict[str, Tuple[int, Report]]): 設定投資組合的函數。
        get_position(self, combined=True): 獲取持倉資訊。

    Examples:
        ```py
        from finlab.portfolio import Portfolio, PortfolioSyncManager

        # 初始化投資組合
        port = Portfolio({'策略A': (report1, 0.3), '策略B': (report2, 0.7)})

        # 設定投資組合
        # pm = PortfolioSyncManager.from_local() or 
        # pm = PortfolioSyncManager.from_cloud()
        pm = PortfolioSyncManager() 
        pm.update(port, total_balance=1000000)
        pm.to_cloud() # pm.to_local()

        print(pm)

        # 下單
        account = ... # 請參考 Account 產生方式
        pm.sync(account) # 平盤價格下單
        ```
    """

    LOCAL_DIR = os.path.join(get_tmp_dir(), 'workspace')
    CLOUD_URL = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_portfolio'

    def __init__(self, data:Optional[Dict]=None, start_with_empty=False):
        """建構投資組合。
        """

        if data and 'position' in data:
            for k, v in data['position'].items():
                position_type_check(k, v)

        self.data = data or {'position': {}, 'history': {}, 'market': None, 'config':{}}
        self._start_with_empty = start_with_empty

    @classmethod
    def _get_local_path(cls, name):
        if not os.path.exists(cls.LOCAL_DIR):
            os.makedirs(cls.LOCAL_DIR)
        return os.path.join(cls.LOCAL_DIR, f'{name}.position.json')


    @classmethod
    def from_local(cls, name='default'):
        """
        從本地檔案初始化投資組合。

        Args:
            path (str): 本地檔案的路徑。

        Returns:
            PortfolioSyncManager: 投資組合類別。
        """
        path = cls._get_local_path(name)

        if not os.path.exists(path):
            raise FileNotFoundError(f'path {path} not existed')

        with open(path, 'r') as f:
            data = json.load(f)

        return cls(data)


    @classmethod
    def from_cloud(cls, name='default'):
        """
        從雲端檔案初始化投資組合。

        Args:
            path (str, optional): 雲端檔案的路徑。預設為 'default'。

        Returns:
            PortfolioSyncManager: 投資組合類別。
        """
        url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_portfolio'
        res = requests.post(cls.CLOUD_URL, params={
            'pid': name,
            'api_token': finlab.get_token(),
            'action': 'get'
            }, timeout=30)
        
        data = res.json()

        if data == None:
            raise FileNotFoundError(f'path {name} not existed')

        return cls(data)

    @classmethod
    def from_path(cls, path):
        """
        從本地檔案初始化投資組合。

        Args:
            path (str): 本地檔案的路徑。

        Returns:
            PortfolioSyncManager: 投資組合類別。
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f'path {path} not existed')

        with open(path, 'r') as f:
            data = json.load(f)

        return cls(data)
    
    def to_local(self, name='default'):
        """
        將投資組合資訊存至本地檔案。

        Returns:
            None
        """
        path = self._get_local_path(name)

        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4, default=str)

    def to_cloud(self, name='default'):
        """
        將投資組合資訊存至雲端檔案。

        Returns:
            None
        """
        res = requests.post(self.CLOUD_URL, params={
            'pid': name,
            'api_token': finlab.get_token(),
            'action': 'set'
        }, json=replace_inf_nan(self.data), timeout=30)
        return res
    
    def to_path(self, path):
        """
        將投資組合資訊存至本地檔案。

        Returns:
            None
        """
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4, default=str)


    @staticmethod
    def _calc_position_value(position, lot, price):

        ret = 0

        for p in position:
            if p['stock_id'] in price:
                num = float(p['quantity']) * float(price[p['stock_id']]) * lot
                if num == num:
                    ret += num
                else:
                    logger.warning(f'price of {p["stock_id"]} is {price[p["stock_id"]]}, quantity is {p["quantity"]}')
            else:
                raise ValueError(f'stock {p["stock_id"]} not found')

        return ret
    
    def update_same_config(self, portfolio):

        if 'config' not in self.data:
            raise ValueError('config not found')

        params = self.data['config']['params']
        kwargs = params.pop('kwargs', {})
        params.update(kwargs)

        self.update(portfolio, **params)


    def update(self, portfolio: Portfolio, total_balance=0, rebalance_safety_weight=0.2, smooth_transition=None, force_override_difference=False, custom_position=None, excluded_stock_ids:Optional[List[str]]=None, **kwargs):
        """
        設定投資組合的函數。

        Args:
            portfolio (Portfolio): 包含投資組合資訊的字典。
            total_balance (float): 總資產。
            rebalance_safety_weight (float): 現金的權重，確保以市價買賣時，新的策略組合價值不超過舊的價值，計算方式為：賣出股票後，有多少比例要變成現金(例如 20％)，再買入新的股票。
            smooth_transition (bool): 是否只在換股日才更新，預設為 None，系統會自行判斷，假如第一次呼叫函示，會是 False，之後會是 True。
            force_override_difference (bool): 是否強制覆蓋不同的部位，預設為 False。
            custom_position (Position or dict): 自定義部位，預設為 None。當 custom_position 不為 None 時，會將 custom_position 加入到部位中。程式在計算部位時，會將 custom_position 排除在外，不列入。
            excluded_stock_ids (List[str], optional): 排除的股票代碼列表。預設為 None。

        Returns:
            None

        Examples:
            ```py
            from finlab.backtest import sim
            from finlab.portfolio import Portfolio, OnlineReport

            # create report 1
            report1 = sim(...) # 請參考回測語法

            # download online report
            report2 = OnlineReport.from_cloud('strategyName') # 下載策略報告

            # create portfolio
            portfolio = Portfolio({'策略1': (report1, 0.5), '策略2': (report2, 0.5)})

            # create PortfolioSyncManager
            pm = PortfolioSyncManager.from_cloud()
            pm.update(portfolio, total_balance=1000000, cash_weight=0.2) # 投資 100 萬元

            # create orders
            account = ... # 請參考 Account 產生方式
            pm.sync(account) # 平盤價格下單
            pm.sync(account, market_order=True) # 市價下單
            ```
        """

        # check the type is portfolio
        if not isinstance(portfolio, Portfolio):
            if isinstance(portfolio, Report):
                portfolio = Portfolio(portfolio)
            else:
                raise ValueError(f'portfolio should be Portfolio or Report object, got {type(portfolio)}')
            
        # update config
        self.data['config'] = {
            'weights': {k.split('|')[0]: v.total_weight for k, v in portfolio.position_schedulers.items()},
            'params': {
                'total_balance': total_balance,
                'rebalance_safety_weight': rebalance_safety_weight,
                'smooth_transition': smooth_transition,
                'force_override_difference': force_override_difference,
                'kwargs': kwargs
            }
        }

        if custom_position:
            if isinstance(custom_position, dict):
                custom_position = Position(custom_position).to_list()
            elif isinstance(custom_position, Position):
                custom_position = custom_position.to_list()
            else:
                raise ValueError(f'custom_position should be Position or dict object, got {type(custom_position)}')
            self.data['config']['custom_position'] = custom_position

        if excluded_stock_ids:
            self.data['config']['excluded_stock_ids'] = excluded_stock_ids

        portfolio = portfolio.position_schedulers

        # check the file exists
        position = self.data['position']
        history = self.data['history']
        now = datetime.datetime.now().astimezone()

        if smooth_transition == None:
            if len(position) == 0 and len(history) == 0 and not self._start_with_empty:
                smooth_transition = False
            else:
                smooth_transition = True

        removed_position = []

        for sid in position:
            if sid not in portfolio:
                next_trading_time = datetime.datetime.fromisoformat(
                    position[sid]['next_trading_time'])
                
                if 'market' in position[sid]:
                    market = get_market_info_by_name(position[sid]['market'])
                    last_market_timestamp = market.get_price('close').index[-1]
                    last_market_timestamp = market.market_close_at_timestamp(last_market_timestamp)

                    if last_market_timestamp == position[sid]['next_trading_time']:
                        logger.info(f'remove {sid} from portfolio')
                        removed_position.append(sid)
                        continue

                result = input(f'{sid} not in portfolio, remove? (y/n): ')

                if result == 'y':
                    logger.info(f'remove {sid} from portfolio')
                    removed_position.append(sid)

            elif sid in portfolio and portfolio[sid].total_weight == 0:

                market = portfolio[sid].market_info
                last_market_timestamp = market.get_price('close').index[-1]

                if last_market_timestamp == portfolio[sid].next_trading_date:
                    logger.info(f'remove {sid} from portfolio')
                    removed_position.append(sid)

        for sid in removed_position:
            if sid not in history:
                history[sid] = []
            
            history[sid].append(position[sid])
            position.pop(sid)
            

        #####################################
        # Identify strategies to update
        #####################################
        updated_strategies = []
        # import pdb; pdb.set_trace()
        for sid, allocation in portfolio.items():

            market = allocation.market_info
            weight = allocation.total_weight

            if weight == 0 and sid not in position:
                continue

            # calc next trading time
            if not hasattr(market, 'market_close_at_timestamp'):
                raise ValueError('market_close_at_timestamp not implemented')

            next_trading_time = market.market_close_at_timestamp(
                allocation.next_trading_date)
            
            # if the next_trading_time is updated, that means
            soft_condition = sid not in position or weight != position[sid]['weight']

            if allocation.is_resample:
                # if resample is enable, then the next trading date is in futures
                is_trading_date = now > next_trading_time
            else:
                # if not enable, then the resample date is in pass
                if sid in position:
                    is_same_portfolio = (next_trading_time.isoformat() 
                            == position[sid]['next_trading_time'])
                    is_trading_date = (now > next_trading_time) and not is_same_portfolio
                else:
                    last_market_timestamp = market.market_close_at_timestamp(market.get_price('close').index[-1])
                    is_trading_date = (now > next_trading_time) and next_trading_time == last_market_timestamp

            if is_trading_date or (not smooth_transition and soft_condition):
            # if sid not in position or now > next_trading_time or weight != position[sid]['weight']:
                updated_strategies.append(sid)

                # add sid to portfolio
                if sid not in position:
                    logger.info(f'add {sid} to portfolio')
                else:
                    reason = 'weight changed' if weight != position[sid][
                        'weight'] else f'now > next trading date {next_trading_time}'
                    logger.info(f'update {sid} in portfolio because {reason}')

        #####################################
        # Check the position is the same
        #####################################
        for sid, info in position.items():
            if sid in updated_strategies:
                continue

            if sid not in portfolio:
                logger.warning(f'{sid} not in portfolio')
                continue

            # check if the current stock list is the same
            position_sids = sorted([p['stock_id'] for p in info['position']])
            report = portfolio[sid]
            report_ids = [s.split(' ')[0]
                          for s in sorted(report.weights.index.tolist())]
            
            # check position_ids is a subset of report_ids
            if not all([s in report_ids for s in position_sids]):
                logger.warning(f'{sid} has changed stock list')
                logger.warning(f'current: {position_sids}')
                logger.warning(f'report: {report_ids}')

                if force_override_difference:
                    logger.warning('force override')
                    updated_strategies.append(sid)
                else:
                    logger.warning(
                        'please set force_override=True to override')

        #####################################
        # Update position
        #####################################
        asset_value = 0
        total_update_weight = 0

        for sid in updated_strategies:
            total_update_weight += portfolio[sid].total_weight


        lot = market.get_odd_lot()
        price = market.get_price('close', adj=False).ffill().iloc[-1]

        for sid, info in position.items():
            if sid not in updated_strategies:
                asset_value += self._calc_position_value(
                    info['position'], lot=lot, price=price)

        liquid_value = min(total_balance - asset_value,
                         total_update_weight * total_balance)
        rebalance_safety_fund = liquid_value * rebalance_safety_weight
        cash = total_balance - asset_value - liquid_value
        free_value = max(liquid_value - max(0, rebalance_safety_fund - cash), 0)

        display_info = {
            '投資總額': total_balance,
            '預計股票價值': asset_value,
            '預計賣出後流動資金': liquid_value,
            '預計保留現金': rebalance_safety_fund,
            '預計可買入金額': free_value,
        }

        # pretty print the display info
        for k, v in display_info.items():
            logger.info('%s: %d (%.2f%%)', k, int(v), v/total_balance * 100)

        for sid in updated_strategies:
            allocation = portfolio[sid]

            if not isinstance(allocation, PositionScheduler):
                raise ValueError(f'portfolio[{sid}] should be PositionScheduler, got {type(allocation)}')

            weight = allocation.total_weight
            report = allocation

            fund = free_value * weight / total_update_weight

            # calc next trading time
            next_trading_time = report.market_info.market_close_at_timestamp(
                report.next_trading_date)
            
            market = allocation.market_info
            last_market_timestamp = market.market_close_at_timestamp(market.get_price('close').index[-1])

            try:
                pos = Position.from_report(allocation, fund, **kwargs).to_list()
            except AssertionError as e:
                logger.warning(f"Cannot create position for {sid}, because {e}"
                               "Set the position to zero.")
                
                pos = []


            if sid in position:
                history[sid] = history.get(sid, [])

                while len(history[sid]) != 0 and history[sid][-1]['next_trading_time'] == next_trading_time.isoformat():
                    history[sid].pop()

                history[sid].append(position[sid])

            position[sid] = {
                'timestamp': now.isoformat(),
                'next_trading_time': next_trading_time.isoformat(),
                'position': pos,
                'allocation': fund,
                'weight': weight,
                'entry_at': report.trade_at if isinstance(report.trade_at, str) else 'close',
                'exit_at': report.trade_at if isinstance(report.trade_at, str) else 'close',
                'stop': [],
                'stop_loss': report.stop_loss,
                'take_profit': report.take_profit if report.take_profit == report.take_profit else None,
                'trail_stop': report.trail_stop if report.trail_stop == report.trail_stop else None,
                'market': allocation.market_info.get_name(),
                'last_market_timestamp': last_market_timestamp.isoformat(),
            }
            logger.info(f'update position {sid}')

        for sid, allocation in portfolio.items():

            if sid not in position:
                continue

            next_trading_time = allocation.market_info.market_close_at_timestamp(
                allocation.next_trading_date)
            

            if not isinstance(allocation, PositionScheduler):
                raise ValueError(f'portfolio[{sid}] should be PositionScheduler, got {type(allocation)}')
            
            report = allocation

            if allocation.actions.isin(['sl_', 'tp_', 'sl', 'tp']).any():
                # find stock id of sl and tp and reset its position to zero
                for s in allocation.actions[allocation.actions.isin(['sl_', 'tp_', 'sl', 'tp'])].index.tolist():
                    stock_id = s.split(' ')[0]
                    for p in position[sid]['position']:
                        if p['stock_id'] == stock_id and p['quantity'] != 0:
                            logger.info(f'{sid} {s} has a {allocation.actions[s]} signal, position set to zero')
                            position[sid]['stop'].append(p.copy())
                            position[sid]['stop'][-1]['timestamp'] = now.isoformat()
                            position[sid]['stop'][-1]['reason'] = allocation.actions.to_dict().get(s, None)
                            p['quantity'] = 0

            if allocation.actions.isin(['sl_enter', 'tp_enter']).any() and now < next_trading_time:
                # find stock id of sl and tp and reset its position to zero if it is not the next trading date
                for s in allocation.actions[allocation.actions.isin(['sl_enter', 'tp_enter'])].index.tolist():
                    stock_id = s.split(' ')[0]
                    for p in position[sid]['position']:
                        if p['stock_id'] == stock_id and p['quantity'] != 0:
                            logger.info(f'{sid} {s} has a {allocation.actions[s]} signal, position set to zero')
                            position[sid]['stop'].append(p.copy())
                            position[sid]['stop'][-1]['timestamp'] = now.isoformat()
                            position[sid]['stop'][-1]['reason'] = allocation.actions.to_dict().get(s, None)
                            p['quantity'] = 0


    def get_last_market_timestamp(self):
        timestamps = [sdata.get('last_market_timestamp') for sid, sdata in self.data['position'].items() if 'last_market_timestamp' in sdata]
        if len(timestamps) == 0:
            return None
        return max(timestamps)


    def get_strategy_position(self, strategy_name, at):
        """
        獲取策略的開倉部位。

        Args:
            strategy_name (str): 策略名稱。

        Returns:
            dict: 開倉部位資訊。
        """

        strategy_position = self.data['position'].get(strategy_name, {})

        # if trade at open, means close and open position are the same

        # TODO: filter the position is entry trade or exit trade
        # for now, we just assume the exit_at is the same as entry_at
        assert strategy_position.get('entry_at', 'close') == strategy_position.get('exit_at', 'close'), \
            'entry_at and exit_at difference is not supported'
        
        market = get_market_info_by_name(strategy_position['market'])

        has_market_timestamp = strategy_position.get('last_market_timestamp', None) is not None
        is_trade_at_open = strategy_position['entry_at'] == 'open'
        last_market_timestamp_is_the_same = strategy_position.get('last_market_timestamp', None)\
            == market.market_close_at_timestamp(market.get_price('close').index[-1]).isoformat()

        # print(market.market_close_at_timestamp(market.get_price('close').index[-1]).isoformat())
        # print(strategy_position.get('last_market_timestamp', None))

        # print('last_market_timestamp_not_defined', last_market_timestamp_not_defined)
        # print('is_trade_at_open', is_trade_at_open)
        # print('last_market_timestamp_is_the_same', last_market_timestamp_is_the_same)

        # latest_market_timestamp = max(
        #     [sdata.get('last_market_timestamp') for sid, sdata in self.data['position'].items() if 'last_market_timestamp' in sdata])
        
        latest_market_timestamp = self.get_last_market_timestamp()
        
        use_previous_position = (
            (
                (at == 'open')
                and has_market_timestamp
                and last_market_timestamp_is_the_same
                and not is_trade_at_open)
            or
            (
                (at == 'prev_close')
                and (latest_market_timestamp == strategy_position.get('last_market_timestamp', None))
            )
        )
        
        if not use_previous_position:
            return strategy_position['position']
        
        # try to find the previous position, 
        # since at the time of the next trading date, the position is not updated
        strategy_history = self.data['history'].get(strategy_name, [])
        if len(strategy_history) == 0:
            return []

        if strategy_history[-1].get('last_market_timestamp', None) == strategy_position.get('last_market_timestamp', None):
            if len(strategy_history) >= 2:
                return strategy_history[-2]['position']
            else:
                return []
        return strategy_history[-1]['position']


    def get_position(self, at='close', market_name=None):
        """
        獲取持倉資訊。

        Args:
            market_name (str, optional): 指定市場名稱。預設為 None，也就是獲取所有市場。

        Returns:
            dict or Position: 若 combined 為 True，則返回合併後的持倉資訊（Position 物件）；
                                若 combined 為 False，則返回原始持倉資訊（dict）。
        """
        position = self.data['position']
        positions = {pname: Position.from_list(self.get_strategy_position(pname, at)) for pname in position.keys()}

        for pname, pos in positions.items():
            for p in pos:
                if 'weight' in p:
                    p['weight'] *= self.data['position'][pname]['weight']
                else:
                    p['weight'] = 1 / len(pos.position) * self.data['position'][pname]['weight']

        if market_name is not None:
            positions = {pname: pos for pname, pos in positions.items() if self.data['position'][pname]['market'] == market_name}

        ret = sum(list(positions.values()), Position({}))

        if 'custom_position' in self.data['config']:
            ret += Position.from_list(self.data['config']['custom_position'])

        if 'excluded_stock_ids' in self.data['config']:
            ret2 = []
            for p in ret.position:
                if p['stock_id'] not in self.data['config']['excluded_stock_ids']:
                    ret2.append(p)
            ret = Position.from_list(ret2)
                        
        return ret

    def clear(self):
        """
        清除持倉資訊。

        Returns:
            None
        """
        self.data = {'position': {}, 'history': {}, 'market': None, 'config':{}}

    def sync(self, account, at='close', consider_margin_as_asset=True, market_name=None, **kwargs):
        """
        同步持倉資訊。

        Args:
            account (Account): 交易帳戶。
            consider_margin_as_asset (bool, optional): 是否將保證金交易視為資產。預設為 True。
            market_name (str, optional): 指定市場名稱。預設為 None，也就是獲取所有市場。
            market_order (bool): 以類市價盡量即刻成交：所有買單掛漲停價，所有賣單掛跌停價
            best_price_limit (bool): 掛芭樂價：所有買單掛跌停價，所有賣單掛漲停價
            view_only (bool): 預設為 False，會實際下單。若設為 True，不會下單，只會回傳欲執行的委託單資料(dict)
            extra_bid_pct (float): 以該百分比值乘以價格進行追價下單，如設定為 0.05 時，將以當前價的 +(-)5% 的限價進買入(賣出)，也就是更有機會可以成交，但是成交價格可能不理想；
                假如設定為 -0.05 時，將以當前價的 -(+)5% 進行買入賣出，也就是限價單將不會立即成交，然而假如成交後，價格比較理想。參數有效範圍為 -0.1 到 0.1 內。

        Returns:
            None
        """
        account_position = account.get_position()
        ideal_position = self.get_position(market_name=market_name, at=at)

        if consider_margin_as_asset:
            ideal_position = self.margin_cash_position_combine(account_position, ideal_position)

        oe = OrderExecutor(ideal_position, account)
        oe.create_orders(**kwargs)
        return oe

    def create_order_executor(self, account, at='close', consider_margin_as_asset=False, market_name=None, **kwargs):
        """
        同步持倉資訊。

        Args:
            account (Account): 交易帳戶。
            consider_margin_as_asset (bool, optional): 是否將融資融券視為資產。預設為 True。
            market_name (str, optional): 指定市場名稱。預設為 None，也就是獲取所有市場。
            market_order (bool): 以類市價盡量即刻成交：所有買單掛漲停價，所有賣單掛跌停價
            best_price_limit (bool): 掛芭樂價：所有買單掛跌停價，所有賣單掛漲停價
            view_only (bool): 預設為 False，會實際下單。若設為 True，不會下單，只會回傳欲執行的委託單資料(dict)
            extra_bid_pct (float): 以該百分比值乘以價格進行追價下單，如設定為 0.05 時，將以當前價的 +(-)5% 的限價進買入(賣出)，也就是更有機會可以成交，但是成交價格可能不理想；
                假如設定為 -0.05 時，將以當前價的 -(+)5% 進行買入賣出，也就是限價單將不會立即成交，然而假如成交後，價格比較理想。參數有效範圍為 -0.1 到 0.1 內。

        Returns:
            None
        """
        account_position = account.get_position()
        ideal_position = self.get_position(market_name=market_name, at=at)

        if consider_margin_as_asset:
            ideal_position = self.margin_cash_position_combine(account_position, ideal_position)

        return OrderExecutor(ideal_position, account)

    def __repr__(self):
        p = self.get_position()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.float_format', '{:.2f}'.format)

        market = TWMarketInfo()

        ref_price = market.get_reference_price()
        close_price = market.get_price(
            'close', adj=False).iloc[-1].to_dict()
        volume = market.get_price(
            'volume', adj=False).iloc[-1].to_dict()

        total_allocation = sum([v['allocation'] for v in self.data['position'].values()])

        pos = copy.deepcopy(self.data['position'])
        has_strategy = {}  # key: stock_id, value: str of strategies
        for name, info in pos.items():
            for stock in info['position']:
                if (stock['stock_id'], stock['order_condition']) not in has_strategy:
                    has_strategy[(stock['stock_id'],
                                  stock['order_condition'])] = name
                else:
                    has_strategy[(stock['stock_id'],
                                  stock['order_condition'])] += ',' + name

        if 'custom_position' in self.data['config']:
            for stock in self.data['config']['custom_position']:
                if (stock['stock_id'], stock['order_condition']) not in has_strategy:
                    has_strategy[(stock['stock_id'],
                                  stock['order_condition'])] = 'custom'
                else:
                    has_strategy[(stock['stock_id'],
                                  stock['order_condition'])] += ',custom'                  

        if len(p.position) != 0:

            df = pd.DataFrame(p.position)\
                .pipe(lambda df: df.assign(strategy=df.apply(lambda r: has_strategy.get((r.stock_id, r.order_condition), ''), axis=1)))\
                .pipe(lambda df: df.assign(type=df.order_condition.map(lambda v: OrderCondition(v).name)))

            df = df.pipe(lambda df: df.assign(price=df.stock_id.map(lambda i: ref_price.get(i, 0))))\
                .pipe(lambda df: df.assign(weight=df.stock_id.map(lambda i: close_price.get(i, 0))*df.quantity / total_allocation * 1000))\
                .pipe(lambda df: df.assign(close_price=df.stock_id.map(lambda i: close_price.get(i, 0))))\
                .pipe(lambda df: df.assign(volume=df.stock_id.map(lambda i: volume.get(i, 0) / 1000)))[["stock_id", "quantity", "price", "weight", "close_price", "volume", "strategy", "type"]]\
                .sort_values('stock_id').set_index('stock_id')
            
            has_odd_lot = (df['quantity'].round(0) - df['quantity']).abs().sum() > 0.00001
            if has_odd_lot:
                df['quantity'] = df['quantity'].map(lambda x: f"{x:.3f}")

        else:
            df = pd.DataFrame()

        if len(df) != 0:
            ret = f'Estimate value {int((df.price.astype(float) * df.quantity.astype(float) * 1000).sum())}'
        else:
            ret = 'Position'

        # add ret string as the title of df
        # show strategies info
        strategy_info = {}
        for name, strategy in pos.items():
            strategy.pop('position')

            # replace key timestamp to updated
            strategy['updated'] = strategy['timestamp']
            strategy.pop('timestamp')

            # replace next_trading_time to expired
            strategy['rebalance_after'] = strategy['next_trading_time']
            strategy.pop('next_trading_time')

            # replace value 1 to 'None' for stop_loss
            strategy['stop_loss'] = strategy['stop_loss'] if strategy['stop_loss'] != 1 else 'None'

            # replace value inf to 'None' for take_profit
            strategy['take_profit'] = strategy['take_profit'] if strategy['take_profit'] != float(
                'inf') else 'None'

            # replace value inf to 'None' for trail_stop
            strategy['trail_stop'] = strategy['trail_stop'] if strategy['trail_stop'] != float(
                'inf') else 'None'

            # simplify str '2024-04-10T18:39:33.032248+00:00' format to %Y-%m-%d %H%m for updated and expiry
            strategy['updated'] = pd.to_datetime(
                strategy['updated']).strftime('%Y-%m-%d %H:%M')
            strategy['rebalance_after'] = pd.to_datetime(
                strategy['rebalance_after']).strftime('%Y-%m-%d %H:%M')

            # make allocation to int
            strategy['allocation'] = int(strategy['allocation'])

            strategy_info[name] = strategy

        if len(strategy_info) != 0:

            df2 = pd.DataFrame(strategy_info).loc[[
                'allocation', 'weight', 'updated', 'stop_loss', 'take_profit', 'trail_stop', 'entry_at', 'exit_at']].T
            
            alloc_sum = self.data['config']['params']['total_balance']

            df2['weight'] = (df2.allocation / alloc_sum).map('{:.2%}'.format) +  '/' + df2['weight'].map('{:.2%}'.format)
        else:
            df2 = pd.DataFrame()

        ret = ret + "\n\n" + df.to_string() + '\n\n\n' + 'strategy\n\n' + df2.to_string()
        pd.reset_option('display.max_rows')
        pd.reset_option('display.float_format')
        return ret

    @staticmethod
    def margin_cash_position_combine(acp, idp):
        """
        合併現金與保證金部位。

        Args:
            acp (Position): 當前帳戶的股票部位。
            idp (Position): 新的帳戶的股票部位。
        """

        diff = (idp - acp)

        cash = {p['stock_id']: p.copy()
                for p in diff.position if p['order_condition'] == OrderCondition.CASH}
        margin_trading = {p['stock_id']: p.copy(
        ) for p in diff.position if p['order_condition'] == OrderCondition.MARGIN_TRADING}

        # cancel negative direction amount
        sids = set(cash.keys()) | set(margin_trading.keys())
        for sid in sids:
            if not (sid in cash and sid in margin_trading):
                continue

            if cash[sid]['quantity'] * margin_trading[sid]['quantity'] < 0:
                reduce_amount = min(abs(cash[sid]['quantity']), abs(
                    margin_trading[sid]['quantity']))

                # reduce toward zero
                if cash[sid]['quantity'] > 0:
                    cash[sid]['quantity'] -= reduce_amount
                    margin_trading[sid]['quantity'] += reduce_amount
                else:
                    cash[sid]['quantity'] += reduce_amount
                    margin_trading[sid]['quantity'] -= reduce_amount

        newdiff = [p for p in cash.values() if p['quantity'] != 0] + \
            [p for p in margin_trading.values() if p['quantity'] != 0]
        newdiff = Position.from_list(newdiff)
        return idp - diff + newdiff

    def compare(self, account):

        # compare stock assets
        p = self.get_position()
        p2 = account.get_position()

