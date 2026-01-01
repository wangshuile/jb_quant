# coding=utf-8

from gm.api import *
from trading.base_executor import BaseTradeExecutor
from utils.data_converter import DataConverter
from utils.logger import default_logger as logger


class LimitPriceTradeExecutor(BaseTradeExecutor):
    """限价交易执行器"""

    def execute_buy(self, context, symbol: str, weight: float) -> bool:
        """使用限价单执行买入"""
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
            available_cash = cash * 0.95

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

            # 使用限价单，略高于现价
            limit_price = cur_price * 1.002  # 上浮0.2%
            order_volume(
                symbol=symbol,
                volume=plan_volume,
                side=OrderSide_Buy,
                order_type=OrderType_Limit,
                position_effect=PositionEffect_Open,
                price=limit_price
            )
            logger.info(f"限价买入委托 {symbol}, 数量: {plan_volume}, 价格: {limit_price:.2f}")
            return True

        except Exception as e:
            logger.error(f"限价买入执行失败 {symbol}: {e}")
            return False
