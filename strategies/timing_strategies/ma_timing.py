# coding=utf-8
from typing import Tuple

import numpy as np

from data.base_data_manager import IDataManager
from strategies.timing_strategies.base_timing import BaseTimingStrategy
from utils.logger import default_logger as logger


class MovingAverageTimingStrategy(BaseTimingStrategy):
    """移动平均线择时策略"""

    def get_signal(self, context=None, symbol: str = None, data_manager: IDataManager = None,
                   position_symbols: list = None, selected_symbols: list = None) -> Tuple[bool, bool, bool]:
        """基于移动平均线的交易信号"""
        if not self.config.timing_enabled:
            return True, False, False

        try:
            data = data_manager.get_stock_data(context, symbol, 20)
            if len(data) < 10:
                return True, False, False

            close_prices = data['close'].values
            current_price = close_prices[-1]

            # 计算多个均线
            if len(close_prices) >= 5:
                ma_5 = np.mean(close_prices[-5:])
                ma_10 = np.mean(close_prices[-10:])
                ma_20 = np.mean(close_prices[-20:])

                # 多头排列：短期均线在长期均线之上
                buy_signal = ma_5 > ma_10 > ma_20 and current_price > ma_5
            else:
                buy_signal = True

            return buy_signal, False, False

        except Exception as e:
            logger.error(f"择时判断失败 {symbol}: {e}")
            return True, False, False
