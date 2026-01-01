# coding=utf-8
from typing import List
import numpy as np
from data.base_data_manager import IDataManager
from core.base import StockInfo
from strategies.selection_strategies.base_selection import BaseStockSelectionStrategy
from utils.logger import default_logger as logger


class MeanReversionStockSelectionStrategy(BaseStockSelectionStrategy):
    """均值回归选股策略"""

    def select_stocks(self, context, data_manager: IDataManager) -> List[StockInfo]:
        """基于均值回归的选股策略"""
        selected_stocks = []
        stock_pool = data_manager.get_stock_pool(context, self.config.stock_pool_size * 2)

        if not stock_pool:
            logger.warning("股票池为空，无法进行选股")
            return []

        logger.info(f"开始对{len(stock_pool)}只股票进行均值回归评分")

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
        """计算均值回归得分"""
        try:
            data = data_manager.get_stock_data(context, symbol, 30)
            if len(data) < 20:
                return 0.5

            close_prices = data['close'].values
            current_price = close_prices[-1]

            # 计算价格相对于多个均线的位置
            deviations = []

            # 相对于5日均线
            if len(close_prices) >= 5:
                ma_5 = np.mean(close_prices[-5:])
                dev_5 = (current_price - ma_5) / ma_5
                deviations.append(dev_5)

            # 相对于10日均线
            if len(close_prices) >= 10:
                ma_10 = np.mean(close_prices[-10:])
                dev_10 = (current_price - ma_10) / ma_10
                deviations.append(dev_10)

            # 相对于20日均线
            if len(close_prices) >= 20:
                ma_20 = np.mean(close_prices[-20:])
                dev_20 = (current_price - ma_20) / ma_20
                deviations.append(dev_20)

            if not deviations:
                return 0.5

            # 负偏离越大，得分越高（均值回归）
            avg_deviation = np.mean(deviations)
            score = 0.5 - avg_deviation * 2  # 负偏离得高分

            return max(0.1, min(score, 1.0))

        except Exception as e:
            logger.debug(f"计算{symbol}得分失败: {e}")
            return 0.5
