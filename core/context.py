from dataclasses import dataclass
from typing import List, Optional

from core.base import StockInfo, IDataManager, ITimingStrategy, IStockSelectionStrategy, IRiskManager, ITradeExecutor


@dataclass
class TradingContext:
    """交易上下文，封装策略运行环境"""

    # 策略组件
    data_manager: Optional[IDataManager] = None
    timing_strategy: Optional[ITimingStrategy] = None
    stock_selection_strategy: Optional[IStockSelectionStrategy] = None
    risk_manager: Optional[IRiskManager] = None
    trade_executor: Optional[ITradeExecutor] = None

    # 选股结果
    selected_stocks: List[StockInfo] = None
    last_selection_date: Optional[str] = None
    # 待买入的股票
    buy_stocks: List[str] = None
    # 待卖出的股票
    sell_stocks: List[str] = None
    # 待减仓股票
    reduce_position_stocks: List[str] = None

    # 性能统计
    trade_count: int = 0
    win_count: int = 0
    total_return: float = 0.0

    def __post_init__(self):
        if self.selected_stocks is None:
            self.selected_stocks = []

        if self.buy_stocks is None:
            self.buy_stocks = []

        if self.sell_stocks is None:
            self.sell_stocks = []

        if self.reduce_position_stocks is None:
            self.reduce_position_stocks = []

    def reset_daily(self):
        """重置每日数据"""
        self.selected_stocks.clear()

    def record_trade(self, symbol: str, returns: float):
        """记录交易结果"""
        self.trade_count += 1
        self.total_return += returns
        if returns > 0:
            self.win_count += 1

    def get_performance(self) -> dict:
        """获取性能统计"""
        win_rate = self.win_count / self.trade_count if self.trade_count > 0 else 0
        avg_return = self.total_return / self.trade_count if self.trade_count > 0 else 0
        return {
            'trade_count': self.trade_count,
            'win_count': self.win_count,
            'win_rate': win_rate,
            'total_return': self.total_return,
            'avg_return': avg_return
        }
