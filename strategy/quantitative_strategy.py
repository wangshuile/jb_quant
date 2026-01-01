from typing import Any

from gm.api import *
from strategy.base_strategy import BaseStrategy
from factory.strategy_factory import StrategyFactory
from config.trading_config import TradingConfig
from utils.logger import default_logger as logger


class QuantitativeTradingStrategy(BaseStrategy):
    """量化交易策略主类 - 使用策略模式"""

    def __init__(self, config: TradingConfig, strategy_factory: StrategyFactory = None):
        super().__init__(config)
        self.factory = strategy_factory or StrategyFactory()
        self._initialize_strategies()

    def _initialize_strategies(self):
        """初始化各个策略组件"""
        self.context.data_manager = self.factory.create_data_manager(self.config)
        self.context.timing_strategy = self.factory.create_timing_strategy(self.config)
        self.context.stock_selection_strategy = self.factory.create_stock_selection_strategy(self.config)
        self.context.risk_manager = self.factory.create_risk_manager(self.config)
        self.context.trade_executor = self.factory.create_trade_executor(
            self.config, self.context.risk_manager
        )

    def init_strategy(self, context: Any):
        """初始化策略"""
        # 设置定时任务
        schedule(schedule_func=self.on_market_open, date_rule='1d', time_rule='09:30:00')
        schedule(schedule_func=self.on_midday, date_rule='1d', time_rule='11:00:00')
        schedule(schedule_func=self.on_afternoon, date_rule='1d', time_rule='13:30:00')
        schedule(schedule_func=self.on_market_close, date_rule='1d', time_rule='14:55:00')
        logger.info("策略初始化完成")

    def on_market_open(self, context: Any):
        """开盘后执行"""
        logger.info("执行开盘策略")
        self.context.data_manager.cache.clear()
        self.context.risk_manager.reset_daily_flags()
        # 更新持仓信息
        self.context.risk_manager.update_position_all(context=context)
        # 选股
        self.context.selected_stocks = self.context.stock_selection_strategy.select_stocks(
            context, self.context.data_manager
        )
        self.context.last_selection_date = context.now.strftime('%Y-%m-%d')
        if self.context.selected_stocks:
            for stock in self.context.selected_stocks:
                logger.info(f"选股: {stock.symbol}, 得分: {stock.score:.3f}")

    def on_midday(self, context: Any):
        """中午执行"""
        current_time = context.now.strftime('%H:%M:%S')
        if not (self.config.trading_start_time <= current_time <= self.config.trading_end_time):
            return

        logger.info("执行中午监控")
        self._execute_stock_selection(context)

    def on_afternoon(self, context: Any):
        """下午执行"""
        current_time = context.now.strftime('%H:%M:%S')
        if not (self.config.trading_start_time <= current_time <= self.config.trading_end_time):
            return

        logger.info("执行下午监控")
        # 检查持仓止盈止损
        self._check_holdings_stop(context)
        # 执行选股买入
        self._execute_stock_selection(context)

    def on_market_close(self, context: Any):
        """收盘前执行"""
        logger.info("执行收盘前策略")
        self._check_holdings_stop(context)

        # 记录当日表现
        performance = self.context.get_performance()
        logger.info(f"当日交易表现: {performance}")

    def on_bar(self, context: Any, bar: dict):
        """K线回调（可选）"""
        # 可以在这里实现基于K线的实时交易信号
        pass

    def _check_holdings_stop(self, context: Any):
        """检查持仓止盈止损"""
        try:
            positions = context.account().positions()
            for position in positions:
                if position['volume'] > 0:
                    symbol = position['symbol']
                    current_data = current(symbols=symbol, fields='price')
                    if current_data:
                        current_price = current_data[0]['price']
                        should_sell, reason = self.context.risk_manager.check_stop_loss_profit(
                            context, symbol, current_price
                        )
                        if should_sell:
                            self.context.trade_executor.execute_sell(context, symbol, reason)
        except Exception as e:
            logger.error(f"检查持仓止盈止损失败: {e}")

    def _execute_stock_selection(self, context: Any):
        """执行选股买入"""
        if not self.context.selected_stocks:
            logger.info("无选股结果，跳过执行")
            return

        total_score = sum(stock.score for stock in self.context.selected_stocks)
        if total_score <= 0:
            total_score = 1

        for stock in self.context.selected_stocks[:self.config.max_positions]:
            symbol = stock.symbol
            # 检查是否已持仓
            positions = context.account().positions(symbol=symbol)
            if positions and positions[0]['volume'] > 0:
                continue
            buy_signal, sell_signal,_ = self.context.timing_strategy.get_signal(
                context, symbol, self.context.data_manager
            )
            if buy_signal and not sell_signal:
                weight = stock.score / total_score * self.config.total_position_ratio
                success = self.context.trade_executor.execute_buy(context, symbol, weight)
                if success:
                    logger.info(f"成功下单买入 {symbol}")
                else:
                    logger.warning(f"下单买入 {symbol} 失败")
            else:
                logger.debug(f"{symbol} 无买入信号")
