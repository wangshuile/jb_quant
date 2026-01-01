from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any
import pandas as pd
from dataclasses import dataclass


@dataclass
class StockInfo:
    """股票信息数据类"""
    symbol: str
    score: float = 0.0
    current_price: float = 0.0
    data: Optional[pd.DataFrame] = None
    industry: str = ""
    market_cap: float = 0.0


@dataclass
class PositionRecord:
    """持仓记录数据类"""
    symbol: str
    avg_cost: float
    highest_price: float
    update_time: Any
    buy_date: str
    volume: int = 0


class IDataManager(ABC):
    """数据管理器接口"""

    @abstractmethod
    def get_stock_pool(self, context, size: int) -> List[str]:
        pass

    @abstractmethod
    def get_stock_data(self, context, symbol: str, count: int, frequency: str = '1d') -> pd.DataFrame:
        pass

    @abstractmethod
    def get_current_data(self, context, symbols: List[str]) -> Dict[str, Any]:
        pass


class ITimingStrategy(ABC):
    """择时策略接口"""

    @abstractmethod
    def get_signal(self, context=None, symbol: str = None, data_manager: IDataManager = None,
                   position_symbols: list = None, selected_symbols: list = None) -> Tuple[bool, bool, bool]:
        pass


class IStockSelectionStrategy(ABC):
    """选股策略接口"""

    @abstractmethod
    def select_stocks(self, context, data_manager: IDataManager) -> List[StockInfo]:
        pass

    @abstractmethod
    def calculate_score(self, context, symbol: str, data_manager: IDataManager) -> float:
        pass


class IRiskManager(ABC):
    """风险管理器接口"""

    @abstractmethod
    def check_position_limits(self, context, symbol: str, plan_amount: float) -> bool:
        pass

    @abstractmethod
    def check_stop_loss_profit(self, context, symbol: str, current_price: float) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def can_sell_today(self, context, symbol: str) -> bool:
        pass

    @abstractmethod
    def update_position_record(self, context, symbol: str, avg_cost: float, volume: int,update_time:Any):
        pass

    @abstractmethod
    def update_position_all(self,context):
        pass


class ITradeExecutor(ABC):
    """交易执行器接口"""

    @abstractmethod
    def execute_buy(self, context, symbol: str, weight: float) -> bool:
        pass

    @abstractmethod
    def execute_sell(self, context, symbol: str, reason: str) -> bool:
        pass

    @abstractmethod
    def execute_reduce_position(self, context, symbol: str, weight: float) -> bool:
        pass