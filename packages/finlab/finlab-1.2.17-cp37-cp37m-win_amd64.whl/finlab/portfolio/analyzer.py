from finlab.online.order_executor import Position
from finlab.online.base_account import Order
from finlab.portfolio import PortfolioSyncManager
from dataclasses import dataclass
from typing import List

@dataclass
class ScheduleRecord:
    time: str

    # scheduled position
    open_position: Position
    close_position: Position


@dataclass
class AccountRecord:
    time: str
    position: Position
    daily_orders: List[Order]


class PortfolioAnalyzer(object):

    def __init__(self):
        self.records = []

    def record_portfolio(self, manager: PortfolioSyncManager):

        self.data['position']
        pass
        
    def record_account(self, account):
        pass
