# coding=utf-8
from typing import List
from core.base import StockInfo, IStockSelectionStrategy
from data.base_data_manager import IDataManager


class BaseStockSelectionStrategy(IStockSelectionStrategy):
    """基础选股策略"""

    def __init__(self, config):
        self.config = config

    def select_stocks(self, context, data_manager: IDataManager) -> List[StockInfo]:
        """选股策略 - 基础实现"""
        raise NotImplementedError("子类必须实现此方法")

    def calculate_score(self, context, symbol: str, data_manager: IDataManager) -> float:
        """计算股票得分 - 基础实现"""
        raise NotImplementedError("子类必须实现此方法")
