# coding=utf-8
from typing import List
import numpy as np

from data.base_data_manager import IDataManager
from core.base import StockInfo
from strategies.selection_strategies.base_selection import BaseStockSelectionStrategy
from utils.logger import default_logger as logger


class MomentumStockSelectionStrategy(BaseStockSelectionStrategy):
    """动量选股策略"""

    def select_stocks(self, context, data_manager: IDataManager) -> List[StockInfo]:
        """基于动量的选股策略"""
        selected_stocks = []
        stock_pool = data_manager.get_stock_pool(context, self.config.stock_pool_size * 2)  # 获取更多股票进行筛选

        if not stock_pool:
            logger.warning("股票池为空，无法进行选股")
            return []

        logger.info(f"开始对{len(stock_pool)}只股票进行动量评分")

        for symbol in stock_pool:
            try:
                symbol_str = str(symbol).strip()
                score = self.calculate_score(context, symbol_str, data_manager)

                selected_stocks.append(StockInfo(
                    symbol=symbol_str,
                    score=max(score, 0.1)
                ))

            except Exception as e:
                logger.debug(f"选股计算失败 {symbol}: {e}")
                continue

        if not selected_stocks:
            logger.warning("没有股票被选中，使用备用方案")
            for symbol in stock_pool[:self.config.stock_pool_size]:
                selected_stocks.append(StockInfo(
                    symbol=symbol,
                    score=0.5
                ))

        selected_stocks.sort(key=lambda x: x.score, reverse=True)
        selected_stocks = selected_stocks[:self.config.stock_pool_size]

        logger.info(f"选股完成，选中{len(selected_stocks)}只股票")
        for stock in selected_stocks:
            logger.info(f"选中股票: {stock.symbol}, 得分: {stock.score:.3f}")

        return selected_stocks

    def calculate_score(self, context, symbol: str, data_manager: IDataManager) -> float:
        """计算动量得分"""
        try:
            data = data_manager.get_stock_data(context, symbol, 20)
            if len(data) < 10:
                return 0.5

            close_prices = data['close'].values
            current_price = close_prices[-1]

            # 计算多个时间周期的动量
            momentum_scores = []

            # 5日动量
            if len(close_prices) >= 6:
                momentum_5 = (current_price - close_prices[-6]) / close_prices[-6]
                momentum_scores.append(momentum_5)

            # 10日动量
            if len(close_prices) >= 11:
                momentum_10 = (current_price - close_prices[-11]) / close_prices[-11]
                momentum_scores.append(momentum_10)

            # 20日动量
            if len(close_prices) >= 21:
                momentum_20 = (current_price - close_prices[-21]) / close_prices[-21]
                momentum_scores.append(momentum_20)

            if not momentum_scores:
                return 0.5

            # 综合动量得分
            avg_momentum = np.mean(momentum_scores)
            score = 0.5 + avg_momentum * 3  # 放大动量效应

            return max(0.1, min(score, 1.0))

        except Exception as e:
            logger.debug(f"计算{symbol}得分失败: {e}")
            return 0.5
