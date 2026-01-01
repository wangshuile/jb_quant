from typing import Optional

from config.trading_config import TradingConfig
# 数据管理
from data.base_data_manager import BaseDataManager
from data.fixed_data_manager import FixedStockPoolDataManager
from data.index_data_manager import IndexConstituentsDataManager
from strategies.risk_managers.aggressive_risk import AggressiveRiskManager
# 风控管理
from strategies.risk_managers.base_risk import BaseRiskManager
from strategies.risk_managers.conservative_risk import ConservativeRiskManager
# 选股策略
from strategies.selection_strategies.base_selection import BaseStockSelectionStrategy
from strategies.selection_strategies.mean_reversion_selection import MeanReversionStockSelectionStrategy
from strategies.selection_strategies.momentum_selection import MomentumStockSelectionStrategy
from strategies.selection_strategies.volatility_selection import VolatilityStockSelectionStrategy
# 择时策略
from strategies.timing_strategies.base_timing import BaseTimingStrategy
from strategies.timing_strategies.disabled_timing import DisabledTimingStrategy
from strategies.timing_strategies.ma_timing import MovingAverageTimingStrategy
from strategies.timing_strategies.mom_timing import MomentumTimingStrategy
from strategies.timing_strategies.rsi_timing import RSITimingStrategy
# 交易执行器
from trading.base_executor import BaseTradeExecutor
from trading.limit_executor import LimitPriceTradeExecutor
from trading.vmap_executor import VWAPTradeExecutor
from utils.logger import default_logger as logger


class StrategyFactory:
    """策略工厂类"""

    @staticmethod
    def create_data_manager(config: TradingConfig,
                            data_manager_type: Optional[str] = None) -> BaseDataManager:
        """创建数据管理器"""
        if data_manager_type is None:
            data_manager_type = config.data_manager_type

        logger.info(f"创建数据管理器，类型: {data_manager_type}")

        if data_manager_type == "index":
            return IndexConstituentsDataManager(config)
        else:  # 默认使用固定股票池
            return FixedStockPoolDataManager(config)

    @staticmethod
    def create_timing_strategy(config: TradingConfig, timing_type: Optional[str] = None) -> BaseTimingStrategy:
        """创建择时策略"""
        if timing_type is None:
            timing_type = config.timing_strategy_type
        logger.info(f"创建择时策略，类型: {timing_type}")
        if timing_type == "ma":
            return MovingAverageTimingStrategy(config)
        elif timing_type == "momentum":
            return MomentumTimingStrategy(config)
        elif timing_type == "rsi":
            return RSITimingStrategy(config)
        else:  # 默认禁用择时
            return DisabledTimingStrategy(config)

    @staticmethod
    def create_stock_selection_strategy(config: TradingConfig,
                                        selection_type: Optional[str] = None) -> BaseStockSelectionStrategy:
        """创建选股策略"""
        if selection_type is None:
            selection_type = config.stock_selection_type

        logger.info(f"创建选股策略，类型: {selection_type}")

        if selection_type == "mean_reversion":
            return MeanReversionStockSelectionStrategy(config)
        elif selection_type == "volatility":
            return VolatilityStockSelectionStrategy(config)
        else:  # 默认使用动量选股
            return MomentumStockSelectionStrategy(config)

    @staticmethod
    def create_risk_manager(config: TradingConfig, risk_type: Optional[str] = None) -> BaseRiskManager:
        """创建风险管理器"""
        if risk_type is None:
            risk_type = config.risk_manager_type

        logger.info(f"创建风险管理器，类型: {risk_type}")

        if risk_type == "conservative":
            return ConservativeRiskManager(config)
        elif risk_type == "aggressive":
            return AggressiveRiskManager(config)
        else:  # 默认基础风控
            return BaseRiskManager(config)

    @staticmethod
    def create_trade_executor(config: TradingConfig, risk_manager: BaseRiskManager,
                              executor_type: Optional[str] = None) -> BaseTradeExecutor:
        """创建交易执行器"""
        if executor_type is None:
            executor_type = config.trade_executor_type

        logger.info(f"创建交易执行器，类型: {executor_type}")

        if executor_type == "limit":
            return LimitPriceTradeExecutor(config, risk_manager)
        elif executor_type == "vwap":
            return VWAPTradeExecutor(config, risk_manager)
        else:  # 默认市价执行
            return BaseTradeExecutor(config, risk_manager)
