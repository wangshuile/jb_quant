# coding=utf-8
from typing import Tuple
from data.base_data_manager import IDataManager
from strategies.timing_strategies.base_timing import BaseTimingStrategy


class DisabledTimingStrategy(BaseTimingStrategy):
    """禁用择时策略"""

    def get_signal(self, context=None, symbol: str = None, data_manager: IDataManager = None,
                   position_symbols: list = None, selected_symbols: list = None) -> Tuple[bool, bool, bool]:
        """始终返回买入信号"""
        return True, False,False
