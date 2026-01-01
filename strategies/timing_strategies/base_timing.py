# coding=utf-8
from typing import Tuple

from core.base import ITimingStrategy
from data.base_data_manager import IDataManager


class BaseTimingStrategy(ITimingStrategy):
    """基础择时策略"""

    def __init__(self, config):
        self.config = config

    def get_signal(self, context=None, symbol: str = None, data_manager: IDataManager = None,
                   position_symbols: list = None, selected_symbols: list = None) -> Tuple[bool, bool, bool]:
        """获取交易信号 - 基础实现"""
        raise NotImplementedError("子类必须实现此方法")
