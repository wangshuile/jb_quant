# coding=utf-8
from typing import Tuple

from data.base_data_manager import IDataManager
from strategies.timing_strategies.base_timing import BaseTimingStrategy
from utils.logger import default_logger as logger


class MomentumTimingStrategy(BaseTimingStrategy):
    """动量择时策略"""

    def get_signal(self, context=None, symbol: str = None, data_manager: IDataManager = None,
                   position_symbols: list = None, selected_symbols: list = None) -> Tuple[bool, bool, bool]:
        """基于动量的交易信号"""
        try:
            data = data_manager.get_stock_data(context, symbol, 10)
            if len(data) < 5:
                return True, False,False

            close_prices = data['close'].values
            current_price = close_prices[-1]

            # 计算5日动量
            if len(close_prices) >= 6:
                momentum_5 = (current_price - close_prices[-6]) / close_prices[-6]
                # 计算10日动量
                momentum_10 = (current_price - close_prices[-11]) / close_prices[-11] if len(close_prices) >= 11 else 0

                buy_signal = momentum_5 > 0 and momentum_10 > 0
            else:
                buy_signal = True

            return buy_signal, False,False

        except Exception as e:
            logger.error(f"动量择时判断失败 {symbol}: {e}")
            return True, False,False
