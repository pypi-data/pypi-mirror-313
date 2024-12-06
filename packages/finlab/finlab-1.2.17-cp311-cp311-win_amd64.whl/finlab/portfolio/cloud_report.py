import gzip
import json
import base64
import logging
import datetime
import requests
import pandas as pd

import finlab
from .utils import validate_structure
from finlab.core.report import Report
from finlab.market_info import TWMarketInfo
from finlab.portfolio.portfolio import PositionScheduler

logger = logging.getLogger(__name__)

def create_report_from_cloud(strategy_id, user_id=None):
    """根據提供的用戶ID和策略ID創建在線報告。
    Create an online report based on the user id and strategy id provided.
    
    
    Args:
        user_id (str): The user id.
        strategy_id (str): The
    """

    return CloudReport.from_cloud(strategy_id, user_id)

class CloudReport(Report):

    def __init__(self, sdata, pdata):
        """
        sdata: dict
        pdata: dict
        """

        # mind user about this is the beta version
        logger.info(
            "OnlineReport is in beta version, please report any issue to FinLab Team at https://discord.gg/tAr4ysPqvR")

        required_sdata_structure = {
            'returns': {
                'value': [int, float],
                'time': [str]
            },
            'metrics': {
                'backtest': {
                    'feeRatio': (int, float),
                    'taxRatio': (int, float),
                    'tradeAt': str,
                    'nextTradingDate': (int, float),
                    'market': str,
                    'livePerformanceStart': (int, float),
                    'stopLoss': (int, float, type(None)),
                    'takeProfit': (int, float, type(None)),
                    'trailStop': (int, float, type(None)),
                    'freq': str
                }
            },
            'trades': str
        }

        validate_structure(sdata, required_sdata_structure)

        self.creturn = pd.Series(sdata['returns']['value'],
                            pd.to_datetime(sdata['returns']['time']))
        # fee_ratio = sdata
        self.fee_ratio = sdata['metrics']['backtest']['feeRatio']
        self.tax_ratio = sdata['metrics']['backtest']['taxRatio']
        self.trade_at = sdata['metrics']['backtest']['tradeAt']
        self.last_trading_date = datetime.datetime.fromtimestamp(
            sdata['metrics']['backtest']['nextTradingDate'])

        if sdata['metrics']['backtest']['market'] == 'tw_stock':
            self.market_info = TWMarketInfo()
        else:
            self.market_info = None

        trades = self.reverse_trades(sdata['trades'])
        trades['entry_date'] = pd.to_datetime(trades['entry_date'].map(
            lambda t: datetime.datetime.fromtimestamp(t/1000) if t == t else pd.NaT))
        trades['entry_sig_date'] = pd.to_datetime(trades['entry_sig_date'].map(
            lambda t: datetime.datetime.fromtimestamp(t/1000) if t == t else pd.NaT))
        trades['exit_date'] = pd.to_datetime(trades['exit_date'].map(
            lambda t: datetime.datetime.fromtimestamp(t/1000) if t == t else pd.NaT))
        trades['exit_sig_date'] = pd.to_datetime(trades['exit_sig_date'].map(
            lambda t: datetime.datetime.fromtimestamp(t/1000) if t == t else pd.NaT))
        trades.index.name = 'trade_index'

        super().__init__(self.creturn, pd.DataFrame(0, index=self.creturn.index, columns=[
            '1', '2']), self.fee_ratio, self.tax_ratio, self.trade_at, self.last_trading_date, self.market_info)

        self.trades = trades

        if 'livePerformanceStart' in sdata['metrics']['backtest'] and sdata['metrics']['backtest']['livePerformanceStart'] is not None:
            self.live_performance_start = datetime.datetime.fromtimestamp(
                sdata['metrics']['backtest']['livePerformanceStart'])
        else:
            self.live_performance_start = None
            
        self.stop_loss = sdata['metrics']['backtest']['stopLoss']
        self.take_profit = sdata['metrics']['backtest']['takeProfit']
        self.trail_stop = sdata['metrics']['backtest']['trailStop']
        self.resample = sdata['metrics']['backtest']['freq']
        self.pdata = pdata
        self.sdata = sdata
        self.position_schedulers = PositionScheduler.from_json(
            pdata)

    def get_metrics(self):
        return self.sdata['metrics']

    def position_info2(self):
        return self.pdata

    def reverse_trades(self, gzip_b64_str: str) -> pd.DataFrame:
        """Reverse trades from gzip_b64_str"""

        # Decode base64 string to gzip bytes
        gzip_bytes = base64.b64decode(gzip_b64_str)

        # Decompress gzip bytes to JSON bytes
        json_bytes = gzip.decompress(gzip_bytes)

        # Decode JSON bytes to JSON string
        json_str = json_bytes.decode('utf-8')

        # Convert JSON string to DataFrame
        trades_df = pd.DataFrame(json.loads(json_str))

        return trades_df

    @classmethod
    def from_cloud(cls, strategy_id, user_id=None):

        url = 'https://asia-east2-fdata-299302.cloudfunctions.net/auth_get_strategy'

        params = {
            'api_token': finlab.get_token(),
            'sid': strategy_id,
            'uid': user_id,
        }

        if user_id is None:
            del params['uid']

        res = requests.get(url, params)

        if res.status_code != 200:
            raise Exception(res.text)

        data = res.json()

        if not data:
            raise ValueError('No strategy found')
        
        pdata = data['position']
        sdata = data['strategy']

        if pdata is None:
            raise ValueError(f'No strategy {strategy_id} found')

        if 'position2' in pdata:
            pdata = pdata['position2']
        elif 'position' in pdata:
            pdata = pdata['position']

        return cls(sdata, pdata)