# coding=utf-8

from gm.api import *
from core.base import ITradeExecutor
from strategies.risk_managers.base_risk import IRiskManager
from utils.data_converter import DataConverter
from utils.logger import default_logger as logger


class BaseTradeExecutor(ITradeExecutor):
    """基础交易执行器"""

    def execute_reduce_position(self, context, symbol: str, weight: float) -> bool:
        pass

    def __init__(self, config, risk_manager: IRiskManager):
        self.config = config
        self.risk_manager = risk_manager

    def execute_buy(self, context, symbol: str, weight: float) -> bool:
        """执行买入"""
        try:
            from gm.api import current
            current_data = current(symbols=symbol, fields='price')
            if not current_data:
                logger.warning(f"无法获取{symbol}的当前价格")
                return False
            cur_price = DataConverter.safe_float(current_data[0])
            account = context.account()
            cash = DataConverter.safe_float(account.cash)
            positions = account.positions()
            total_position_value = 0
            for pos in positions:
                volume = DataConverter.safe_float(pos['volume'])
                price = DataConverter.safe_float(pos['price'])
                total_position_value += volume * price

            total_assets = cash + total_position_value

            plan_amount = total_assets * weight
            available_cash = cash * 0.95  # 保留5%现金

            if plan_amount > available_cash:
                plan_amount = available_cash

            if plan_amount <= 0:
                logger.debug(f"计划买入金额为0: {symbol}")
                return False

            plan_volume = int(plan_amount / cur_price / 100) * 100

            if plan_volume < 100:
                logger.debug(f"买入数量不足100股: {symbol}")
                return False

            if not self.risk_manager.check_position_limits(context, symbol, plan_volume * cur_price):
                return False

            # 执行买入
            order_volume(
                symbol=symbol,
                volume=plan_volume,
                side=OrderSide_Buy,
                order_type=OrderType_Market,
                position_effect=PositionEffect_Open
            )
            logger.info(
                f"买入委托 {symbol}, 数量: {plan_volume}, 价格: {cur_price:.2f}, 金额: {plan_volume * cur_price:.2f}")
            return True
        except Exception as e:
            logger.error(f"买入执行失败 {symbol}: {e}")
            return False

    def execute_sell(self, context, symbol: str, reason: str) -> bool:
        """执行卖出"""
        try:
            from gm.api import current
            if not self.risk_manager.can_sell_today(context, symbol):
                logger.debug(f"T+1限制，无法卖出 {symbol}")
                return False
            positions = context.account().positions(symbol=symbol)
            if not positions or DataConverter.safe_float(positions[0]['volume']) <= 0:
                return False
            position = positions[0]
            volume_to_sell = int(DataConverter.safe_float(position['volume']))
            cur_price = DataConverter.safe_float(current(symbols=symbol, fields='price')[0])
            order_target_percent(symbol=symbol, percent=0, order_type=OrderType_Market, price=cur_price,
                                 position_side=PositionSide_Long)
            logger.info(f"卖出 {symbol}, 数量: {volume_to_sell}, 价格: {cur_price:.2f}, 原因: {reason}")
            return True

        except Exception as e:
            logger.error(f"卖出执行失败 {symbol}: {e}")
            return False
