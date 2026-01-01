# coding=utf-8
from typing import Tuple

import numpy as np

from data.base_data_manager import IDataManager
from strategies.timing_strategies.base_timing import BaseTimingStrategy
from utils.logger import default_logger as logger


class RSITimingStrategy(BaseTimingStrategy):
    """RSI择时策略"""

    def get_signal(self, context=None, symbol: str = None, data_manager: IDataManager = None,
                   position_symbols: list = None, selected_symbols: list = None) -> Tuple[bool, bool, bool]:
        """基于RSI的交易信号"""
        try:
            data = data_manager.get_stock_data(context, symbol, 15)
            if len(data) < 14:
                return True, False,False

            close_prices = data['close'].values

            # 计算RSI
            rsi = self.calculate_rsi(close_prices, 14)
            current_rsi = rsi[-1] if len(rsi) > 0 else 50

            # RSI低于30为超卖，买入信号
            buy_signal = current_rsi < 30
            sell_signal = current_rsi > 70

            return buy_signal, sell_signal,False

        except Exception as e:
            logger.error(f"RSI择时判断失败 {symbol}: {e}")
            return True, False,False

    def calculate_rsi(self, prices: np.ndarray, period: int = 14) -> np.ndarray:
        """计算RSI指标"""
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gains = np.zeros_like(prices)
        avg_losses = np.zeros_like(prices)
        # 初始值
        avg_gains[period] = np.mean(gains[:period])
        avg_losses[period] = np.mean(losses[:period])
        # 计算后续值
        for i in range(period + 1, len(prices)):
            avg_gains[i] = (avg_gains[i - 1] * (period - 1) + gains[i - 1]) / period
            avg_losses[i] = (avg_losses[i - 1] * (period - 1) + losses[i - 1]) / period
        rs = avg_gains / (avg_losses + 1e-10)  # 避免除零
        rsi = 100 - (100 / (1 + rs))
        return rsi
