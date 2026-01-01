from abc import ABC, abstractmethod
from typing import Any

from core.context import TradingContext
from utils.logger import default_logger as logger


class BaseStrategy(ABC):
    """策略基类"""

    def __init__(self, config):
        self.config = config
        self.context = TradingContext()
        self.initialized = False

    @abstractmethod
    def init_strategy(self, context: Any):
        """初始化策略"""
        pass

    @abstractmethod
    def on_market_open(self, context: Any):
        """开盘后执行"""
        pass

    @abstractmethod
    def on_market_close(self, context: Any):
        """收盘前执行"""
        pass

    @abstractmethod
    def on_bar(self, context: Any, bar: dict):
        """K线回调"""
        pass

    def before_trading_start(self, context: Any):
        """交易开始前执行"""
        if not self.initialized:
            self.init_strategy(context)
            self.initialized = True

    def after_trading_end(self, context: Any):
        """交易结束后执行"""
        # 记录当日表现
        performance = self.context.get_performance()
        logger.info(f"当日表现: {performance}")

        # 重置选股结果
        self.context.reset_daily()
