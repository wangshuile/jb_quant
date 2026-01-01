# coding=utf-8
from typing import List
from gm.api import *
from data.base_data_manager import BaseDataManager
from utils.logger import default_logger as logger


class IndexConstituentsDataManager(BaseDataManager):
    """指数成分股数据管理器"""

    def get_stock_pool(self, context, size: int) -> List[str]:
        """获取指数成分股"""
        try:
            if self.config.mode == 'BACKTEST':
                constituents_data = stk_get_index_constituents(
                    index='SHSE.000300',
                    trade_date=context.now.strftime('%Y-%m-%d')
                )
            else:
                constituents_data = stk_get_index_constituents(index='SHSE.000300')

            if constituents_data is None or len(constituents_data) == 0:
                logger.warning("获取到的成分股数据为空")
                return []

            if hasattr(constituents_data, 'columns') and 'symbol' in constituents_data.columns:
                symbols = constituents_data['symbol'].tolist()
            else:
                logger.warning("成分股数据格式未知")
                return []

            filtered_symbols = []
            for symbol in symbols[:size * 3]:
                try:
                    symbol_str = str(symbol).strip()
                    if not symbol_str:
                        continue
                    stock_info_list = get_instrumentinfos(symbols=symbol_str)
                    if not stock_info_list:
                        continue
                    stock_info = stock_info_list[0]
                    symbol_name = getattr(stock_info, 'symbol_name', '')
                    if symbol_name and ('ST' in symbol_name or '*ST' in symbol_name):
                        continue
                    if not symbol_str.startswith('BJ'):
                        filtered_symbols.append(symbol_str)
                except Exception as e:
                    logger.debug(f"过滤股票{symbol}时出错: {e}")
                    continue
                if len(filtered_symbols) >= size:
                    break

            logger.info(f"获取到{len(filtered_symbols)}只成分股")
            return filtered_symbols[:size]

        except Exception as e:
            logger.error(f"获取指数成分股失败: {e}")
            return []
