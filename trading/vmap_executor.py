# coding=utf-8
from datetime import timedelta

from gm.api import *
from trading.base_executor import BaseTradeExecutor
from utils.data_converter import DataConverter
from utils.logger import default_logger as logger


class VWAPTradeExecutor(BaseTradeExecutor):
    """VWAP交易执行器"""

    def execute_buy(self, context, symbol: str, weight: float) -> bool:
        """使用VWAP策略执行买入"""
        try:
            from gm.api import current, history
            end_time = context.now
            start_time = end_time - timedelta(days=5)
            # 获取近期数据计算VWAP
            data = history(
                symbol=symbol,
                frequency='1d',
                start_time=start_time,
                end_time=end_time,
                fields='open,high,low,close,volume,amount',
                df=True,
                skip_suspended=True
            )
            if data is None or data.empty:
                return super().execute_buy(context, symbol, weight)
            # 计算VWAP
            total_volume = data['volume'].sum()
            total_amount = data['amount'].sum()
            if total_volume > 0:
                vwap = total_amount / total_volume
            else:
                vwap = data['close'].iloc[-1]
            current_data = current(symbols=symbol, fields='price')
            if not current_data:
                return False
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
                return False
            # 使用VWAP价格计算数量
            plan_volume = int(plan_amount / vwap / 100) * 100
            if plan_volume < 100:
                return False
            if not self.risk_manager.check_position_limits(context, symbol, plan_volume * vwap):
                return False
            # 以VWAP价格下单
            order_volume(
                symbol=symbol,
                volume=plan_volume,
                side=OrderSide_Buy,
                order_type=OrderType_Limit,
                position_effect=PositionEffect_Open,
                price=vwap
            )
            logger.info(f"VWAP买入委托 {symbol}, 数量: {plan_volume}, VWAP价格: {vwap:.2f}")
            return True
        except Exception as e:
            logger.error(f"VWAP买入执行失败 {symbol}: {e}")
            return super().execute_buy(context, symbol, weight)
