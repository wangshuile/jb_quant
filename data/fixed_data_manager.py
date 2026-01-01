# coding=utf-8
from typing import List
from data.base_data_manager import BaseDataManager
from utils.logger import default_logger as logger


class FixedStockPoolDataManager(BaseDataManager):
    """固定股票池数据管理器"""

    def get_stock_pool(self, context, size: int) -> List[str]:
        """获取固定股票池"""
        try:
            fixed_symbols = [
                'SHSE.600519',  # 贵州茅台
                'SHSE.601318',  # 中国平安
                'SZSE.000858',  # 五粮液
                'SZSE.000333',  # 美的集团
                'SHSE.600036',  # 招商银行
            ]
            logger.info(f"使用固定股票池，共{len(fixed_symbols)}只股票")
            return fixed_symbols[:size]
        except Exception as e:
            logger.error(f"获取股票池失败: {e}")
            return ['SHSE.600519', 'SHSE.601318'][:size]
