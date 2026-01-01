# coding=utf-8
from datetime import timedelta
from typing import Any, Dict, List

import pandas as pd
from gm.api import *

from core.base import IDataManager
from utils.cache_manager import CacheManager
from utils.data_converter import DataConverter
from utils.logger import default_logger as logger


class BaseDataManager(IDataManager):
    """基础数据管理器"""

    def __init__(self, config):
        self.config = config
        self.cache = CacheManager()

    def get_stock_pool(self, context, size: int) -> List[str]:
        """获取股票池 - 基础实现"""
        raise NotImplementedError("子类必须实现此方法")

    def get_stock_data(self, context, symbol: str, count: int, frequency: str = '1d') -> pd.DataFrame:
        """获取股票数据"""
        symbol_str = str(symbol).strip()
        cache_key = f"{symbol_str}_{frequency}_{count}"
        cached_data = self.cache.get(cache_key)
        if cached_data is not None:
            return cached_data
        try:
            end_time = context.now
            start_time = end_time - timedelta(days=count * 2)
            data = history(
                symbol=symbol_str,
                frequency=frequency,
                start_time=start_time,
                end_time=end_time,
                fields='open,high,low,close,volume,amount',
                df=True,
                skip_suspended=True,
                fill_missing='Last'
            )
            if data is None or data.empty:
                logger.warning(f"获取{symbol_str}数据为空")
                return pd.DataFrame()
            data = data.sort_index()
            if len(data) > count:
                data = data.tail(count)
            self.cache.set(cache_key, data)
            return data
        except Exception as e:
            logger.error(f"获取{symbol_str}数据失败: {e}")
            return pd.DataFrame()

    def get_current_data(self, context, symbols: List[str]) -> Dict[str, Any]:
        """获取当前数据"""
        from gm.api import current
        try:
            if not symbols:
                return {}
            current_data = current(symbols=symbols, fields='open,high,low,price,volume,amount')
            result = {}
            for data in current_data:
                symbol = data['symbol']
                result[symbol] = {
                    'open': DataConverter.safe_float(data.get('open', 0)),
                    'high': DataConverter.safe_float(data.get('high', 0)),
                    'low': DataConverter.safe_float(data.get('low', 0)),
                    'price': DataConverter.safe_float(data.get('price', 0)),
                    'volume': DataConverter.safe_float(data.get('volume', 0)),
                    'amount': DataConverter.safe_float(data.get('amount', 0))
                }
            return result
        except Exception as e:
            logger.error(f"获取当前数据失败: {e}")
            return {}
